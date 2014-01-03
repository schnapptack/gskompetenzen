def refine_INSTALLED_APPS(original):
    return ['mptt', 'gsaudit'] + list(original)
    

def refine_MIDDLEWARE_CLASSES(original):
    return list(original) + ['gsaudit.middleware.AuthMiddleware']
    
    
    
def refine_TEMPLATE_CONTEXT_PROCESSORS(original):
    return list(original) + [
        'gsaudit.context_processors.teacher',
    ]



refine_LOGIN_URL = '/login/'
refine_LOGIN_REDIRECT_URL = '/'
refine_LOGOUT_REDIRECT_URL = '/login/'


refine_LANGUAGE_CODE = 'de-de'

