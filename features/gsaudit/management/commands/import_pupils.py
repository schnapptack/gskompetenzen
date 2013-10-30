# -*- coding: UTF-8 -*-
import random
from django.core.management.base import BaseCommand
from gsaudit.models import Pupil, Grade, GradeParticipant
from datetime import datetime

class Command(BaseCommand):
    args = '<filepath>'

    def handle(self, *args, **options):

        import codecs
        fp = codecs.open('sch2.txt', encoding='utf-8')
        
        for line in fp:
            parts = [x.strip() for x in line.split('\t')]
            
            grade_raw=parts[0]
            gender_raw=parts[5]
            gender='W'
            if gender_raw=='0':
                gender='M'
            pdata = dict(
                first_name=parts[2],
                last_name=parts[1],
                gender=gender,
                #birthday
            )
            
            grade = Grade.objects.get(name=grade_raw)
            print pdata['first_name'], pdata['last_name']
            print grade.name
            
            
            
            pupil = Pupil(**pdata)
            pupil.save()
            participation = GradeParticipant(
                pupil=pupil,
                grade=grade
            )
            participation.save()
