from django.http import HttpResponseRedirect


class AuthMiddleware(object):

    def process_request(self, request):
        
        if request.META['PATH_INFO'].startswith('/static/'):
            return None
        
        if not request.user.is_authenticated():
            if request.META['PATH_INFO'].startswith('/files/upload/'):
                return None
        else:
            if not request.user.is_staff and request.META['PATH_INFO'].startswith('/admin/'):
                return HttpResponseRedirect('/')
            
            if hasattr(request.user, 'teacher'):
                request.teacher = request.user.teacher
                request.school = request.teacher.school
            else:
                #raise Exception('User is not a teacher')
                pass

            if request.user.is_staff and not request.META['PATH_INFO'].startswith('/admin/'):
                return HttpResponseRedirect('/admin/')

        return None
