import time
import pandas as pd
from django.conf import settings
from traceback import print_exc
from logging import basicConfig, DEBUG, debug
from django.http import JsonResponse
from rest_framework.status import HTTP_400_BAD_REQUEST

def handle_error(error):
    # TODO: Send these errors to sentry
    basicConfig(format='%(levelname)s: %(message)s', level=DEBUG)
    print()
    debug(f'An exception has ocurred: {str(error)}')
    print()
    print_exc()
    return JsonResponse(data={'message': 'Something went wrong', 'code': HTTP_400_BAD_REQUEST, 'status': 'error', 'error': str(error)}, status=HTTP_400_BAD_REQUEST)