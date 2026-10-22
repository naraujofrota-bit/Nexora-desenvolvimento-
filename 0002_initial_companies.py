from django.db import migrations

def add_initial_companies(apps, schema_editor):
    Company = apps.get_model("core", "Company")
    Company.objects.get_or_create(name="Bioflex")
    Company.objects.get_or_create(name="Pontual Gráfica")

class Migration(migrations.Migration):
    dependencies = [("core", "0001_initial")]
    operations = [migrations.RunPython(add_initial_companies, migrations.RunPython.noop)]
