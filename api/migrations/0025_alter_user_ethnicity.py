# Generated by Django 5.1.2 on 2024-10-23 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_alter_user_date_joined_alter_user_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ethnicity',
            field=models.CharField(choices=[('English', 'English'), ('Han Chinese', 'Han Chinese'), ('Arab', 'Arab'), ('Bengali', 'Bengali'), ('Hispanic/Latino', 'Hispanic/Latino'), ('Punjabi', 'Punjabi'), ('Russian', 'Russian'), ('Javanese', 'Javanese'), ('Japanese', 'Japanese'), ('German', 'German'), ('Korean', 'Korean'), ('French', 'French'), ('Vietnamese', 'Vietnamese'), ('Telugu', 'Telugu'), ('Marathi', 'Marathi'), ('Tamil', 'Tamil'), ('Turkish', 'Turkish'), ('Italian', 'Italian'), ('Yoruba', 'Yoruba'), ('Gujarati', 'Gujarati'), ('Persian', 'Persian'), ('Polish', 'Polish'), ('Pashto', 'Pashto'), ('Kannada', 'Kannada'), ('Xhosa', 'Xhosa'), ('Malayali', 'Malayali'), ('Sundanese', 'Sundanese'), ('Hausa', 'Hausa'), ('Thai', 'Thai'), ('Amhara', 'Amhara'), ('Oromo', 'Oromo'), ('Burmese', 'Burmese'), ('Ukrainian', 'Ukrainian'), ('Bhojpuri', 'Bhojpuri'), ('Tagalog', 'Tagalog'), ('Malay', 'Malay'), ('Igbo', 'Igbo'), ('Uzbek', 'Uzbek'), ('Sindhi', 'Sindhi'), ('Oriya', 'Oriya'), ('Romanian', 'Romanian'), ('Cebuano', 'Cebuano'), ('Dutch', 'Dutch'), ('Kurdish', 'Kurdish'), ('Serbo-Croatian', 'Serbo-Croatian'), ('Malagasy', 'Malagasy'), ('Saraiki', 'Saraiki'), ('Nepali', 'Nepali'), ('Sinhalese', 'Sinhalese'), ('Khmer', 'Khmer'), ('Tutsi', 'Tutsi'), ('Hutu', 'Hutu'), ('Fulani', 'Fulani'), ('Somali', 'Somali'), ('Greek', 'Greek'), ('Czech', 'Czech'), ('Portuguese', 'Portuguese'), ('Swedish', 'Swedish'), ('Hungarian', 'Hungarian'), ('Belarusian', 'Belarusian'), ('Zulu', 'Zulu'), ('Jewish', 'Jewish'), ('Armenian', 'Armenian'), ('Berber', 'Berber'), ('Kazakh', 'Kazakh'), ('Tibetan', 'Tibetan'), ('Uyghur', 'Uyghur'), ('Hmong', 'Hmong'), ('Tatar', 'Tatar'), ('Chechen', 'Chechen'), ('Romani', 'Romani'), ('Akan', 'Akan'), ('Shona', 'Shona'), ('Maori', 'Maori'), ('Aboriginal Australian', 'Aboriginal Australian'), ('Inuit', 'Inuit'), ('Native American', 'Native American'), ('Quechua', 'Quechua'), ('Aymara', 'Aymara'), ('Guarani', 'Guarani')], max_length=200, null=True),
        ),
    ]
