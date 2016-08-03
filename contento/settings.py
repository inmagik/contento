"""
Overridable settings for contento cms
"""
import django.conf as conf
settings = conf.settings

DEFAULT_CONTENTO_BACKEND = 'contento.backends.files.FlatFilesBackend'
CONTENTO_BACKEND = getattr(settings, 'CONTENTO_BACKEND', DEFAULT_CONTENTO_BACKEND)

#IF used, this setting must be specified by the user.
CONTENTO_FLATFILES_BASE = getattr(settings, 'CONTENTO_FLATFILES_BASE', None)


DEFAULT_CONTENTO_TEXT_PROCESSORS = [
    'contento.processors.InternalLinks',
]

CONTENTO_TEXT_PROCESSORS = getattr(settings, 'CONTENTO_TEXT_PROCESSORS', DEFAULT_CONTENTO_TEXT_PROCESSORS)
