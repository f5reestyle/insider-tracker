# Generated by Django 3.1.5 on 2021-03-04 04:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Firm',
            fields=[
                ('cik', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('country', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='SIC',
            fields=[
                ('sic', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('industry', models.CharField(max_length=61)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('ticker', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('exchange', models.CharField(choices=[('NASDAQ', 'Nasdaq'), ('NYSE', 'NYSE')], max_length=6)),
                ('IPO_year', models.CharField(max_length=4, null=True)),
                ('is_active', models.BooleanField(null=True)),
                ('volume', models.IntegerField(null=True)),
                ('firm', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stocks.firm')),
            ],
        ),
        migrations.CreateModel(
            name='Insider',
            fields=[
                ('cik', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('amount', models.IntegerField()),
                ('firm', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stocks.firm')),
            ],
        ),
        migrations.AddField(
            model_name='firm',
            name='sic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stocks.sic'),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('accNumber', models.IntegerField(primary_key=True, serialize=False)),
                ('transaction_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('amount', models.IntegerField()),
                ('price', models.IntegerField()),
                ('title', models.CharField(choices=[('CS', 'Common Stock'), ('SO', 'Stock Option')], max_length=2)),
                ('action', models.CharField(choices=[('A', 'Acquired'), ('D', 'Disposed of')], max_length=1)),
                ('firm', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stocks.firm')),
            ],
        ),
    ]
