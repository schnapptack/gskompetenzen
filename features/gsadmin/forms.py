# -*- coding: UTF-8 -*-
from gsaudit.models import Grade, TeachingAssignment
from gsaudit.models import Pupil,  GradeParticipant
from django import forms

class TaAdminForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(TaAdminForm, self).__init__(*args, **kwargs)
        self.fields['skill'].queryset = self.fields['skill'].queryset.filter(level=0)
        self.fields['skill'].label = 'Kompetenzbaum'
        
class GradeAdminForm(forms.ModelForm):
    
    participants = forms.ModelMultipleChoiceField(
        queryset=Pupil.objects.all(), 
        widget=forms.SelectMultiple(attrs={'class': 'chosen',}),
        label='Klassenteilnehmer'
    )
    
    class Meta:
        model = Grade
        
    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            initial = kwargs.setdefault('initial', {})
            initial['participants'] = [p.pk for p in kwargs['instance'].pupils.all()]

        forms.ModelForm.__init__(self, *args, **kwargs)
    
    def save(self, commit=True):
        # Get the unsave Pizza instance
        instance = forms.ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           # This is where we actually link the pizza with toppings
           instance.pupils.clear()
           for pupil in self.cleaned_data['participants']:
               p = GradeParticipant(pupil=pupil, grade=instance)
               p.save()                
               
        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

        return instance
    
    

class PupilAdminForm(forms.ModelForm):
    
    grades = forms.ModelMultipleChoiceField(
        queryset=Grade.objects.all(), 
        widget=forms.SelectMultiple(attrs={'class': 'chosen',}),
        label='Klassen'
    )
    class Meta:
        model = Pupil
    
    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            initial = kwargs.setdefault('initial', {})
            initial['grades'] = [p.pk for p in kwargs['instance'].grade_set.all()]
        forms.ModelForm.__init__(self, *args, **kwargs)
        
    def save(self, commit=True):
        # Get the unsave Pizza instance
        instance = forms.ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           # This is where we actually link the pizza with toppings
           instance.grade_set.clear()
           for grade in self.cleaned_data['grades']:
               p = GradeParticipant(pupil=instance, grade=grade)
               p.save()                
               
        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

        return instance
    
    
