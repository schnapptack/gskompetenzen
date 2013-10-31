from gsaudit.models import School


def teacher(request):

    if hasattr(request, 'teacher') and hasattr(request, 'school'):
        return {
            'teacher': request.teacher,
            'school': request.school,
        }
    else:
        return {}
    
    
