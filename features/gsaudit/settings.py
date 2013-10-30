def refine_INSTALLED_APPS(original):
    return ['mptt', 'gsaudit'] + list(original)
    

def refine_MIDDLEWARE_CLASSES(original):
    return list(original) + ['gsaudit.middleware.AuthMiddleware']
    
    
    
def refine_TEMPLATE_CONTEXT_PROCESSORS(original):
    return list(original) + [
        'gsaudit.context_processors.teacher',
    ]


refine_LOGIN_URL = '/teachers/login/'

