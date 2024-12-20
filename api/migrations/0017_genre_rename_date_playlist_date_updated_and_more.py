# Generated by Django 5.0.6 on 2024-10-22 01:22

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_user_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.RenameField(
            model_name='playlist',
            old_name='date',
            new_name='date_updated',
        ),
        migrations.RemoveField(
            model_name='album',
            name='album_data',
        ),
        migrations.RemoveField(
            model_name='album',
            name='date',
        ),
        migrations.RemoveField(
            model_name='artist',
            name='artist_data',
        ),
        migrations.RemoveField(
            model_name='playlist',
            name='playlist_data',
        ),
        migrations.RemoveField(
            model_name='song',
            name='date',
        ),
        migrations.RemoveField(
            model_name='song',
            name='song_data',
        ),
        migrations.AddField(
            model_name='album',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='album_covers/'),
        ),
        migrations.AddField(
            model_name='album',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='album',
            name='is_single',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='album',
            name='record_label',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='album',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='social_links',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='verified',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='playlist',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='playlist_covers/'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playlist',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='playlist',
            name='is_public',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='songs', to='api.album'),
        ),
        migrations.AddField(
            model_name='song',
            name='bpm',
            field=models.PositiveIntegerField(blank=True, help_text='Beats Per Minute', null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='song',
            name='duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='explicit',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='songs/'),
        ),
        migrations.AddField(
            model_name='song',
            name='isrc',
            field=models.CharField(blank=True, help_text='International Standard Recording Code', max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='lyrics',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='waveform_data',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='user_avatars/'),
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_premium',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='language',
            field=models.CharField(blank=True, choices=[('aa', 'Afar'), ('ab', 'Abkhazian'), ('ae', 'Avestan'), ('af', 'Afrikaans'), ('ak', 'Akan'), ('am', 'Amharic'), ('an', 'Aragonese'), ('ar', 'Arabic'), ('as', 'Assamese'), ('av', 'Avaric'), ('ay', 'Aymara'), ('az', 'Azerbaijani'), ('ba', 'Bashkir'), ('be', 'Belarusian'), ('bg', 'Bulgarian'), ('bh', 'Bihari languages'), ('bi', 'Bislama'), ('bm', 'Bambara'), ('bn', 'Bengali'), ('bo', 'Tibetan'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan; Valencian'), ('ce', 'Chechen'), ('ch', 'Chamorro'), ('co', 'Corsican'), ('cr', 'Cree'), ('cs', 'Czech'), ('cu', 'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic'), ('cv', 'Chuvash'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('dv', 'Divehi; Dhivehi; Maldivian'), ('dz', 'Dzongkha'), ('ee', 'Ewe'), ('el', 'Greek, Modern (1453-)'), ('en', 'English'), ('eo', 'Esperanto'), ('es', 'Spanish; Castilian'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('ff', 'Fulah'), ('fi', 'Finnish'), ('fj', 'Fijian'), ('fo', 'Faroese'), ('fr', 'French'), ('fy', 'Western Frisian'), ('ga', 'Irish'), ('gd', 'Gaelic; Scottish Gaelic'), ('gl', 'Galician'), ('gn', 'Guarani'), ('gu', 'Gujarati'), ('gv', 'Manx'), ('ha', 'Hausa'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('ho', 'Hiri Motu'), ('hr', 'Croatian'), ('ht', 'Haitian; Haitian Creole'), ('hu', 'Hungarian'), ('hy', 'Armenian'), ('hz', 'Herero'), ('ia', 'Interlingua (International Auxiliary Language Association)'), ('id', 'Indonesian'), ('ie', 'Interlingue; Occidental'), ('ig', 'Igbo'), ('ii', 'Sichuan Yi; Nuosu'), ('ik', 'Inupiaq'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('iu', 'Inuktitut'), ('ja', 'Japanese'), ('jv', 'Javanese'), ('ka', 'Georgian'), ('kg', 'Kongo'), ('ki', 'Kikuyu; Gikuyu'), ('kj', 'Kuanyama; Kwanyama'), ('kk', 'Kazakh'), ('kl', 'Kalaallisut; Greenlandic'), ('km', 'Central Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('kr', 'Kanuri'), ('ks', 'Kashmiri'), ('ku', 'Kurdish'), ('kv', 'Komi'), ('kw', 'Cornish'), ('ky', 'Kirghiz; Kyrgyz'), ('la', 'Latin'), ('lb', 'Luxembourgish; Letzeburgesch'), ('lg', 'Ganda'), ('li', 'Limburgan; Limburger; Limburgish'), ('ln', 'Lingala'), ('lo', 'Lao'), ('lt', 'Lithuanian'), ('lu', 'Luba-Katanga'), ('lv', 'Latvian'), ('mg', 'Malagasy'), ('mh', 'Marshallese'), ('mi', 'Maori'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('ms', 'Malay'), ('mt', 'Maltese'), ('my', 'Burmese'), ('na', 'Nauru'), ('nb', 'Bokmål, Norwegian; Norwegian Bokmål'), ('nd', 'Ndebele, North; North Ndebele'), ('ne', 'Nepali'), ('ng', 'Ndonga'), ('nl', 'Dutch; Flemish'), ('nn', 'Norwegian Nynorsk; Nynorsk, Norwegian'), ('no', 'Norwegian'), ('nr', 'Ndebele, South; South Ndebele'), ('nv', 'Navajo; Navaho'), ('ny', 'Chichewa; Chewa; Nyanja'), ('oc', 'Occitan (post 1500)'), ('oj', 'Ojibwa'), ('om', 'Oromo'), ('or', 'Oriya'), ('os', 'Ossetian; Ossetic'), ('pa', 'Panjabi; Punjabi'), ('pi', 'Pali'), ('pl', 'Polish'), ('ps', 'Pushto; Pashto'), ('pt', 'Portuguese'), ('qu', 'Quechua'), ('rm', 'Romansh'), ('rn', 'Rundi'), ('ro', 'Romanian; Moldavian; Moldovan'), ('ru', 'Russian'), ('rw', 'Kinyarwanda'), ('sa', 'Sanskrit'), ('sc', 'Sardinian'), ('sd', 'Sindhi'), ('se', 'Northern Sami'), ('sg', 'Sango'), ('si', 'Sinhala; Sinhalese'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sm', 'Samoan'), ('sn', 'Shona'), ('so', 'Somali'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('ss', 'Swati'), ('st', 'Sotho, Southern'), ('su', 'Sundanese'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('tg', 'Tajik'), ('th', 'Thai'), ('ti', 'Tigrinya'), ('tk', 'Turkmen'), ('tl', 'Tagalog'), ('tn', 'Tswana'), ('to', 'Tonga (Tonga Islands)'), ('tr', 'Turkish'), ('ts', 'Tsonga'), ('tt', 'Tatar'), ('tw', 'Twi'), ('ty', 'Tahitian'), ('ug', 'Uighur; Uyghur'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('uz', 'Uzbek'), ('ve', 'Venda'), ('vi', 'Vietnamese'), ('vo', 'Volapük'), ('wa', 'Walloon'), ('wo', 'Wolof'), ('xh', 'Xhosa'), ('yi', 'Yiddish'), ('yo', 'Yoruba'), ('za', 'Zhuang; Chuang'), ('zh', 'Chinese'), ('zu', 'Zulu')], default='en', max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='last_active',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='api.artist'),
        ),
        migrations.AlterField(
            model_name='album',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='account',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='artist_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='artist',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='stage_name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playlists', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='song',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='api.artist'),
        ),
        migrations.AlterField(
            model_name='song',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='firstname',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='lastname',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='album',
            name='genres',
            field=models.ManyToManyField(blank=True, related_name='albums', to='api.genre'),
        ),
        migrations.AddField(
            model_name='artist',
            name='genres',
            field=models.ManyToManyField(blank=True, related_name='artists', to='api.genre'),
        ),
        migrations.AddField(
            model_name='song',
            name='genres',
            field=models.ManyToManyField(blank=True, related_name='songs', to='api.genre'),
        ),
        migrations.CreateModel(
            name='PlaylistSong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.playlist')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.song')),
            ],
            options={
                'ordering': ['order'],
                'unique_together': {('playlist', 'song')},
            },
        ),
        migrations.AddField(
            model_name='playlist',
            name='songs',
            field=models.ManyToManyField(blank=True, related_name='playlists', through='api.PlaylistSong', to='api.song'),
        ),
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('host', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='podcast_covers/')),
                ('rss_feed', models.URLField(unique=True)),
                ('language', models.CharField(max_length=10)),
                ('is_explicit', models.BooleanField(default=False)),
                ('genres', models.ManyToManyField(related_name='podcasts', to='api.genre')),
            ],
        ),
        migrations.CreateModel(
            name='PodcastEpisode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('audio_file', models.FileField(upload_to='podcast_episodes/')),
                ('duration', models.DurationField()),
                ('release_date', models.DateTimeField()),
                ('podcast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='api.podcast')),
            ],
        ),
        migrations.CreateModel(
            name='Radio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('genre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.genre')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_type', models.CharField(choices=[('FREE', 'Free'), ('PREMIUM', 'Premium'), ('FAMILY', 'Family')], default='FREE', max_length=10)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('payment_method', models.CharField(blank=True, max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listened_at', models.DateTimeField(auto_now_add=True)),
                ('duration_listened', models.DurationField()),
                ('source', models.CharField(choices=[('search', 'Search'), ('playlist', 'Playlist'), ('radio', 'Radio'), ('recommendation', 'Recommendation')], max_length=50)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_activities', to='api.song')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Activities',
            },
        ),
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_quality', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('lossless', 'Lossless')], default='medium', max_length=20)),
                ('language', models.CharField(default='en', max_length=10)),
                ('enable_explicit_content', models.BooleanField(default=False)),
                ('favorite_artists', models.ManyToManyField(blank=True, to='api.artist')),
                ('favorite_genres', models.ManyToManyField(blank=True, to='api.genre')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='preferences', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SongRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='api.song')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'song')},
            },
        ),
        migrations.CreateModel(
            name='UserFollowing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed_at', models.DateTimeField(auto_now_add=True)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='api.artist')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'artist')},
            },
        ),
    ]
