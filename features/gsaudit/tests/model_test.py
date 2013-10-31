import unittest
from gsaudit.models import School,Teacher,Grade,Pupil,Skill
from datetime import datetime
from admintests.mixins import AdminTestMixin
class GSAuditAdminTests(AdminTestMixin,unittest.TestCase):
    models = [School,Teacher,Grade,Pupil,Skill]
    
    
    def create_objects(self):
        test_school = School(name="Test_School",domain="something",address="something",contact_person="someone")
        test_school.save()
        self.register(School,test_school)
        
        test_teacher = Teacher(gender='m',phone="123123123",school=test_school)
        test_teacher.save()
        self.register(Teacher,test_teacher)
        
        test_grade = Grade(name="test_Grade",school=test_school)
        test_grade.save()
        self.register(Grade,test_grade)

        test_pupil = Pupil(first_name="Markus",last_name="Mueller",gender='m',birthday=datetime.now(),school=test_school)
        test_pupil.save()
        self.register(Pupil,test_pupil)
        
        test_skill = Skill(name="test_skill",weight=0)
        test_skill.save()
        self.register(Skill,test_skill)                
        

        
        
        
        







