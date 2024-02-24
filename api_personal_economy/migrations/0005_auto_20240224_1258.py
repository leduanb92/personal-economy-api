# Generated by Django 3.2.8 on 2024-02-24 18:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_personal_economy', '0004_alter_cuenta_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cuenta',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='operacion',
            options={'ordering': ['-date']},
        ),
        migrations.RenameField(
            model_name='cuenta',
            old_name='nombre',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='operacion',
            old_name='fecha',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='operacion',
            old_name='descripcion',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='operacion',
            name='cuenta',
        ),
        migrations.RemoveField(
            model_name='operacion',
            name='monto',
        ),
        migrations.RemoveField(
            model_name='operacion',
            name='tipo',
        ),
        migrations.AddField(
            model_name='cuenta',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cuenta',
            name='initial_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AddField(
            model_name='cuenta',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='operacion',
            name='account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='operations', to='api_personal_economy.cuenta'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='operacion',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='operacion',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='operacion',
            name='type',
            field=models.CharField(choices=[('In', 'Income'), ('Exp', 'Expense')], default='Exp', max_length=3),
        ),
        migrations.AddField(
            model_name='operacion',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='cuenta',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='cuenta',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to=settings.AUTH_USER_MODEL),
        ),
    ]
