'''
helpers.py

like models instances of these helper classes can be passed into a template in a view e.g.
provide a special view on your data e.g. for access control.

Example:

#in views.py
from myapp import helpers
def my_view(request, obj_pk):
    x = helpers.X(obj_pk)
    return render('path/to/tmpl.html', dict(
        x=x,
    ))

Now use the x object and its funky functions in your template. 
'''

from gsaudit.models import PupilAuditSkill, TeachingAssignment
from django.db.models import Count
from django.utils.safestring import mark_safe
from django.template.loader import get_template
from django.template import Context
from django.core.urlresolvers import reverse
from copy import copy
import json

class SkillGroup(object):
    '''
    dep of PupilSkillMatrix
    '''
    def __init__(self, group):
        self.group=group
        self.skills=[]
        
    def append(self, skill):
        self.skills.append(skill)
    
    def size(self):
        return len(self.skills)
        

class SkillGroupHeadline(object):

    def __init__(self, skill):
        self.is_headline = True
        self.skill = skill        


class PupilSkillMatrix(object):
    '''
    the highly experimental Pupil x Skill x how_many_audits matrix ;)
    
    Use the source, Luke!
    '''
    
    def __init__(self, grade, subject):
        assignment = TeachingAssignment.objects.get(grade=grade, subject=subject)
        pupils = grade.get_participants()
        skills = assignment.get_all_skills()
    
        pupilauditskills = PupilAuditSkill.objects.filter(
            audit__assignment=assignment, rating__gt=0
        ).values('pupil', 'skill').annotate(num_audits=Count('id')).order_by()
    
        #create skillgroups
        self.skillgroups = []
        self.skills = []
        skill_id_to_index = dict()
        currentgroup = []#DIRTY HACK
        for skill in skills:
            if not skill.is_leaf_node():
                currentgroup = SkillGroup(skill)
                self.skillgroups.append(currentgroup)
            else:
                currentgroup.append(skill)
                skill_id_to_index[skill.id] = len(self.skills)
                self.skills.append(skill)
                
        self.pupils = []
        pupil_id_to_index = dict()
        for pupil in pupils:
            pupil.skills = []
            for orig_skill in self.skills:
                skill = copy(orig_skill)
                skill.audits = 0
                pupil.skills.append(skill)
            pupil_id_to_index[pupil.id] = len(self.pupils)
            self.pupils.append(pupil)
        
        for pupilauditskill in pupilauditskills:
            pupil = self.pupils[pupil_id_to_index[pupilauditskill['pupil']]]
            skill_index = skill_id_to_index[pupilauditskill['skill']]
            pupil.skills[skill_index].audits = pupilauditskill['num_audits']

        self.skill_array = mark_safe(','.join(["'%s'" % x.name for x in self.skills]))
        self.pupil_array = mark_safe(','.join(["'%s'" % x.get_full_name() for x in self.pupils]))
        thelist = []
        for pupil in self.pupils:
            for skill in pupil.skills:
                val = skill.audits
                thelist.append(str(val))
            
        self.data_array = mark_safe(','.join(thelist))


class SkillGraph(object):
    '''
    To visualize the progress of a pupil over time
    
    public interface:
    
    graph = SkillGraph(grade, subject, pupil)
    graph.skills             # list of skills in (grade, subject)
    skill = graph.skills[0]  # now the interface of skill
    skill.name               # skills are of type gsaudit.models.Skill
    skill.is_group           # but have special features
                             # is_group means that this skill is a skillgroup
                             # like 'Schreiben' that contains
                             # the actual skills
    skill.development        # this returns the special snippet that draws the jquery sparkline
                             #the ratings of the pupil are used as data
    
    graph.script_node        #the graph once more: returns the JS to draw all the sparklines
                             #call this once in the template
    '''
    
    script_node = mark_safe('''
    <script>
        $('.inlinesparkline').each(function() {
            var elem = $(this);
            if (!$.trim(elem.text())) {
                elem.parent.addClass('no-data-yet');
            } else {
                elem.sparkline('html', {
                    type: 'bar',
                    zeroAxis: true,
                    chartRangeMin: -2,
                    chartRangeMax: 2,
                    height:30
                    
                });
            }
        });
    </script>
    ''')

    def __init__(self, grade, subject, pupil, assignment):
        '''
        create SkillGraph of pupil of grade in subject
        
        sets up the properties
        '''
        
        self.grade = grade
        self.subject = subject
        self.assignment = assignment
        self.pupil = pupil
        _skills = self.assignment.get_all_skills()
        pupilauditskills = PupilAuditSkill.objects.filter(
            audit__assignment=assignment,
            rating__gt=0,
            pupil=pupil,
        ).exclude(written_exam=True).order_by('audit__date')

        self.skill_groups = []
        skill_id_to_skill = dict()
        
        def development_sparkline(self):
            return mark_safe('<span class="inlinesparkline">%s</span>' % (
                ','.join([str(rating - 3) for rating in self.audit_ratings]),
            ))
            
        def development_json(self):
            return json.dumps([rating - 3 for rating in self.audit_ratings])
  
            
        
        current_group = None
        for skill in _skills:
            skill.augment_skill_level_attrs(assignment)
            #FIXME use object composition instead of monkey patching here
            if skill.level == 1:
                self.skill_groups.append(SkillGroupHeadline(skill))
            if skill.level == 2:
                current_group = SkillGroup(skill)
                self.skill_groups.append(current_group)
            elif skill.level == 3:
                skill.audit_ratings = []
                skill.pupil_audits = []
                skill.development_sparkline = development_sparkline.__get__(skill, skill.__class__)
                skill.development_json = development_json.__get__(skill, skill.__class__)
                                
                current_group.skills.append(skill)
                skill_id_to_skill[skill.id] = skill
        
        #print skill_id_to_skill
        
        for elem in pupilauditskills:
            skill = skill_id_to_skill[elem.skill.id]
            skill.audit_ratings.append(elem.rating)
            skill.pupil_audits.append(elem)


class AuditCalendar(object):
    def __init__(self, audits):
        self.audits = audits

    def render(self):
        template = get_template('gsaudit/audit/calendar_helper.html')
        return template.render(Context(dict(events=self.get_as_jqfc_events(self.audits))))
    
    def get_as_jqfc_events(self, audits):
        events = []
        for audit in audits:
            events.append(dict(
                title = audit.name,
                start = audit.date.isoformat(),
                written_exam = audit.written_exam,
                url = reverse('audit-evaluate', kwargs=dict(audit_id=audit.id))
    
            ))
        return json.dumps(events)
