from gsaudit.models import PupilAuditSkill, Audit, TeachingAssignment, PupilTAInfo
from django.db.models import Count
from django.utils.safestring import mark_safe
from django.template.loader import get_template
from django.template import Context
from django.core.urlresolvers import reverse
from copy import copy
import json


class SkillCategoryWrapper(object):

    def __init__(self, skill):
        self.cat = skill
        self._groups = []
        self._avg = None
    
    @property
    def avg(self):
        if not self._avg:
            avg = 0
            count = 0
            for item in self.groups:
                item_avg = item.avg
                if item_avg != -1:
                    count += 1
                    avg += item_avg
            if count:
                self._avg = avg / count
            else:
                self._avg = -1
            
        return self._avg

    @property
    def groups(self):
        return self._groups

class SkillGroupWrapper(object):
    
    def __init__(self, skill):
        self.group = skill
        self._skills = []
        self._avg = None
    
    @property
    def avg(self):
        try:
            if not self._avg:
                avg = 0
                count = 0
                for item in self.skills:
                    item_avg = item.avg
                    if item_avg != -1:
                        count += 1
                        avg += item_avg
                if count:
                    self._avg = avg / count
                else:
                    self._avg = -1
            return self._avg
        except:
            import traceback
            traceback.print_exc()
    @property
    def skills(self):
        return self._skills

class SkillWrapper(object):

    def __init__(self, skill, assignment, pupil):
        self.skill = skill
        self.assignment = assignment
        self.pupil = pupil
        
        self._num_audits = None
        self._num_diagnostic_audits = None
        self._avg = None
        self._initialized = False

    def _calculate(self):
        pags = PupilAuditSkill.objects.filter(
            skill=self.skill,
            audit__assignment=self.assignment,
            pupil=self.pupil,
            rating__gt=0,
        ).exclude(written_exam=True)
        total = 0.0
        count = 0
        dia_count = 0
        for pag in pags:
            
            if pag.diagnosis:
                dia_count += 1
            else:
                count += 1
                #narf 5 is ++ and 1 is --
                total += (6 - pag.rating)

        if count == 0:
            self._avg = -1
        else:
            self._avg = total / count
        self.num_audits = count
        self.num_diagnostic_audits = dia_count
        self._initialized = True

    @property
    def avg(self):
        try:
            if not self._initialized:
                self._calculate()
            return self._avg
        except:
            import traceback
            traceback.print_exc()

class ExamWrapper(object):
    
    def __init__(self, audit, pupil):
        self.audit=audit
        self.pupil=pupil
        self._calculate()
        
    def _calculate(self):
        pags = PupilAuditSkill.objects.filter(
            audit=self.audit,
            pupil=self.pupil,
            rating__gt=0,
            written_exam=True
        )
        total = 0.0
        count = 0
        for pag in pags:
            count += 1
            #narf 5 is ++ and 1 is --
            total += (6 - pag.rating)

        if count == 0:
            self._avg = -1
        else:
            self._avg = total / count
    
    @property
    def avg(self):
        return self._avg

class EvaluationHelper(object):
    
    def __init__(self, assignment, pupil):
        self.info, created = PupilTAInfo.objects.get_or_create(teaching_assignment=assignment, pupil=pupil)
        self.assignment=assignment
        self.pupil=pupil
        
        self._categories = None
        self._avg = None
        self._exams = None
        self.remaining_weight = 0
        self._calculate()
    
    def _calculate(self):
        if not self._avg:
            avg = 0
            weighted_avg = 0
            count = 0
            weighted_valid = True
            total_weight = 0
            for item in self.categories:
            
                item_avg = item.avg
                total_weight += item.cat.weight
                if item_avg != -1:
                    count += 1
                    avg += item_avg
                    weighted_avg += item_avg * item.cat.weight
                    
                else:
                    weighted_valid = False
            
            self._avg = -1
            self.weighted_avg = -1
            self.skills_total_weight = total_weight
            self.remaining_weight = 100 - self.skills_total_weight
            
            if count:
                #self._avg = avg / count
                if weighted_valid:
                    self._avg = weighted_avg / total_weight
                    
                    self.skills_weighted_abs = weighted_avg
            #else:
            #    self.skills_weighted_abs = 0

    @property
    def skill_rating(self):
        return self._avg
    
    @property
    def written_exams(self):
        if not self._exams:
            exams = []
            audits = Audit.objects.filter(
                assignment=self.assignment,
                written_exam=True
            ).order_by('date')
            
            for audit in audits:
                exams.append(ExamWrapper(audit, self.pupil))
            
            self._exams = exams
        return self._exams
    
    @property
    def written_exams_rating(self):
        try:
            avg = 0
            count = 0
            for item in self.written_exams:
                item_avg = item.avg
                if item_avg != -1:
                    count += 1
                    avg += item_avg
            if count:
                self._avg = avg / count
            else:
                self._avg = -1
                
            return self._avg
        except:
            import traceback
            traceback.print_exc()
            
    @property
    def total_rating(self):
        wer = self.written_exams_rating
        if self._avg and self._avg != -1 and hasattr(self, "skills_weighted_abs"):
            return (self.skills_weighted_abs + wer * self.remaining_weight) / 100
        else:
            return -1
    
    @property
    def categories(self):
        if not self._categories:
            
            self._categories = []
            _cat = None
            _group = None
            _skill = None
            for item in self.assignment.get_all_skills():
                if item.level == 1:
                    _cat = SkillCategoryWrapper(item)
                    self._categories.append(_cat)
                if item.level == 2:
                    _group = SkillGroupWrapper(item)
                    _cat._groups.append(_group)
                if item.level == 3:
                    _skill = SkillWrapper(item, self.assignment, self.pupil)
                    _group._skills.append(_skill)
                
        return self._categories
