from contento.settings import CONTENTO_BACKEND
from django.utils.module_loading import import_string

def get_current_backend():
    cms_backend = import_string(CONTENTO_BACKEND)()
    return cms_backend
