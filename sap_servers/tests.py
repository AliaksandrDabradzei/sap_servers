"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

# import inspect
# import sap_servers.models
# 
# for name, obj in inspect.getmembers(sap_servers.models):
#     if inspect.isclass(obj):
#         print obj
#     
# print sap_servers.models.OS.text
import re
X = 'SAP R/3 Release 4.6C'
print X
x = re.search('\d(?<!R/3).*', X)#.group(0)
print x.group()
print X[:x.start()]
#print x.group(0)


# objs = ["SAP BOE 4.0, SAP R/3 Release 4.6C, Data Services 4.0, Inf.Steward 4.0"]
# for obj1 in objs:
#         obj1 = obj1.strip().split(',')
#         for obj in obj1:
#             obj = obj.strip()
#             print obj
#             x = re.search("\d", obj[obj.find("R/3")+3:])
#             print obj[obj.find("R/3")+3:][x.start():]
            #x = re.search("(?<='\d')\s+", obj)
            #print obj[obj.find("R/3")+3:]
            #x = re.search("\d", obj[obj.find("R/3")+3:])
            #print x.group(0)
#             if x:
#                 print x.group(0)
#             else:
#                 print

