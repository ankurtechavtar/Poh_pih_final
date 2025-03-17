# Generated by Django 4.2.18 on 2025-03-17 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pih_poh_app', '0002_subscriptionplan_usersubscription_payment_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['user', 'status'], name='Pih_poh_app_user_id_6d4e12_idx'),
        ),
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['payment_intent_id'], name='Pih_poh_app_payment_02b14b_idx'),
        ),
    ]
