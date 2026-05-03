from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tournaments', '0002_tournament_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='password',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='founder',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]
