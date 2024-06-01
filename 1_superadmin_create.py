
import os
import json
import sys
import traceback
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_net_backend.settings')

import django
django.setup()

from social_app.models import *
from django.db import transaction

if __name__ == '__main__':
    print ('Starting execution...')
    try:
        with transaction.atomic():
            email='admin@gmail.com'
            username='superadmin'
            password='admin@123'
     
            superadmin = CustomUser(
                username=username,
                email=email,
                is_superuser=True,
                is_staff=True)
            superadmin.set_password(password)
            # superadmin.full_clean()
            superadmin.save()

            print ('Completed execution...')



    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)
