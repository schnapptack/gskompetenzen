# -*- coding: UTF-8 -*-
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from users.admin import UserAdmin
from gsaudit.models import Grade, TeachingAssignment, Pupil, Skill, Teacher,School
from gsadmin.forms import TaAdminForm, GradeAdminForm, PupilAdminForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class TaAdmin(admin.StackedInline):
    model = TeachingAssignment 
    extra = 0
    form = TaAdminForm
    fieldsets = [
         (None, {
            'fields':  ('teacher', 'subject', 'skill', 'min_skill_level', 'max_skill_level'),
            #'description': 'Fügen Sie einen Lehrer für ein bestimmtes Fach dieser Klasse hinzu'
        }),
    ]
    
    
class GradeAdmin(admin.ModelAdmin):
    model = Grade
    inlines = [TaAdmin]
    form = GradeAdminForm
    fields = ['name', 'school', 'participants']    
    

   

# ------------------------------------------------------------------


class PupilAdmin(admin.ModelAdmin):
    
    form = PupilAdminForm
    model = Pupil
    
    fields = ['first_name', 'last_name', 'gender', 'grades', 'school', 'note']



# ------------------------------------------------------------------


class SkillAdmin(MPTTModelAdmin):
    model = Skill
    
    exclude = ['author']
    fieldsets = [
        (None, {
            'fields':  ('name', 'parent', ),
        }),
        ('Beschreibung', {
            'fields':  ('description', 'pupil_description', ),
        }),
        ('Eignung', {
            'fields':  (('min_skill_level', 'max_skill_level',), ),
        }),
        ('Erweitert', {
            'fields':  ('weight', ),
            'classes': ['collapse'],
        }),
    ]
    
    def get_form(self, request, obj=None, **kwargs):
        f = MPTTModelAdmin.get_form(self, request, obj, **kwargs)
        
        if obj:
            qs = obj.get_root().get_descendants(include_self=True)
        else:
            root_node = self._get_root(request)
            if root_node:
                qs = root_node.get_descendants(include_self=True)
            else:
                qs = Skill.objects.none()
        
        class NewForm(f):
            def __init__(self, *args, **kwargs):
                f.__init__(self, *args, **kwargs)
                self.fields['parent'].queryset =qs
                
        return NewForm
    
    def save_model(self, request, obj, form, change):
        obj.author = request.teacher
        obj.save()
        return obj
    
    
    def _get_root(self, request):
        
        try:
            return Skill.objects.get(id=request.GET.get('root_id', False), parent=None)
        except Skill.DoesNotExist:
            return None
        
        
    def add_view(self, request, form_url='', extra_context=None):
        
        root_node = self._get_root(request)
        
        extra_context = extra_context or {}
        extra_context.update({
            'root_node': root_node
        })
        return MPTTModelAdmin.add_view(self, request, form_url, extra_context=extra_context)


    def response_change(self, request, obj, *args, **kwargs):
         
        if request.POST.has_key('_save'):
            return HttpResponseRedirect(reverse('gsadmin-skilltree', args=[obj.get_root().id]))
        elif request.POST.has_key('_continue'):
            return HttpResponseRedirect(reverse('admin:gsaudit_skill_change', args=[obj.id]))
        elif request.POST.has_key('_addanother'):
            return HttpResponseRedirect(reverse('admin:gsaudit_skill_add') + '?root_id=%s' % obj.get_root().id)

        return super(SkillAdmin, self).response_change(
            request, obj, *args, **kwargs
        )

    
# ------------------------------------------------------------------


class TeacherAdmin(UserAdmin):
    fieldsets = [
         ('main', {
            'fields':  ('gender', 'first_name', 'last_name', 'email', 'school', 'username', 'is_active')
        }),
    ]


    
admin.site.register(School)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Pupil, PupilAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Teacher, TeacherAdmin)



