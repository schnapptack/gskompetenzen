
def refine_get_urls(original):

    def get_urls():
        from django.conf.urls.defaults import url, patterns, include
        
        urlpatterns = patterns('gsadmin',
            url(r'^admin/gsaudit/skilltrees/$', 'views.skilltrees', name='gsadmin-skilltrees'),
            url(r'^admin/gsaudit/skilltree/(?P<id>\d+)$', 'views.skilltree', name='gsadmin-skilltree'),
        )
        
        
        return urlpatterns + original()
    return get_urls

