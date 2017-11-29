from django.apps import apps as global_apps
from django.db import migrations
from django.db.utils import OperationalError

from django.db.backends.postgresql.schema import DatabaseSchemaEditor as PgSE

sql = '''

'''

reverse_sql = '''

'''

def forwards(app, schema_editor):
    models = app.all_models['api']
    if not isinstance(schema_editor, PgSE):
        print('this migration is only guaranteed to work with Postgres!')
        return
    try:
        schema_editor.execute('alter table south_migrationhistory rename to legacy_south_migrationhistory;')
        print('Found legacy application')
        for model in models:
            schema_editor.execute('drop table api_{0} cascade;'.format(model))
            schema_editor.execute('alter table portal_{0} rename to api_{0};'.format(model))
            schema_editor.execute('alter sequence portal_{0}_id_seq rename to api_{0}_id_seq;'.format(model))

    except Exception as e:
        pass

def backwards(app, schema_editor):
    models = app.all_models['api']
    if not isinstance(schema_editor, PgSE):
        print('this migration is only guaranteed to work with Postgres!')
        return
    try:
        schema_editor.execute('alter table legacy_south_migrationhistory rename to south_migrationhistory;')
        print('Found migrated application')
        for model in models:
            schema_editor.execute('alter table api_{0} rename to portal_{0};'.format(model))
            schema_editor.execute('alter sequence api_{0}_id_seq rename to portal_{0}_id_seq;'.format(model))
    except Exception as e:
        pass

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(forwards, backwards),
    ]
    dependencies = [
        ('api', '0001_initial'),
    ]
