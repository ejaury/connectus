
from south.db import db
from django.db import models
from connectus.grades.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Gradeable'
        db.create_table('grades_gradeable', (
            ('id', orm['grades.Gradeable:id']),
            ('name', orm['grades.Gradeable:name']),
            ('course', orm['grades.Gradeable:course']),
            ('created_at', orm['grades.Gradeable:created_at']),
            ('updated_at', orm['grades.Gradeable:updated_at']),
        ))
        db.send_create_signal('grades', ['Gradeable'])
        
        # Adding model 'Grade'
        db.create_table('grades_grade', (
            ('id', orm['grades.Grade:id']),
            ('comment', orm['grades.Grade:comment']),
            ('score', orm['grades.Grade:score']),
            ('gradeable', orm['grades.Grade:gradeable']),
            ('student', orm['grades.Grade:student']),
        ))
        db.send_create_signal('grades', ['Grade'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Gradeable'
        db.delete_table('grades_gradeable')
        
        # Deleting model 'Grade'
        db.delete_table('grades_grade')
        
    
    
    models = {
        'courses.course': {
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'grades.grade': {
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'gradeable': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grades.Gradeable']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.FloatField', [], {}),
            'student': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'grades.gradeable': {
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.Course']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['grades']
