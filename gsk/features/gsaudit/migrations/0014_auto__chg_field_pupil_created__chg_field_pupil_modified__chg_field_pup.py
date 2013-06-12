# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Pupil.created'
        db.alter_column(u'gsaudit_pupil', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'Pupil.modified'
        db.alter_column(u'gsaudit_pupil', 'modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'Pupil.jsondata'
        db.alter_column(u'gsaudit_pupil', 'jsondata', self.gf('jsonfield.fields.JSONField')())

        # Changing field 'AuditSkill.created'
        db.alter_column(u'gsaudit_auditskill', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'AuditSkill.modified'
        db.alter_column(u'gsaudit_auditskill', 'modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'AuditSkill.jsondata'
        db.alter_column(u'gsaudit_auditskill', 'jsondata', self.gf('jsonfield.fields.JSONField')())

        # Changing field 'PupilTAInfo.created'
        db.alter_column(u'gsaudit_pupiltainfo', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'PupilTAInfo.modified'
        db.alter_column(u'gsaudit_pupiltainfo', 'modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'PupilTAInfo.jsondata'
        db.alter_column(u'gsaudit_pupiltainfo', 'jsondata', self.gf('jsonfield.fields.JSONField')())

        # Changing field 'TeachingAssignment.created'
        db.alter_column(u'gsaudit_teachingassignment', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'TeachingAssignment.modified'
        db.alter_column(u'gsaudit_teachingassignment', 'modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'TeachingAssignment.jsondata'
        db.alter_column(u'gsaudit_teachingassignment', 'jsondata', self.gf('jsonfield.fields.JSONField')())

        # Changing field 'Grade.created'
        db.alter_column(u'gsaudit_grade', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'Grade.modified'
        db.alter_column(u'gsaudit_grade', 'modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'Grade.jsondata'
        db.alter_column(u'gsaudit_grade', 'jsondata', self.gf('jsonfield.fields.JSONField')())

        # Changing field 'PupilAuditSkill.created'
        db.alter_column(u'gsaudit_pupilauditskill', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'PupilAuditSkill.jsondata'
        db.alter_column(u'gsaudit_pupilauditskill', 'jsondata', self.gf('jsonfield.fields.JSONField')())

        # Changing field 'PupilAuditSkill.modified'
        db.alter_column(u'gsaudit_pupilauditskill', 'modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'Audit.created'
        db.alter_column(u'gsaudit_audit', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'Audit.jsondata'
        db.alter_column(u'gsaudit_audit', 'jsondata', self.gf('jsonfield.fields.JSONField')())

        # Changing field 'Audit.modified'
        db.alter_column(u'gsaudit_audit', 'modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'School.modified'
        db.alter_column(u'gsaudit_school', 'modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'School.created'
        db.alter_column(u'gsaudit_school', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'School.jsondata'
        db.alter_column(u'gsaudit_school', 'jsondata', self.gf('jsonfield.fields.JSONField')())

        # Changing field 'Skill.created'
        db.alter_column(u'gsaudit_skill', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'Skill.modified'
        db.alter_column(u'gsaudit_skill', 'modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'Skill.jsondata'
        db.alter_column(u'gsaudit_skill', 'jsondata', self.gf('jsonfield.fields.JSONField')())
        # Deleting field 'Teacher.phone'
        db.delete_column(u'gsaudit_teacher', 'phone')


        # Changing field 'Subject.modified'
        db.alter_column(u'gsaudit_subject', 'modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'Subject.created'
        db.alter_column(u'gsaudit_subject', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'Subject.jsondata'
        db.alter_column(u'gsaudit_subject', 'jsondata', self.gf('jsonfield.fields.JSONField')())

        # Changing field 'GradeParticipant.created'
        db.alter_column(u'gsaudit_gradeparticipant', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'GradeParticipant.modified'
        db.alter_column(u'gsaudit_gradeparticipant', 'modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'GradeParticipant.jsondata'
        db.alter_column(u'gsaudit_gradeparticipant', 'jsondata', self.gf('jsonfield.fields.JSONField')())

    def backwards(self, orm):

        # Changing field 'Pupil.created'
        db.alter_column(u'gsaudit_pupil', 'created', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Pupil.modified'
        db.alter_column(u'gsaudit_pupil', 'modified', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Pupil.jsondata'
        db.alter_column(u'gsaudit_pupil', 'jsondata', self.gf('jsonfield.JSONField')())

        # Changing field 'AuditSkill.created'
        db.alter_column(u'gsaudit_auditskill', 'created', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'AuditSkill.modified'
        db.alter_column(u'gsaudit_auditskill', 'modified', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'AuditSkill.jsondata'
        db.alter_column(u'gsaudit_auditskill', 'jsondata', self.gf('jsonfield.JSONField')())

        # Changing field 'PupilTAInfo.created'
        db.alter_column(u'gsaudit_pupiltainfo', 'created', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'PupilTAInfo.modified'
        db.alter_column(u'gsaudit_pupiltainfo', 'modified', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'PupilTAInfo.jsondata'
        db.alter_column(u'gsaudit_pupiltainfo', 'jsondata', self.gf('jsonfield.JSONField')())

        # Changing field 'TeachingAssignment.created'
        db.alter_column(u'gsaudit_teachingassignment', 'created', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'TeachingAssignment.modified'
        db.alter_column(u'gsaudit_teachingassignment', 'modified', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'TeachingAssignment.jsondata'
        db.alter_column(u'gsaudit_teachingassignment', 'jsondata', self.gf('jsonfield.JSONField')())

        # Changing field 'Grade.created'
        db.alter_column(u'gsaudit_grade', 'created', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Grade.modified'
        db.alter_column(u'gsaudit_grade', 'modified', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Grade.jsondata'
        db.alter_column(u'gsaudit_grade', 'jsondata', self.gf('jsonfield.JSONField')())

        # Changing field 'PupilAuditSkill.created'
        db.alter_column(u'gsaudit_pupilauditskill', 'created', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'PupilAuditSkill.jsondata'
        db.alter_column(u'gsaudit_pupilauditskill', 'jsondata', self.gf('jsonfield.JSONField')())

        # Changing field 'PupilAuditSkill.modified'
        db.alter_column(u'gsaudit_pupilauditskill', 'modified', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Audit.created'
        db.alter_column(u'gsaudit_audit', 'created', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Audit.jsondata'
        db.alter_column(u'gsaudit_audit', 'jsondata', self.gf('jsonfield.JSONField')())

        # Changing field 'Audit.modified'
        db.alter_column(u'gsaudit_audit', 'modified', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'School.modified'
        db.alter_column(u'gsaudit_school', 'modified', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'School.created'
        db.alter_column(u'gsaudit_school', 'created', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'School.jsondata'
        db.alter_column(u'gsaudit_school', 'jsondata', self.gf('jsonfield.JSONField')())

        # Changing field 'Skill.created'
        db.alter_column(u'gsaudit_skill', 'created', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Skill.modified'
        db.alter_column(u'gsaudit_skill', 'modified', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Skill.jsondata'
        db.alter_column(u'gsaudit_skill', 'jsondata', self.gf('jsonfield.JSONField')())
        # Adding field 'Teacher.phone'
        db.add_column(u'gsaudit_teacher', 'phone',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Subject.modified'
        db.alter_column(u'gsaudit_subject', 'modified', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Subject.created'
        db.alter_column(u'gsaudit_subject', 'created', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Subject.jsondata'
        db.alter_column(u'gsaudit_subject', 'jsondata', self.gf('jsonfield.JSONField')())

        # Changing field 'GradeParticipant.created'
        db.alter_column(u'gsaudit_gradeparticipant', 'created', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'GradeParticipant.modified'
        db.alter_column(u'gsaudit_gradeparticipant', 'modified', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'GradeParticipant.jsondata'
        db.alter_column(u'gsaudit_gradeparticipant', 'jsondata', self.gf('jsonfield.JSONField')())

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'gsaudit.audit': {
            'Meta': {'object_name': 'Audit'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gsaudit.TeachingAssignment']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jsondata': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'written_exam': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'gsaudit.auditskill': {
            'Meta': {'object_name': 'AuditSkill'},
            'audit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gsaudit.Audit']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jsondata': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gsaudit.Skill']"}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'gsaudit.grade': {
            'Meta': {'object_name': 'Grade'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jsondata': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gsaudit.School']"})
        },
        u'gsaudit.gradeparticipant': {
            'Meta': {'object_name': 'GradeParticipant'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'grade': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gsaudit.Grade']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jsondata': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pupil': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gsaudit.Pupil']"})
        },
        u'gsaudit.pupil': {
            'Meta': {'ordering': "('last_name', 'first_name')", 'object_name': 'Pupil'},
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jsondata': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'gsaudit.pupilauditskill': {
            'Meta': {'object_name': 'PupilAuditSkill'},
            'audit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gsaudit.Audit']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'diagnosis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jsondata': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pupil': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gsaudit.Pupil']"}),
            'rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gsaudit.Skill']"}),
            'written_exam': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'gsaudit.pupiltainfo': {
            'Meta': {'unique_together': "(('pupil', 'teaching_assignment'),)", 'object_name': 'PupilTAInfo'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'jsondata': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pupil': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gsaudit.Pupil']"}),
            'teaching_assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gsaudit.TeachingAssignment']"}),
            'written_exam_rating': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True', 'blank': 'True'})
        },
        u'gsaudit.school': {
            'Meta': {'object_name': 'School'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jsondata': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'gsaudit.skill': {
            'Meta': {'object_name': 'Skill'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jsondata': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['gsaudit.Skill']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'gsaudit.subject': {
            'Meta': {'object_name': 'Subject'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jsondata': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'gsaudit.teacher': {
            'Meta': {'object_name': 'Teacher'},
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gsaudit.School']"}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'gsaudit.teachingassignment': {
            'Meta': {'object_name': 'TeachingAssignment'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'grade': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gsaudit.Grade']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jsondata': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gsaudit.Skill']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gsaudit.Subject']"}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gsaudit.Teacher']"})
        }
    }

    complete_apps = ['gsaudit']