import jshook from 'jshook'

jshook.register('pages', require('./hooks/pages').default)
jshook.register('textarea-jsonschema', require('./hooks/textareaJsonschema').default)
jshook.register('content-editor', require('./hooks/contentEditor').default)

jshook.boot()
