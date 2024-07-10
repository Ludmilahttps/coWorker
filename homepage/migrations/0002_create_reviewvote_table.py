# homepage/migrations/0002_create_reviewvote_table.py

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_type', models.CharField(choices=[('upvote', 'Upvote'), ('downvote', 'Downvote')], max_length=10)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='homepage.rating')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.users')),
            ],
        ),
    ]
