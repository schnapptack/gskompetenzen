from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gsaudit.models import TeachingAssignment, PupilAuditSkill

@login_required
def index(request):
    '''
    Renders the the dashboard view presenting an overview of all classes of the 
    current teacher.
    '''
    activity = PupilAuditSkill.objects.filter(audit__assignment__id__in=TeachingAssignment.objects.filter(teacher=request.teacher).values_list('id', flat=True)).count()
        
    return render(request, 'gsaudit/dashboard/index.html', {
        "teaching_assignments": TeachingAssignment.objects.filter(teacher=request.teacher),
        'activity_index': activity
    })
    

@login_required
def myaccount(request):
    '''
    Renders the the dashboard view presenting an overview of all classes of the 
    current teacher.
    '''
        
    return render(request, 'gsaudit/dashboard/myaccount.html', {
    })
