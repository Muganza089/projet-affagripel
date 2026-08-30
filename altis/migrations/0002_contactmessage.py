# Ajout du modele ContactMessage (page /contact, sujet libre).
# DevisRequest n'est PAS modifie : aucune operation sur altis_devis_request.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('altis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=255)),
                ('telephone', models.CharField(blank=True, default='', max_length=30)),
                ('entreprise', models.CharField(blank=True, default='', max_length=200)),
                ('sujet', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('statut', models.CharField(choices=[('nouveau', 'Nouveau'), ('en_cours', 'En cours'), ('traite', 'Traité'), ('rejete', 'Rejeté / spam')], db_index=True, default='nouveau', max_length=16)),
                ('notes_internes', models.TextField(blank=True, default='')),
                ('source_origin', models.CharField(blank=True, default='', max_length=200)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.CharField(blank=True, default='', max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Message de contact ALTIS',
                'verbose_name_plural': 'Messages de contact ALTIS',
                'db_table': 'altis_contact_message',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['email', '-created_at'], name='altis_contact_email_idx')],
            },
        ),
    ]
