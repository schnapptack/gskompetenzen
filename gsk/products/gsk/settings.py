# -*- coding: utf-8 -*-
import os

BASE_PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
FILES_DIR = os.path.normpath(BASE_PROJECT_DIR + '/__data__')

refine_STATIC_ROOT = FILES_DIR + '/generated_static/'
refine_MEDIA_ROOT = FILES_DIR + '/media/'


def refine_INSTALLED_APPS(original):
    return [
        'gsk',
    ] + list(original)


refine_LANGUAGE_CODE = 'de-de'
