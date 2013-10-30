
def refine_get_urls(original):

    def get_urls():
        from django.conf.urls.defaults import url, patterns, include
        urlpatterns = patterns('gsaudit.views',
            url(r'^$', 'dashboard.index'),
            url(r'^myaccount/$', 'dashboard.myaccount', name='myaccount'),
            url(r'^course/(?P<grade_id>\d+)_(?P<subject_id>\d+)/$', 'course.index', name='course-index'),
            url(r'^course/overview/(?P<grade_id>\d+)_(?P<subject_id>\d+)/$', 'course.overview', name='course-overview'),
            url(r'^course/subject_statistics/(?P<grade_id>\d+)_(?P<subject_id>\d+)/$', 'course.subject_statistics', name='course-subject_statistics'),
             url(r'^course/(?P<grade_id>\d+)_(?P<subject_id>\d+)/pupil/(?P<pupil_id>\d+)/$', 'course.pupil_frame', name='course-pupil_frame'),

            url(r'^pupil/profile/(?P<pupil_id>\d+)/$', 'pupil.profile', name='pupil-profile'),
            url(r'^pupil/ta_info/(?P<pupil_id>\d+)/(?P<subject_id>\d+)/(?P<grade_id>\d+)/$', 'pupil.pupil_ta_info', name='pupil-ta_info'),
            url(r'^pupil/eval_info/(?P<pupil_id>\d+)/(?P<subject_id>\d+)/(?P<grade_id>\d+)/$', 'pupil.pupil_eval_info', name='pupil-eval_info'),
            url(r'^pupil/statistic/(?P<grade_id>\d+)_(?P<subject_id>\d+)/pupil/(?P<pupil_id>\d+)/$', 'pupil.pupil_statistic', name='pupil-statistic'),
            url(r'^pupil/print_statistic/(?P<grade_id>\d+)_(?P<subject_id>\d+)/pupil/(?P<pupil_id>\d+)/$', 'pupil.print_pupil_statistic', name='pupil-print_statistic'),
          
        
            
            url(r'^audit/evaluate/(?P<audit_id>\d+)/$', 'audit.evaluate', name='audit-evaluate'),
            url(r'^audit/manage/course/(?P<grade_id>\d+)_(?P<subject_id>\d+)/$', 'audit.manage', name='audit-manage'),
            url(r'^audit/manage/(?P<audit_id>\d+)/course/(?P<grade_id>\d+)_(?P<subject_id>\d+)/$', 'audit.manage', name='audit-manage'),
            url(r'^audit/listing/course/(?P<grade_id>\d+)_(?P<subject_id>\d+)/$', 'audit.listing', name='audit-listing'),
            url(r'^audit/calendar_listing/course/(?P<grade_id>\d+)_(?P<subject_id>\d+)/$', 'audit.calendar_listing', name='audit-calendar_listing'),
            url(r'^audit/delete/(?P<audit_id>\d+)/$', 'audit.delete', name='audit-delete'),

            url(r'^exam/manage/course/(?P<grade_id>\d+)_(?P<subject_id>\d+)/$', 'audit.manage', {'written_exam': True}, name='exam-manage'),
            url(r'^exam/manage/(?P<audit_id>\d+)/course/(?P<grade_id>\d+)_(?P<subject_id>\d+)/$', 'audit.manage', {'written_exam': True}, name='exam-manage'),
            # direct_to_template was removed in django 1.5
            #url(r'^about/$', direct_to_template, {'template': 'gsaudit/about.html'}, name='about'),
        )
        
        from users import authurls
        from gsaudit.models import Teacher
        urlpatterns += authurls.get_patterns(Teacher)
        return urlpatterns + original()
    return get_urls



