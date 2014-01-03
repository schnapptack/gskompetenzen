from django.shortcuts import render, get_object_or_404
from gsaudit.models import Grade, Pupil, Subject, Audit, TeachingAssignment, PupilAuditSkill
from gsaudit.forms import TeachingAssignmentForm
from gsaudit import helpers
from gsaudit.models import GradeParticipant
from gsaudit.models import PupilTAInfo
from django.core.exceptions import ObjectDoesNotExist
from gsaudit.evalhelper import EvaluationHelper
from django.contrib.auth.decorators import login_required


@login_required
def index(request, subject_id=0, grade_id=0):
    '''
    Returns all data required for changing the subject within the grade browser.
    '''
   
    
    grade = get_object_or_404(Grade, id=grade_id)
    subject = get_object_or_404(Subject, id=subject_id)
    assignment = TeachingAssignment.objects.get(grade=grade, subject=subject, teacher=request.teacher)
    other_subjects = request.teacher.get_grade_subjects(grade_id)
    pupils = grade.get_participants()
    audits = Audit.objects.filter(assignment=assignment).order_by('-date')
    oral_audits = audits.filter(written_exam=False)
    written_audits = audits.filter(written_exam=True)
    pupil_skill_matrix = []
    #helpers.PupilSkillMatrix(grade, subject)
    
    pas_count = PupilAuditSkill.objects.filter(audit__assignment__grade=grade, audit__assignment=assignment).count()
    
    
    return render(request, 'gsaudit/course/index.html', 
        dict(
            grade=grade,
            subject=subject, 
            other_subjects=other_subjects,
            pupils=pupils,
            audits=audits,
            oral_audits=oral_audits,
            written_audits=written_audits,
            pupil_skill_matrix=pupil_skill_matrix,
            course_dashboard=True,
            pas_count=pas_count
        )
    )

@login_required
def overview(request, subject_id=0, grade_id=0):
    '''
    Returns all data required for changing the subject within the grade browser.
    '''
    user = request.user
    if user is None:
        return render(request, 'login/error.html')
    
    grade = get_object_or_404(Grade, id=grade_id)
    subject = get_object_or_404(Subject, id=subject_id)
    assignment = TeachingAssignment.objects.get(grade=grade, subject=subject, teacher=user)
    other_subjects = user.get_grade_subjects(grade_id)
    pupils = grade.get_participants()
    audits = Audit.objects.filter(assignment=assignment).order_by('-date')
    #pupil_skill_matrix = helpers.PupilSkillMatrix(grade, subject)

    form = TeachingAssignmentForm(request.POST or None, instance=assignment)
    if request.method == 'POST':
        if form.is_valid():
            print form
            ta = form.save(commit=False)
            print ta.note
            ta.save()
            
    
    return render(request, 'gsaudit/course/overview.html', 
        dict(
            grade=grade,
            subject=subject, 
            other_subjects=other_subjects,
            pupils=pupils,
            audits=audits,
            #pupil_skill_matrix=pupil_skill_matrix,
            form=form,
        )
    )

@login_required
def pupil_frame(request, subject_id=0, grade_id=0, pupil_id=0):

    grade = get_object_or_404(Grade, id=grade_id)
    subject = get_object_or_404(Subject, id=subject_id)
    pupil = get_object_or_404(Pupil, id=pupil_id)

    return render(request, 'gsaudit/course/pupil_frame.html', {
        'subject': subject,
        'grade': grade,        
        'pupil': pupil
    })

@login_required
def subject_statistics(request, grade_id=0, subject_id=0):
    '''
    Renders the view for the given pupil
    '''
    user = request.user
    if user is None:
        return render(request, 'login/error.html')

    grade = get_object_or_404(Grade, id=grade_id)
    subject = get_object_or_404(Subject, id=subject_id)
    assignment = TeachingAssignment.objects.get(grade=grade, subject=subject, teacher=user)
    
    grade_participants = GradeParticipant.objects.filter(grade=assignment.grade)
    subject_stats = []
    for grade_participant in grade_participants:
        eval_helper = EvaluationHelper(assignment=assignment, pupil=grade_participant.pupil)
        try:
            info = PupilTAInfo.objects.get(pupil=grade_participant.pupil, teaching_assignment=assignment)
        except ObjectDoesNotExist:
            info = PupilTAInfo(pupil=grade_participant.pupil, teaching_assignment=assignment)
            info.save()
        
        subject_stats.append({'evaluation': eval_helper, 'info': info})

    return render(request, 'gsaudit/course/subject_statistic.html', {
        'user': user, 
        'grade': grade,
        'subject': subject,
        'categories': eval_helper.categories,
        'subject_stats': subject_stats,
        'subject_statistic_view': True,
    })


