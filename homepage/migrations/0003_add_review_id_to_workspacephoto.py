# homepage/migrations/0003_add_review_id_to_workspacephoto.py

from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_create_reviewvote_table'),  # Ajuste para depender da última migração aplicada
    ]

    operations = [
        migrations.AddField(
            model_name='workspacephoto',
            name='review',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='homepage.rating'),
            preserve_default=False,
        ),
    ]
