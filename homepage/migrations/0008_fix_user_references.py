# homepage/migrations/0003_fix_user_references.py

from django.db import migrations

def fix_user_references(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    # Obter os modelos
    WorkspacePhoto = apps.get_model('homepage', 'WorkspacePhoto')
    EventUser = apps.get_model('homepage', 'EventUser')
    Rating = apps.get_model('homepage', 'Rating')
    ReviewVote = apps.get_model('homepage', 'ReviewVote')
    Trip = apps.get_model('homepage', 'Trip')
    LikedWorkspaces = apps.get_model('homepage', 'LikedWorkspaces')

    # Corrigir as referências em todas as tabelas relevantes
    for model in [WorkspacePhoto, EventUser, Rating, ReviewVote, Trip, LikedWorkspaces]:
        for obj in model.objects.using(db_alias).all():
            if obj.user_id:
                try:
                    # Atualizar o user_id com base na tabela accounts_users
                    user = apps.get_model('accounts', 'Users').objects.using(db_alias).get(id=obj.user_id)
                    obj.user_id = user.id
                    obj.save()
                except apps.get_model('accounts', 'Users').DoesNotExist:
                    # Se o usuário não existir, você pode decidir o que fazer: deletar o registro, definir como NULL, etc.
                    pass

class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0007_alter_eventuser_user_alter_likedworkspaces_user_and_more'),
    ]

    operations = [
        migrations.RunPython(fix_user_references),
    ]