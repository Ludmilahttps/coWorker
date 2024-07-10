# homepage/migrations/0002_update_user_references.py

from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0004_alter_workspacephoto_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.users'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.users'),
        ),
        migrations.AlterField(
            model_name='reviewvote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.users'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='user',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='accounts.users'),
        ),
        migrations.AlterField(
            model_name='workspace',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.users'),
        ),
        migrations.AlterField(
            model_name='workspacephoto',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.users'),
        ),
        migrations.AlterField(
            model_name='likedworkspaces',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.users'),
        ),
    ]

