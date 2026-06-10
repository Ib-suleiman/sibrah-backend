from django.db import migrations
from django.contrib.auth import get_user_model

def create_admin(apps, schema_editor):
    User = get_user_model()

    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="Abdullahi",
            email="info@sibrahtech.com.ng",
            password="admin1234590"
        )

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]