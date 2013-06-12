# -*- coding: UTF-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from gsaudit.models import Skill
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def skilltrees(request):
    skilltrees = Skill.objects.filter(level=0)
    return render(request, 'admin/gsaudit/skilltrees.html', dict(
        skilltrees=skilltrees
    ))
    


@login_required
def skilltree(request, id):
    skilltree = get_object_or_404(Skill, id=id, level=0)
    return render(request, 'admin/gsaudit/skilltree.html', dict(
        skilltree=skilltree
    ))
