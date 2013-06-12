# -*- coding: UTF-8 -*-
from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from django.forms.models import inlineformset_factory
from gsaudit.models import Pupil, Audit, AuditSkill, PupilAuditSkill, Skill, TeachingAssignment

def generate_form(name, fields):
    return type(name, (forms.BaseForm,), { 'base_fields': fields })


class SkillForm(ModelForm):
    
    #skill_level = forms.ChoiceField(widget=forms.CheckboxSelectMultiple, choices=(
    #    ('1', '1'),('2', '2'),('3', '3'),('4', '4'),('5', '5'),
    #))
    
    class Meta:
        model = Skill
        


class TeachingAssignmentForm(ModelForm):
    class Meta:
        model = TeachingAssignment
        fields=('note',)

class AuditForm(ModelForm):
    '''
    AuditForm to create/update Audits
    
    provides a field to select pupils
    and form inlines to create AuditSkills
    
    '''
    pupils = forms.MultipleChoiceField(
        label=u'Schüler',
        widget=forms.CheckboxSelectMultiple, 
        choices=[],
    )


    def __init__(self, *args, **kwargs):
        self.skills = kwargs.pop('skills', [])
        super(AuditForm, self).__init__(*args, **kwargs)
    
    def save(self, written_exam):
        '''
        save auditform
        
        also manages creation and deletion of PupilAuditSkill records as needed.
        '''
        
     
        audit = super(AuditForm, self).save(commit=False)
        audit.written_exam = written_exam
        audit.save()

        pupils = self.cleaned_data['pupils']
        pupil_ids = [int(pupil) for pupil in pupils]

        #clean up no longer needed PupilAuditSkills
        PupilAuditSkill.objects.filter(audit=audit).exclude(
            pupil__in=Pupil.objects.filter(id__in=pupil_ids)
        ).delete()
        PupilAuditSkill.objects.filter(audit=audit).exclude(
            skill__in=self.skills
        ).delete()

        for item in self.skills:
            skill = Skill.objects.get(id=int(item))
            AuditSkill.objects.get_or_create(audit=audit, skill=skill)
        
        AuditSkill.objects.filter(audit=audit).exclude(
            skill__in=self.skills
        ).delete()
        
        #create or update PupilAuditSkills
        for skill in self.skills:
            for pupil in pupils:
                obj, created = PupilAuditSkill.objects.get_or_create(
                    pupil=Pupil.objects.get(id=pupil),
                    audit=audit,
                    skill=Skill.objects.get(id=int(skill)),
                    written_exam=written_exam,                    
                    defaults=dict(
                        rating=0
                    ),
                )
        return audit
    
    
    def clean(self):
        if not len(self.skills):
            self.errors['skills'] = 'Es muss mindestens eine Kompetenz gewählt werden'
            raise forms.ValidationError('Wählen Sie mindestens eine Kompetenz')
        return self.cleaned_data
        
    
        
    class Meta:
        model = Audit
        exclude=('grade', 'subject', 'assignment')

def _generate_auditskill_choices(skills):
    '''
    generates options with optgroups from the skill tree of a subject
    
    pass in the skills in tree order including the root
    
    the root is omitted in the result
    skills nested deeper than 2 are not supported
    '''
    choices = []
    currentchoice = ('', '-')
    choices.append(currentchoice)
    root_id = None
    for skill in skills:
        if skill.is_root_node():
            root_id = skill.id
            continue
        if skill.parent_id == root_id:
            currentchoice = (unicode(skill), [])
            choices.append(currentchoice)
        else:
            currentchoice[1].append((skill.id, unicode(skill)))
    return choices

def get_auditskill_formset(post=None, files=None, audit=None):
    '''
    return the formset for auditskill
    '''
    AuditSkillFormSet = inlineformset_factory(Audit, AuditSkill)
    formset = AuditSkillFormSet(post, files, instance=audit)
    skills = audit.assignment.get_all_skills(include_root=True)
    choices = _generate_auditskill_choices(skills)
    for form in formset:
        form.fields["skill"].choices = choices
    empty_form = formset.empty_form
    empty_form.fields["skill"].choices = choices
    formset.default_form = empty_form
    return formset

def get_audit_form(post=None, audit=None, grade=None):
    
    skills = []
    if post:
        skills = post.getlist('selected_skills')
    
    initial = dict(
        pupils = [str(p.id) for p in audit.get_participants()],
    )
    audit_form = AuditForm(post, instance=audit, initial=initial, skills=skills)
    audit_form.fields["pupils"].choices = [
        (pupil.id, unicode(pupil)) for pupil in grade.get_participants()
    ]
    return audit_form

class HorizRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w.tag() for w in self]))

def get_audit_evaluation_form(audit):
    #audit.get_participants
    pupils = audit.get_participants()
    skills = audit.get_all_skills()
    
    evalfields = dict()
    
    for pupil in pupils:
        for skill in skills:
            evalfields['eval_%s_%s' % (pupil.id, skill.id)] = forms.ChoiceField(
                choices= [
                    ('1', '--'),
                    ('2', '-'),
                    ('3', 'o'),
                    ('4', '+'),
                    ('5', '++'),
                ],
                widget=forms.RadioSelect(renderer=HorizRadioRenderer), required=False
            )
            evalfields['eval_note_%s_%s' % (pupil.id, skill.id)] = forms.CharField(widget=forms.Textarea, required=False)
            if not audit.written_exam:
                evalfields['eval_diagnosis_%s_%s' % (pupil.id, skill.id)] = forms.BooleanField(required=False)
    
    def render(self):
        html = ['<table class="eval-form">']
        html.append('<thead><tr><th class="headcol">Kind/Kompetenz</th>')
        for skill in skills:
            skill.augment_skill_level_attrs(audit.assignment)
            html.append(u'<th class="ratings"><div class="eval-form-skill">%s</div><div class="eval-form-ratings"><span>--</span><span>-</span><span>o</span><span>+</span><span>++</span></div></th>' % (skill.skill_tag))
            
            
        html.append('</tr></thead><tbody >')
        odd = False
        for pupil in pupils:
            odd = not odd
            clz = ' class="odd" ' if odd else ''
            html.append(u'<tr%s><th>%s</th>' % (clz, pupil.get_full_name()))
            for skill in skills:
                if audit.written_exam:
                    diagnosis_field = ''
                else:
                    diagnosis_field = u'%s Diagnose' % (self['eval_diagnosis_%s_%s' % (pupil.id, skill.id)], )

                html.append(
                    u'''
                    <td >
                        <div class="skill_note">
                            <div class="skill-rating">%(checkboxes)s</div>
                            <div class="skill-tools">
                                <span class="eval-diagnosis">%(diagnosis_checkbox)s</span>
                                <a href="#" class="eval-note" data-skill-name="%(skill_name)s" data-pupil-name="%(pupil_name)s" >[Notiz]</a>
                                %(textarea)s
                            </div>
                        </div>                    
                    </td>
                    ''' % 
                    dict(
                        checkboxes=self['eval_%s_%s' % (pupil.id, skill.id)],
                        diagnosis_checkbox=diagnosis_field,
                        skill_name=skill.name,
                        pupil_name=pupil,
                        textarea=self['eval_note_%s_%s' % (pupil.id, skill.id)],
                    )
                )
            html.append('</tr>')
        
        html.append('</tbody></table>')
        return mark_safe(u''.join(html))
    
    def save(self):
        for pupil in pupils:
            for skill in skills:
                if audit.written_exam:
                    diagnosis_value = False
                else:
                    diagnosis_value = self.cleaned_data['eval_diagnosis_%s_%s' % (pupil.id, skill.id)] 
                new_rating = self.cleaned_data['eval_%s_%s' % (pupil.id, skill.id)]
                if new_rating == '':
                    new_rating = None
                    
                try:
                    obj = PupilAuditSkill.objects.get(pupil=pupil,audit=audit, skill=skill, written_exam=audit.written_exam)
                    obj.rating = new_rating
                    obj.note = self.cleaned_data['eval_note_%s_%s' % (pupil.id, skill.id)]
                    obj.written_exam = audit.written_exam
                    obj.diagnosis = diagnosis_value
                    obj.save()
                except PupilAuditSkill.DoesNotExist:
                    """
                    obj = PupilAuditSkill(
                        pupil=pupil,audit=audit, skill=skill,
                        written_exam = audit.written_exam,
                        rating = new_rating,
                        note = self.cleaned_data['eval_note_%s_%s' % (pupil.id, skill.id)],
                        diagnosis = diagnosis_value,
                    )
                    obj.save()                    
                    """
                        
                    
    
    def get_initial_data():
        initial = dict()
        for pupil in pupils:
            for skill in skills:
                obj, created = PupilAuditSkill.objects.get_or_create(
                    pupil=pupil,
                    audit=audit,
                    skill=skill,
                    written_exam = audit.written_exam,
                    defaults=dict(
                        rating=0
                    ),
                )
                if not created:
                    initial['eval_%s_%s' % (pupil.id, skill.id)] = obj.rating
                    initial['eval_note_%s_%s' % (pupil.id, skill.id)] = obj.note
                    initial['eval_diagnosis_%s_%s' % (pupil.id, skill.id)] = obj.diagnosis
        return initial
        
    eval_form = generate_form('EvaluationForm', fields=evalfields)
    eval_form.render = render
    eval_form.save = save
    eval_form.get_initial_data = staticmethod(get_initial_data)
    
    return eval_form
    
