# Generated by Django 4.2.3 on 2023-07-22 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_alter_mailing_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'permissions': [('can_view_users', 'can_view_users'), ('can_block_users', 'can_block_users')], 'verbose_name': 'Клиент', 'verbose_name_plural': 'Клиенты'},
        ),
    ]
