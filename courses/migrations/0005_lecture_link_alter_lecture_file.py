from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_lecture_course_alter_course_price_enrollment'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='link',
            field=models.URLField(blank=True, verbose_name='رابط المحاضرة أو اللايف'),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='lectures/'),
        ),
    ]
