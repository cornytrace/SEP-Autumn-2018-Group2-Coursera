# Generated by Django 2.1.1 on 2018-10-01 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursera', '0012_create_leavers_per_module_view'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClickstreamEvent',
            fields=[
                ('id', models.CharField(db_column='hashed_user_id', max_length=100, primary_key=True, serialize=False)),
                ('hashed_session_cookie_id', models.CharField(blank=True, max_length=100, null=True)),
                ('server_timestamp', models.DateTimeField(blank=True, null=True)),
                ('hashed_ip', models.CharField(blank=True, max_length=100, null=True)),
                ('user_agent', models.CharField(blank=True, max_length=100, null=True)),
                ('url', models.CharField(blank=True, max_length=100, null=True)),
                ('initial_referrer_url', models.CharField(blank=True, max_length=100, null=True)),
                ('browser_language', models.CharField(blank=True, max_length=100, null=True)),
                ('course_id', models.CharField(blank=True, max_length=100, null=True)),
                ('country_cd', models.CharField(blank=True, max_length=100, null=True)),
                ('region_cd', models.CharField(blank=True, max_length=100, null=True)),
                ('timezone', models.CharField(blank=True, max_length=100, null=True)),
                ('os', models.CharField(blank=True, max_length=100, null=True)),
                ('browser', models.CharField(blank=True, max_length=100, null=True)),
                ('key', models.CharField(blank=True, max_length=100, null=True)),
                ('value', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'clickstream_events',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LastActivity',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('state_type_id', models.IntegerField(blank=True, db_column='course_progress_state_type_id', null=True)),
                ('timestamp', models.DateTimeField(blank=True, db_column='course_progress_ts', null=True)),
            ],
            options={
                'db_table': 'last_activity_view',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LastActivityPerModule',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(blank=True, db_column='course_progress_ts', null=True)),
            ],
            options={
                'db_table': 'last_activity_per_module',
                'managed': False,
            },
        ),
    ]