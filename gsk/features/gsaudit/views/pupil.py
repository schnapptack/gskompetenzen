from django.shortcuts import render, get_object_or_404
from gsaudit.models import Pupil, TeachingAssignment, PupilTAInfo, Grade, Subject
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import modelform_factory
from gsaudit.evalhelper import EvaluationHelper
from django.contrib.auth.decorators import login_required
from gsaudit import helpers
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

@login_required
def profile(request, pupil_id=0):
    '''
    Renders the pupil profile
    '''
   
    pupil = get_object_or_404(Pupil, id=pupil_id)

    return render(request, 'gsaudit/pupil/profile.html', {
        "pupil": pupil,
    })
    
@login_required
def pupil_ta_info(request, pupil_id, subject_id, grade_id):

    pupil = get_object_or_404(Pupil, id=pupil_id)
    ta = get_object_or_404(TeachingAssignment, subject__id=subject_id, grade__id=grade_id, teacher=request.teacher)
    
    try:
        info = PupilTAInfo.objects.get(pupil=pupil, teaching_assignment=ta)
    except ObjectDoesNotExist:
        info = PupilTAInfo(pupil=pupil, teaching_assignment=ta)
        info.save()

    formclass = modelform_factory(PupilTAInfo, fields=('info', 'written_exam_rating'))
    
    if request.method == 'POST':
        form = formclass(request.POST, instance=info)
        if form.is_valid():
            info = form.save(commit=False)
            info.pupil = pupil
            info.teaching_assignment = ta
            info.save()
            messages.success(request, 'Notiz wurde gespeichert')
            return HttpResponseRedirect(reverse('pupil-ta_info', kwargs=dict(pupil_id=pupil_id, subject_id=subject_id, grade_id=grade_id)))
    else:
        form = formclass(instance=info)
        
    return render(request, 'gsaudit/pupil/profile.html', {
        'info': info,
        'form': form,
        'grade': ta.grade,
        'subject': ta.subject,
        'pupil': pupil,
        'pupil_info_view': True
    })
    
@login_required
def pupil_eval_info(request, pupil_id, subject_id, grade_id):

    pupil = get_object_or_404(Pupil, id=pupil_id)
    ta = get_object_or_404(TeachingAssignment, subject__id=subject_id, grade__id=grade_id, teacher=request.teacher)
    eval_helper = EvaluationHelper(assignment=ta, pupil=pupil)
    try:
        info = PupilTAInfo.objects.get(pupil=pupil, teaching_assignment=ta)
    except ObjectDoesNotExist:
        info = PupilTAInfo(pupil=pupil, teaching_assignment=ta)
        info.save()
    
    return render(request, 'gsaudit/pupil/eval.html', {
        'info': info,
        'evaluation': eval_helper,
        'grade': ta.grade,
        'subject': ta.subject,
        'pupil': pupil,
        'pupil_eval_info_view': True,
    })
    
@login_required
def pupil_statistic(request, grade_id=0, subject_id=0, pupil_id=0):
    '''
    Renders the view for the given pupil
    '''

    grade = get_object_or_404(Grade, id=grade_id)
    subject = get_object_or_404(Subject, id=subject_id)
    pupil = get_object_or_404(Pupil, id=pupil_id)
    assignment = TeachingAssignment.objects.get(grade=grade, subject=subject, teacher=request.teacher)

    return render(request, 'gsaudit/pupil/stats_application.html', {
        'user': request.teacher, 
        'pupil': pupil,
        'subject': subject,
        'grade': grade,
        'skill_graph': helpers.SkillGraph(grade, subject, pupil, assignment),
        'pupil_stats_view': True,
    })

@login_required
def print_pupil_statistic(request, grade_id=0, subject_id=0, pupil_id=0):
    '''
    Renders the view for the given pupil
    '''

    grade = get_object_or_404(Grade, id=grade_id)
    subject = get_object_or_404(Subject, id=subject_id)
    pupil = get_object_or_404(Pupil, id=pupil_id)
    assignment = TeachingAssignment.objects.get(grade=grade, subject=subject, teacher=request.teacher)

    return render(request, 'gsaudit/pupil/stats_print.html', {
        'pupil': pupil,
        'subject': subject,
        'grade': grade,
        'skill_graph': helpers.SkillGraph(grade, subject, pupil, assignment),
    })

