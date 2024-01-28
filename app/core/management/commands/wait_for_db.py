#management command --> to wait for db 
#to create a management command you need a management folder with init and commands folder with init and files for desired commands

"""Django command to wait for db to be available """
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand 

class Command(BaseCommand):
    """Django command to wait for db"""
    def handle(self, *args, **options):
       # pass #structure  to create a command
        self.stdout.write('Waiting for db...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True 
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('db unavailable..waiting 2 sec..')
                time.sleep(2)

        self.stdout.write(self.style.SUCCESS('db available'))
