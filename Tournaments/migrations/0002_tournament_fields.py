# Přidání chybějících polí Tournament modelu (name, max_teams, start_time)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tournaments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='tournament',
            name='max_teams',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='tournament',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
    ]
