# -*- coding: UTF-8 -*-
from django.db import models
from users.models import AbstractUser
import mptt
import users
from mptt.fields import TreeForeignKey
from jsonfield import JSONField
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.conf import settings

GENDER_CHOICES = (('W', 'weiblich',),('M', 'männlich',))


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    jsondata = JSONField(editable=False, default={})
    
    class Meta:
        abstract = True


class School(BaseModel):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=200)
    address = models.TextField()
    contact_person = models.TextField()
    
    class Meta:
        verbose_name = 'Schule'
        verbose_name_plural = 'Schulen'
        
    def get_grades(self):
        ''' Retrieves all grades of this school '''
        return Grade.objects.select_related().filter(school=self)
    
    def get_teachers(self):
        ''' Retrieves all teachers of this school '''
        return Teacher.objects.select_related().filter(school=self)
    
    def get_pupils(self):
        return Pupil.objects.filter(school=self)
    
    def get_teaching_assignments(self):
        return TeachingAssignment.objects.filter(grade__school=self)
    
    def __unicode__(self):
        return '%s' % (self.name)


class Teacher(AbstractUser):
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Geschlecht')
    phone = models.CharField(max_length=255, null=True, blank=True, verbose_name='Telefon')
    school = models.ForeignKey(School, verbose_name='Schule')

    class Meta:
        verbose_name = 'LehrerIn'
        verbose_name_plural = 'LehrerInnen'

    def get_gender(self):
        ''' Retrieves gender of this teacher '''
        return 'Herr' if (self.gender=='M') else 'Frau';
    
    def get_grades(self):
        ''' Retrieves all grades the teacher is teaching in '''
        return Grade.objects.filter(teachingassignment__teacher=self).distinct()
    
    def get_subjects(self):
        ''' Retrieves all subjects the teacher is teaching for '''
        return Subject.objects.filter(teachingassignment__teacher=self)
    
    def get_grade_subjects(self, grade):
        ''' Retrieves all subjects the teacher is teaching for the given grade '''
        return Subject.objects.filter(teachingassignment__teacher=self, teachingassignment__grade=grade)
    

    def __unicode__(self):
        return '%s %s %s' % (self.get_gender(), self.first_name, self.last_name)        

    def get_salutation(self):
        return '%s %s' % (self.first_name, self.last_name)
        
    def full_salutation(self):
        s = ''
        if self.gender == 'W':
            s+= 'Frau '
        else:
            s+= 'Herr '
        return s + self.get_salutation()

users.register(Teacher,dict(
    APP_LABEL = 'gsaudit',
    URL_PREFIX = 'teachers',
    FROM_EMAIL = settings.DEFAULT_FROM_EMAIL,
    LOGIN_URL = '/teachers/login/',
    CONFIRM_EMAIL_SUBJECT = 'Ihr Zugang für GS-Kompetenzen',
    LOGIN_REDIRECT_URL = '/',
    LOGOUT_REDIRECT_URL = '/teachers/login/',
    USE_USER_EMAIL = True,
    ADDITIONALLY_SEND_TO = [],
))        

class Grade(BaseModel):
    name = models.CharField(max_length=255)
    school = models.ForeignKey(School, verbose_name='Schule')
    pupils = models.ManyToManyField('Pupil', through='GradeParticipant', null=True, blank=True)

    class Meta:
        verbose_name = 'Klasse'
        verbose_name_plural = 'Klassen'
    
    def get_all_subjects(self):
        ''' Retrieves all subjects of this grade '''
        return Subject.objects.filter(teachingassignment__grade=self)
    
    def get_all_teachers(self):
        ''' Retrieves all teachers of this grade '''
        return Teacher.objects.filter(teachingassignment__grade=self)
    
    def get_subject_teacher(self, subject):
        ''' Retrieves the teacher for the given subjects in this grade '''
        return Teacher.objects.get(teachingassignment__grade=self, teachingassignment__subject=subject)
    
    def get_teacher_subjects(self, teacher):
        ''' Retrieves all subjects of the given teacher in this grade '''
        return Subject.objects.filter(teachingassignment__grade=self, teachingassignment__teacher=teacher)
        
    def get_participants(self):
        ''' Retrieves all participants in this grade '''
        return Pupil.objects.filter(gradeparticipant__grade=self).order_by('last_name')
    
    def __unicode__(self):
        return self.name


class Pupil(BaseModel):
    first_name = models.CharField(max_length=255, verbose_name='Vorname')
    last_name = models.CharField(max_length=255, verbose_name='Nachname')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Geschlecht')
    birthday = models.DateField(verbose_name='Geburtsdatum', blank=True, null=True)
    note = models.TextField(null=True, blank=True, verbose_name='Notiz')
    school = models.ForeignKey(School, verbose_name='Schule')

    class Meta:
        verbose_name = 'SchülerIn'
        verbose_name_plural = 'SchülerInnen'
        ordering = ('last_name', 'first_name')

    def gradeparticipant_vis(self):
        return ' '.join([unicode(x) for x in self.gradeparticipant_set.all()])

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_all_grades(self):
        ''' Retrieves all grades in which this pupil is participating '''
        return Grade.objects.filter(gradeparticipant__pupil=self)

    def get_all_subjects(self):
        ''' Retrieves all subjects in which this pupil is participating '''
        subjects = []
        for grade in self.get_all_grades():
            subjects += grade.get_all_subjects()
            
        return subjects;

    def get_grade_subjects(self, grade_id):
        ''' Retrieves all subjects for the given in which this pupil is participating '''
        return Grade.objects.get(id=grade_id).get_all_subjects()

    def get_grade_subject_teacher(self, grade_id, subject_id):
        ''' Retrieves the teacher for the given grade in which this pupil is participating and for the subject of this pupil '''
        return Grade.objects.get(id=grade_id).get_subject_teacher(subject_id)
    
    def get_all_teachers(self):
        ''' Retrieves all teachers from this pupil '''
        teachers = []
        for grade in self.get_grades():
            teachers += grade.get_teachers()
            
        return teachers

    def get_grade_teachers(self, grade):
        raise Exception('Not implemented yet')

    def get_audit_skills(self, audit):
        ''' Retrieves all skills evaluated for this pupil '''
        return Skill.objects.select_related().filter(pupilauditskill__pupil=self, pupilauditskill__audit=audit)

    def get_skill_audits(self, skill):
        ''' Retrieves the audits of this pupil in wich the given skill is evaluated '''
        return Audit.objects.select_related().filter(pupilauditskill__pupil=self, pupilauditskill__skill=skill)

    def get_audit_skill_rate(self, audit, skill):
        ''' Retrieves the rating of this pupil for the given skill and given audit '''
        return Skill.objects.select_related().filter(
             pupilauditskill__pupil=self, 
             pupilauditskill__audit=audit, 
             pupilauditskill__skill=skill)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Skill(BaseModel):
    ''' Skills are assigned to a subject or other skill '''
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True, verbose_name='Kompetenzbeschreibung')
    pupil_description = models.TextField(null=True, blank=True, verbose_name='Schülergerechte Übersetzung')
    weight = models.IntegerField(default=0, verbose_name='Gewichtung')
    #TODO: Baumhöhe auf 1 Kind reduzieren!
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name='Unterknoten von')
    
    min_skill_level = models.IntegerField(null=True, blank=True, verbose_name='Geeignet von')
    max_skill_level = models.IntegerField(null=True, blank=True, verbose_name='Geeignet bis')
    
    author = models.ForeignKey(Teacher, null=True, blank=True, verbose_name='Autor')

    class Meta:
        verbose_name = 'Kompetenz'
        verbose_name_plural = 'Kompetenzen'

    def get_audits(self):
        ''' Retrieves all audits evaluated for this skill '''
        return Audit.objects.filter(auditskill__skill=self)

    def __unicode__(self):
        return '%s' % (self.name, )
        
    def get_skill_range(self):
        # check for None explicitely as the skill level can be 0
        if self.is_leaf_node() and self.min_skill_level != None and self.max_skill_level != None:
            return range(self.min_skill_level, self.max_skill_level + 1)
    
    def skill_range_admin(self):
        if self.is_leaf_node():
            if self.min_skill_level and self.max_skill_level:
                return range(self.min_skill_level, self.max_skill_level + 1)
            else:
                return 'nicht angegeben'
        else:
            return ''
    skill_range_admin.short_description = "Schwierigkeitsgrad"
    
    def augment_skill_level_attrs(self, ta):
        rs = self.get_skill_range()
        rta = ta.get_skill_range()
        if rs and rta:        
            if rta[0] in rs or rta[-1] in rs:
                tag = '<span class="skill-ok">%s</span>' 
            elif rta[0] > rs[-1]:
                tag = '<span class="skill-beginner">%s</span>'
            elif rta[0] < rs[0]:
                tag = '<span class="skill-pro">%s</span>' 
        else:
            tag = '<span class="skill-ok">%s</span>' 
        
        self.skill_tag = mark_safe(tag % escape(self.name))
            
    augment_attrs = augment_skill_level_attrs
    


class Subject(BaseModel):
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = 'Fach'
        verbose_name_plural = 'Fächer'

    def get_grade_subject_audits(self, grade, subject):
        '''Retrieves all audits belonging to a subject in a grade'''
        return Audit.objects.filter(subject=subject, grade=grade)
        

    def get_all_teachers(self):
        ''' Retrieves all teachers teaching this subject '''
        return Teacher.objects.filter(teachingassignment__subject=self).distinct()

    def get_all_grades(self):
        ''' Retrieves all assigned grades for this subject '''
        return Grade.objects.filter(teachingassignment__subject=self)

    def __unicode__(self):
        return '%s' % (self.name)

class GradeParticipant(BaseModel):
    '''
    A pupil is part of a grade.
    '''
    grade = models.ForeignKey(Grade, verbose_name='Klasse')
    pupil = models.ForeignKey(Pupil, verbose_name='SchülerIn')

    class Meta:
        verbose_name = 'KlassenteilnehmerIn'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '%s in %s' % (self.pupil.first_name, self.grade.name )



class TeachingAssignment(BaseModel):
    ''' 
    Teachers teach different subject in different grades.
    '''
    teacher = models.ForeignKey(Teacher, verbose_name='LehrerIn')
    grade = models.ForeignKey(Grade, verbose_name='Klasse')
    subject = models.ForeignKey(Subject, verbose_name='Fach')
    skill = models.ForeignKey('Skill', verbose_name='Kompetenzbaum')
    note = models.TextField(blank=True, null=True, verbose_name='Notizen')
    
    min_skill_level = models.IntegerField(null=True, blank=True, verbose_name='Schwierigkeitsgrad von')
    max_skill_level = models.IntegerField(null=True, blank=True, verbose_name='Schwierigkeitsgrad bis')
    
    class Meta:
        verbose_name = 'Lehrauftrag'
        verbose_name_plural = 'Lehraufträge'
        
    def __unicode__(self):
        return '%s:%s:%s' % (self.teacher.last_name, self.grade.name, self.subject.name )
    
    def get_skill_range(self):
        if self.min_skill_level and self.max_skill_level:
            return range(self.min_skill_level, self.max_skill_level + 1)

    def get_all_skills(self, include_root=False):
        ''' Retrieves all assigned skills for this subject '''
        return self.skill.get_descendants(include_self=include_root) #| self.skill_2.get_descendants(include_self=include_root)

       

    def get_participants(self):
        return self.grade.get_participants()

class Audit(BaseModel): 
    '''
    Audits are composed of skills. An audit is stereotype for a certain
    pupil evaluation.
    '''
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True, verbose_name='Beschreibung')
    assignment = models.ForeignKey(TeachingAssignment, verbose_name='Lehrauftrag')
    date = models.DateTimeField(verbose_name='Datum')
    written_exam = models.BooleanField()

    def get_all_skills(self):
        return Skill.objects.filter(auditskill__audit=self).distinct()

    def get_participants(self):
        return Pupil.objects.filter(pupilauditskill__audit=self).distinct()
    
    def get_type(self):
        if self.written_exam:
            return 'Schriftliche Lernstandserhebung'
        else:
            return 'Beobachtung'    
    
    class Meta:
        verbose_name = 'Evaluation'
        verbose_name_plural = 'Evaluationen'

    def __unicode__(self):
        return '%s:%s:%s' % (self.assignment.grade, self.assignment.subject, self.name)


class PupilAuditSkill(BaseModel):
    '''
    Represents the skill rating for a certain pupil within a certain audit.
    '''
    diagnosis = models.BooleanField()
    rating = models.IntegerField(verbose_name='Bewertung', null=True, blank=True)
    note = models.TextField(null=True, blank=True, verbose_name='Notiz')
    pupil = models.ForeignKey(Pupil, verbose_name='Schüler')
    audit = models.ForeignKey(Audit, verbose_name='Evaluation')
    skill = models.ForeignKey(Skill, verbose_name='Kompetenz')
    written_exam = models.BooleanField()

    class Meta:
        verbose_name = 'Kompetenzbewertung'
        verbose_name_plural = 'Kompetenzbewertungen'
        
    def __unicode__(self):
        return '%s:%s:%s' % (self.pupil.first_name, self.audit.name, self.skill.name )


class AuditSkill(BaseModel):
    '''
    Represents a skill within an audit.
    '''
    weight = models.IntegerField(verbose_name='Gewichtung', default=1)
    audit = models.ForeignKey(Audit, verbose_name='Evaluation')
    skill = models.ForeignKey(Skill, verbose_name='Kompetenz')

    class Meta:
        verbose_name = 'Evaluations-Kompetenz'
        verbose_name_plural = 'Evaluations-Kompetenzen'
    
    def __unicode__(self):
        return '%s:%s:%s:%s:%s' % (self.audit.assignment.grade.name, self.audit.assignment.subject.name, self.audit.name, self.skill.name, self.weight)




class PupilTAInfo(BaseModel):
    '''
    Stores a pupil description for each teaching assignment, which in fact is one description for each pupil for
    each subject for each grade.
    '''
    
    info = models.TextField(null=True, blank=True)
    pupil = models.ForeignKey(Pupil)
    teaching_assignment = models.ForeignKey(TeachingAssignment)
    written_exam_rating = models.FloatField(null=True, blank=True, default=0.0)
    
    class Meta:
        unique_together = ('pupil', 'teaching_assignment',)

try:
    mptt.register(Skill)
except mptt.AlreadyRegistered:
    pass
