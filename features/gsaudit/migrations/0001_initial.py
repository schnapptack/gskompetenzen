# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'School'
        db.create_table('gsaudit_school', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('jsondata', self.gf('jsonfield.JSONField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('gsaudit', ['School'])

        # Adding model 'Teacher'
        db.create_table('gsaudit_teacher', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gsaudit.School'])),
        ))
        db.send_create_signal('gsaudit', ['Teacher'])

        # Adding model 'Grade'
        db.create_table('gsaudit_grade', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('jsondata', self.gf('jsonfield.JSONField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gsaudit.School'])),
        ))
        db.send_create_signal('gsaudit', ['Grade'])

        # Adding model 'Pupil'
        db.create_table('gsaudit_pupil', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('jsondata', self.gf('jsonfield.JSONField')(blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phone_home_fix', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phone_mother_business', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phone_mother_mobile', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phone_father_business', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phone_father_mobile', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('gsaudit', ['Pupil'])

        # Adding model 'Skill'
        db.create_table('gsaudit_skill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('jsondata', self.gf('jsonfield.JSONField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['gsaudit.Skill'])),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('gsaudit', ['Skill'])

        # Adding model 'Subject'
        db.create_table('gsaudit_subject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('jsondata', self.gf('jsonfield.JSONField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gsaudit.Skill'])),
        ))
        db.send_create_signal('gsaudit', ['Subject'])

        # Adding model 'Audit'
        db.create_table('gsaudit_audit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('jsondata', self.gf('jsonfield.JSONField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('grade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gsaudit.Grade'])),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gsaudit.Subject'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('gsaudit', ['Audit'])

        # Adding model 'GradeParticipant'
        db.create_table('gsaudit_gradeparticipant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('jsondata', self.gf('jsonfield.JSONField')(blank=True)),
            ('grade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gsaudit.Grade'])),
            ('pupil', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gsaudit.Pupil'])),
        ))
        db.send_create_signal('gsaudit', ['GradeParticipant'])

        # Adding model 'PupilAuditSkill'
        db.create_table('gsaudit_pupilauditskill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('jsondata', self.gf('jsonfield.JSONField')(blank=True)),
            ('rating', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('pupil', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gsaudit.Pupil'])),
            ('audit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gsaudit.Audit'])),
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gsaudit.Skill'])),
        ))
        db.send_create_signal('gsaudit', ['PupilAuditSkill'])

        # Adding model 'AuditSkill'
        db.create_table('gsaudit_auditskill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('jsondata', self.gf('jsonfield.JSONField')(blank=True)),
            ('weight', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('audit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gsaudit.Audit'])),
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gsaudit.Skill'])),
        ))
        db.send_create_signal('gsaudit', ['AuditSkill'])

        # Adding model 'TeachingAssignment'
        db.create_table('gsaudit_teachingassignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('jsondata', self.gf('jsonfield.JSONField')(blank=True)),
            ('teacher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gsaudit.Teacher'])),
            ('grade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gsaudit.Grade'])),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gsaudit.Subject'])),
        ))
        db.send_create_signal('gsaudit', ['TeachingAssignment'])

        # Adding model 'PupilTAInfo'
        db.create_table('gsaudit_pupiltainfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('jsondata', self.gf('jsonfield.JSONField')(blank=True)),
            ('info', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('pupil', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gsaudit.Pupil'])),
            ('teaching_assignment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gsaudit.TeachingAssignment'])),
        ))
        db.send_create_signal('gsaudit', ['PupilTAInfo'])

        # Adding unique constraint on 'PupilTAInfo', fields ['pupil', 'teaching_assignment']
        db.create_unique('gsaudit_pupiltainfo', ['pupil_id', 'teaching_assignment_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'PupilTAInfo', fields ['pupil', 'teaching_assignment']
        db.delete_unique('gsaudit_pupiltainfo', ['pupil_id', 'teaching_assignment_id'])

        # Deleting model 'School'
        db.delete_table('gsaudit_school')

        # Deleting model 'Teacher'
        db.delete_table('gsaudit_teacher')

        # Deleting model 'Grade'
        db.delete_table('gsaudit_grade')

        # Deleting model 'Pupil'
        db.delete_table('gsaudit_pupil')

        # Deleting model 'Skill'
        db.delete_table('gsaudit_skill')

        # Deleting model 'Subject'
        db.delete_table('gsaudit_subject')

        # Deleting model 'Audit'
        db.delete_table('gsaudit_audit')

        # Deleting model 'GradeParticipant'
        db.delete_table('gsaudit_gradeparticipant')

        # Deleting model 'PupilAuditSkill'
        db.delete_table('gsaudit_pupilauditskill')

        # Deleting model 'AuditSkill'
        db.delete_table('gsaudit_auditskill')

        # Deleting model 'TeachingAssignment'
        db.delete_table('gsaudit_teachingassignment')

        # Deleting model 'PupilTAInfo'
        db.delete_table('gsaudit_pupiltainfo')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'gsaudit.audit': {
            'Meta': {'object_name': 'Audit'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'grade': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gsaudit.Grade']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jsondata': ('jsonfield.JSONField', [], {'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gsaudit.Subject']"})
        },
        'gsaudit.auditskill': {
            'Meta': {'object_name': 'AuditSkill'},
            'audit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gsaudit.Audit']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jsondata': ('jsonfield.JSONField', [], {'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gsaudit.Skill']"}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'gsaudit.grade': {
            'Meta': {'object_name': 'Grade'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jsondata': ('jsonfield.JSONField', [], {'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gsaudit.School']"})
        },
        'gsaudit.gradeparticipant': {
            'Meta': {'object_name': 'GradeParticipant'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'grade': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gsaudit.Grade']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jsondata': ('jsonfield.JSONField', [], {'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'pupil': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gsaudit.Pupil']"})
        },
        'gsaudit.pupil': {
            'Meta': {'ordering': "('first_name', 'last_name')", 'object_name': 'Pupil'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jsondata': ('jsonfield.JSONField', [], {'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'phone_father_business': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone_father_mobile': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone_home_fix': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone_mother_business': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone_mother_mobile': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'gsaudit.pupilauditskill': {
            'Meta': {'object_name': 'PupilAuditSkill'},
            'audit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gsaudit.Audit']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jsondata': ('jsonfield.JSONField', [], {'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pupil': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gsaudit.Pupil']"}),
            'rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gsaudit.Skill']"})
        },
        'gsaudit.pupiltainfo': {
            'Meta': {'unique_together': "(('pupil', 'teaching_assignment'),)", 'object_name': 'PupilTAInfo'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'jsondata': ('jsonfield.JSONField', [], {'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'pupil': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gsaudit.Pupil']"}),
            'teaching_assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gsaudit.TeachingAssignment']"})
        },
        'gsaudit.school': {
            'Meta': {'object_name': 'School'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jsondata': ('jsonfield.JSONField', [], {'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'gsaudit.skill': {
            'Meta': {'object_name': 'Skill'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jsondata': ('jsonfield.JSONField', [], {'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['gsaudit.Skill']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'gsaudit.subject': {
            'Meta': {'object_name': 'Subject'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jsondata': ('jsonfield.JSONField', [], {'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gsaudit.Skill']"})
        },
        'gsaudit.teacher': {
            'Meta': {'object_name': 'Teacher', '_ormbases': ['auth.User']},
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gsaudit.School']"}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'gsaudit.teachingassignment': {
            'Meta': {'object_name': 'TeachingAssignment'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'grade': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gsaudit.Grade']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jsondata': ('jsonfield.JSONField', [], {'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gsaudit.Subject']"}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gsaudit.Teacher']"})
        }
    }

    complete_apps = ['gsaudit']
