
from south.db import db
from django.db import models
from connectus.courses.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Course'
        db.create_table('courses_course', (
            ('id', orm['courses.Course:id']),
            ('title', orm['courses.Course:title']),
            ('description', orm['courses.Course:description']),
            ('term', orm['courses.Course:term']),
            ('year', orm['courses.Course:year']),
        ))
        db.send_create_signal('courses', ['Course'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Course'
        db.delete_table('courses_course')
        
    
    
    models = {
        'courses.course': {
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }
    
    complete_apps = ['courses']
