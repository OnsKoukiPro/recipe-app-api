"""Testing custom commands"""
import psycopg2
from unittest.mock import patch #patch is used for mocking the behaviour of simulating the db 

from psycopg2 import OperationalError as Psycopg2Error #OperationalError is example of error we might encounter when running db 

from django.core.management import call_command #call_command is helper function that simulates the command
from django.db.utils import OperationalError
from django.test import SimpleTestCase #SimpleTestCase because db is not available 


@patch('core.management.commands.wait_for_db.Command.check') #the command we're mocking - we provide the path -check is provided by the BaseCommand class
class CommandTest(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check): #patched_check object is 
        """test waiting for db if db is ready"""
        patched_check.return_value = True #when check is called  we want patched_check to return True 

        call_command('wait_for_db') #calls wait_for_db, also check that the command is correct

        patched_check.assert_called_once_with(databases=['default']) #ensures that the mocked value which is check method is called with the default db

    @patch('time.sleep') #mock the sleep function --> to not wait inside the testing
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """test waiting for database when getting OperationalError"""
        patched_check.side_effects= [Psycopg2Error] * 2 + [OperationalError] * 3 + [True] #side_effects to make it raise an Exception
        #the first 2 times (*2) we raise the Psycop2Error
        #next 3 times we raise OperationalError ( to be in synch with the Postgres process of starting the db)
        #True we get it in the sixth time 

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6) #we only call the check method 6 times 
        patched_check.assert_called_with(databases=['default'])
