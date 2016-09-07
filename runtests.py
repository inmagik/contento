#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    if len(sys.argv) == 2:
        what_to_test = 'tests/%s' % sys.argv[1]
    else:
        what_to_test = 'tests'

    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests([what_to_test])
    sys.exit(bool(failures))
