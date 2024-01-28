"""sample tests"""

from django.test import SimpleTestCase #without database
from app import calc

class CalcTests(SimpleTestCase):

    def test_addnumbers(self):
        res=calc.add(5,6)

        self.assertEqual(res,11)

    def test_subnumbers(self):
        res=calc.subtract(10,15)

        self.assertEqual(res,5)

