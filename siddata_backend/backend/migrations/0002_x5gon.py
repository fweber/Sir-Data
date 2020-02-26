from django.db import migrations
from backend.models import X5gonResource
import csv
from siddata_backend import settings

def forwards(apps, schema_editor):
    if schema_editor.connection.alias != 'default':
        return

    with open('%s/backend/test_data/datasets_x5gon_catalogue.tsv'%settings.BASE_DIR) as tsvfile:
      reader = csv.reader(tsvfile, delimiter='\t')
      for row in reader:
        id = row[0]
        title = row[1]
        type = row[3]
        language = row[2]
        keywords = [x.strip() for x in row[4][1:-1].split(",")]
        concepts = [x.strip() for x in row[5][1:-1].split(",")]

        object = X5gonResource.objects.get_or_create(x5gon_id=id, title=title, type=type, language=language, keywords=keywords, concepts=concepts)[0]
        object.save()

class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
