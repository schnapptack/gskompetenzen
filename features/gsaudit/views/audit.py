# -*- coding: UTF-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from gsaudit.models import Grade, Subject, Audit, TeachingAssignment, AuditSkill, Skill
from gsaudit.forms import get_audit_form, get_auditskill_formset, get_audit_evaluation_form
from gsaudit import helpers
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def augment_skills(skills, audit, assignment):
    for skill in skills:
        skill.augment_skill_level_attrs(assignment)
        try:
            auditskill = AuditSkill.objects.get(skill=skill, audit=audit)
            sel = 'checked="checked"'
        except ObjectDoesNotExist:
            sel = ''
        skill.selected = sel
        yield skill
        
        

@login_required
def manage(request, audit_id=0, grade_id=0, subject_id=0, written_exam=False):
    '''
    shows the form to create/edit an audit
    '''
    subject = get_object_or_404(Subject, pk=subject_id)
    grade = get_object_or_404(Grade, pk=grade_id)
    assignment = TeachingAssignment.objects.get(grade=grade, subject=subject, teacher=request.user)
    try:
        audit = Audit.objects.get(pk=audit_id)
        edit_mode = True
    except Audit.DoesNotExist:
        #print written_exam, 28828282
        audit = Audit(assignment=assignment, written_exam=written_exam)
        edit_mode = False

    if request.method == "POST":
        #print audit.written_exam, 999
        auditform = get_audit_form(request.POST, audit=audit, grade=grade)
        #print audit.written_exam, 999
        if auditform.is_valid():
            # TODO: here audit_form.written_exam seems to be false, changed by is_valid() call???
            #print audit, audit.written_exam, written_exam
            audit = auditform.save(written_exam=written_exam)
            
            if edit_mode:
                msg = 'Beobachtung wurde gespeichert'
            else:
                msg = 'Beobachtung wurde angelegt'
            messages.success(request, msg)
            return HttpResponseRedirect(reverse('audit-evaluate', kwargs=dict(audit_id=audit.id)))
    else:
        auditform = get_audit_form(audit=audit, grade=grade)
        
    try:
        skills = augment_skills(assignment.skill.get_descendants(), audit, assignment)
    except ObjectDoesNotExist:
        subject_node = None
        skills = []

    if audit.written_exam:
        post_url = reverse('exam-manage', kwargs=dict(audit_id=audit_id, grade_id=grade.id, subject_id=subject.id))
    else:
        post_url = reverse('audit-manage', kwargs=dict(audit_id=audit_id, grade_id=grade.id, subject_id=subject.id))
        
    return render(request, 'gsaudit/audit/manage.html', dict(
        post_url=post_url,
        auditform=auditform,
        edit_mode=edit_mode,
        grade=grade,
        subject=subject,
        audit=audit,
        skills = skills,
        written_exam = written_exam,
        audit_view=True,
        create=not (audit.id or False)
    ))


@login_required
def delete(request, audit_id=0):
    
    audit = get_object_or_404(Audit, pk=audit_id)
    grade_id = audit.assignment.grade.id
    subject_id = audit.assignment.subject.id
    
    if request.method == 'POST':
        audit.delete()
        messages.success(request, 'Beobachtung wurde gelöscht')
        return HttpResponseRedirect(reverse('audit-listing', kwargs=dict(grade_id=grade_id, subject_id=subject_id)))
    else:
        return render(
            request, 
            'gsaudit/audit/delete.html', 
            dict(audit=audit, grade=audit.assignment.grade, subject=audit.assignment.subject)
        )
        
    
    
    
@login_required
def evaluate(request, audit_id=0):
    audit = get_object_or_404(Audit, pk=audit_id)
    
    EvaluationForm = get_audit_evaluation_form(audit)
    if request.method == 'POST':
        eval_form = EvaluationForm(request.POST)
        if eval_form.is_valid():
            eval_form.save()
            messages.success(request, 'Evaluation wurde gespreichert')
            return HttpResponseRedirect(reverse('audit-evaluate', kwargs=dict(audit_id=audit.id)))
    else:
        eval_form = EvaluationForm(EvaluationForm.get_initial_data())
    
    eval_form.render()
    return render(
        request,
        "gsaudit/audit/evaluate.html",
        dict(
            eval_form=eval_form,
            audit=audit,
            subject=audit.assignment.subject,
            grade=audit.assignment.grade,
            audit_view=True
        ),
    )


@login_required
def listing(request, grade_id=0, subject_id=0):
    subject = get_object_or_404(Subject, pk=subject_id)
    grade = get_object_or_404(Grade, pk=grade_id)
    assignment = TeachingAssignment.objects.get(grade=grade, subject=subject, teacher=request.user)
    audits = Audit.objects.filter(assignment=assignment).order_by('-date').distinct()

    return render(
        request,
        "gsaudit/audit/listing.html",
        dict(
            audits=audits,
            grade=grade,
            subject=subject,
            listing_view=True,
            audit_view=True,
        )
    )

@login_required
def calendar_listing(request, grade_id=0, subject_id=0):
    subject = get_object_or_404(Subject, pk=subject_id)
    grade = get_object_or_404(Grade, pk=grade_id)
    assignment = TeachingAssignment.objects.get(grade=grade, subject=subject, teacher=request.user)
    audits = Audit.objects.filter(assignment=assignment).order_by('-date')

    return render(
        request,
        "gsaudit/audit/calendar_listing.html",
        dict(
            audits = audits,
            grade = grade,
            subject = subject,
            calendar = helpers.AuditCalendar(audits),
            calendar_listing_view=True,
            audit_view = True,
        )
    )
