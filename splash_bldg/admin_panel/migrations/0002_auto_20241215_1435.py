# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attendancerecord',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='attendancerecord',
            name='employee_name',
        ),
        migrations.RemoveField(
            model_name='attendancerecord',
            name='employee_id',
        ),
        migrations.RemoveField(
            model_name='attendancerecord',
            name='date',
        ),
        migrations.RemoveField(
            model_name='attendancerecord',
            name='check_in',
        ),
        migrations.RemoveField(
            model_name='attendancerecord',
            name='check_out',
        ),
        migrations.RemoveField(
            model_name='attendancerecord',
            name='hours_worked',
        ),
        migrations.RemoveField(
            model_name='attendancerecord',
            name='status',
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='ref_no',
            field=models.CharField(max_length=50, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='name',
            field=models.CharField(max_length=200, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='category',
            field=models.CharField(max_length=50, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='month',
            field=models.CharField(max_length=20, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='year',
            field=models.IntegerField(default=2024),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='attendance_data',
            field=models.JSONField(default=dict),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attendancerecord',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterUniqueTogether(
            name='attendancerecord',
            unique_together={('ref_no', 'month', 'year')},
        ),
    ]