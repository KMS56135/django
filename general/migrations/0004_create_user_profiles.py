from django.db import migrations

def create_user_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('general', 'UserProfile')
    
    for user in User.objects.all():
        UserProfile.objects.get_or_create(user=user)

def reverse_func(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('general', '0003_userprofile'),
    ]

    operations = [
        migrations.RunPython(create_user_profiles, reverse_func),
    ] 