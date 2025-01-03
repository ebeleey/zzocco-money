from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_co_no', models.TextField()),
                ('kor_co_nm', models.TextField()),
                ('fin_prdt_cd', models.TextField(unique=True)),
                ('fin_prdt_nm', models.TextField()),
                ('join_way', models.TextField()),
                ('join_deny', models.IntegerField(choices=[(1, '제한없음'), (2, '서민전용'), (3, '일부제한')])),
                ('join_member', models.TextField()),
                ('spcl_cnd', models.TextField()),
                ('etc_note', models.TextField(blank=True, null=True)),
                ('max_limit', models.BigIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Saving',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_co_no', models.TextField()),
                ('kor_co_nm', models.TextField()),
                ('fin_prdt_cd', models.TextField(unique=True)),
                ('fin_prdt_nm', models.TextField()),
                ('join_way', models.TextField()),
                ('join_deny', models.IntegerField(choices=[(1, '제한없음'), (2, '서민전용'), (3, '일부제한')])),
                ('join_member', models.TextField()),
                ('spcl_cnd', models.TextField()),
                ('etc_note', models.TextField(blank=True, null=True)),
                ('max_limit', models.BigIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SavingOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intr_rate_type', models.CharField(max_length=10)),
                ('intr_rate_type_nm', models.CharField(max_length=100)),
                ('rsrv_type', models.CharField(max_length=10, null=True)),
                ('rsrv_type_nm', models.CharField(max_length=50, null=True)),
                ('save_trm', models.IntegerField()),
                ('intr_rate', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('intr_rate2', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('saving_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='savings.saving')),
            ],
        ),
        migrations.CreateModel(
            name='DepositOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intr_rate_type', models.CharField(max_length=10)),
                ('intr_rate_type_nm', models.CharField(max_length=100)),
                ('save_trm', models.IntegerField()),
                ('intr_rate', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('intr_rate2', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('deposit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='savings.deposit')),
            ],
        ),
    ]
