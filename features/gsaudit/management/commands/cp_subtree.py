# -*- coding: UTF-8 -*-
import random
from django.core.management.base import BaseCommand
from gsaudit.models import Skill
from datetime import datetime

class Command(BaseCommand):
    args = '<src>, <target>'

    def handle(self, *args, **options):

        src = Skill.objects.get(id=int(args[0]))
        target = Skill.objects.get(id=int(args[1]))
        
        new = self.cp_node(src, target)
        new.save()
        
        self.copy(src, new)
        
        
    
    def copy(self, src, target):
        
        for old in src.get_children():
            new = self.cp_node(old, target)
            new.save()
            self.copy(old, new)
            
    def cp_node(self, a, target):
        new = Skill(
            parent=target,
            name=a.name, 
            description=a.description,
            pupil_description=a.pupil_description,
            weight=a.weight,
            min_skill_level=a.min_skill_level, 
            max_skill_level=a.max_skill_level,
            author=a.author,
        )
            
        return new
            
            
            
        
