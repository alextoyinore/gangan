from django.db import models
from helpers.lists import countries, ethnicities, languages
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.utils import timezone
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import random
import string
from rest_framework.authtoken.models import Token
from django.utils.text import slugify



# Create your models here.

def validate_username(value):
    if not value.replace('_', '').replace('-', '').isalnum():
        raise ValidationError(
            _('Username can only contain alphanumeric characters, underscores, and hyphens.'),
            code='invalid_username'
        )

def generate_unique_slug(model):
    characters = string.ascii_letters + string.digits
    while True:
        slug = ''.join(random.choice(characters) for _ in range(8))
        if not model.objects.filter(slug=slug).exists():
            return slug


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):

        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email).lower()
        username = username.lower()
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, username, password, **extra_fields)


    def get_by_natural_key(self, email):
        return self.get(email=email)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=250, 
        unique=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9_-]+$',
                code='invalid_username'
            ),
            validate_username
        ]
    )
    country = models.CharField(choices=countries, max_length=200, null=True)
    ethnicity = models.CharField(choices=ethnicities, max_length=200, null=True)
    language = models.CharField(max_length=2, choices=languages, default='en', null=True, blank=True)
    slug = models.SlugField(max_length=8, unique=True, blank=True)
    avatar = models.ImageField(upload_to='user_avatars/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_premium = models.BooleanField(default=False, null=True)
    is_artist = models.BooleanField(default=False, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(User)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.username

    def get_short_name(self):
        return self.first_name or self.username

    def clean(self):
        super().clean()
        validate_username(self.username)

    def update_last_active(self):
        self.last_active = timezone.now()
        self.save(update_fields=['last_active'])


class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='artist_user_profile', null=True)
    stage_name = models.CharField(max_length=200)
    bio = models.TextField(blank=True, null=True)
    genres = models.ManyToManyField('Genre', related_name='artists', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    verified = models.BooleanField(default=False, null=True)
    social_links = models.JSONField(default=dict, null=True, blank=True)  # Store social media links

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Artist)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.stage_name


class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums', null=False)
    title = models.CharField(max_length=200)
    release_date = models.DateField(null=True, blank=True)
    cover_image = models.ImageField(upload_to='album_covers/', null=True, blank=True)
    genres = models.ManyToManyField('Genre', related_name='albums_genres', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    is_single = models.BooleanField(default=False, null=True)
    record_label = models.CharField(max_length=200, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Album)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.artist.stage_name} - {self.title}'
    
    class Meta:
        unique_together = ('artist', 'title')


class Song(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='songs')
    title = models.CharField(max_length=200)
    duration = models.DurationField(null=True, blank=True)
    file = models.FileField(upload_to='songs/', null=True, blank=True)
    genres = models.ManyToManyField('Genre', related_name='song_genres', blank=True)
    release_date = models.DateField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    lyrics = models.TextField(blank=True, null=True)
    isrc = models.CharField(max_length=12, blank=True, null=True, help_text="International Standard Recording Code")
    bpm = models.PositiveIntegerField(null=True, blank=True, help_text="Beats Per Minute")
    explicit = models.BooleanField(default=False, null=True)
    # Store waveform data for visualization
    waveform_data = models.JSONField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('album', 'title')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Song)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.artist.stage_name} - {self.title}'


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    name = models.CharField(max_length=200)
    songs = models.ManyToManyField('Song', related_name='playlist_songs', through='PlaylistSong', blank=True)
    is_public = models.BooleanField(default=False, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='playlist_covers/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Playlist)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - {self.name}'



class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        unique_together = ['playlist', 'song']


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Genre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_user')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='activity_song')
    listened_at = models.DateTimeField(auto_now_add=True)
    duration_listened = models.DurationField()
    source = models.CharField(max_length=50, choices=[
        ('search', 'Search'),
        ('playlist', 'Playlist'),
        ('radio', 'Radio'),
        ('recommendation', 'Recommendation')
    ])

    class Meta:
        verbose_name_plural = 'User Activities'

    def __str__(self):
        return f'{self.user.username} listened to {self.song.title}'


class Subscription(models.Model):
    Subscription_Types = [
        ('free', 'Free'),
        ('premium', 'Premium'),
        ('family', 'Family'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription_user')
    subscription_type = models.CharField(max_length=10, choices=Subscription_Types, default='Free')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.subscription_type}'


class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    favorite_genres = models.ManyToManyField(Genre, blank=True)
    favorite_artists = models.ManyToManyField(Artist, blank=True)
    audio_quality = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('lossless', 'Lossless')
    ], default='medium')
    language = models.CharField(max_length=10, default='en')
    enable_explicit_content = models.BooleanField(default=False)


class Radio(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Radio)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class RadioSong(models.Model):
    radio = models.ForeignKey(Radio, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        unique_together = ['radio', 'song']
        

class Podcast(models.Model):
    title = models.CharField(max_length=200)
    host = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='podcast_covers/', null=True, blank=True)
    rss_feed = models.URLField(unique=True)
    genres = models.ManyToManyField(Genre, related_name='podcasts')
    language = models.CharField(max_length=10, choices=languages)
    is_explicit = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Podcast)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PodcastEpisode(models.Model):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='episodes')
    title = models.CharField(max_length=200)
    description = models.TextField()
    audio_file = models.FileField(upload_to='podcast_episodes/')
    duration = models.DurationField()
    release_date = models.DateTimeField()
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(PodcastEpisode)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.podcast.title} - {self.title}'


class UserFollowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='followed_artist')
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'artist']

    def __str__(self):
        return f'{self.user.username} follows {self.artist.stage_name}'


class SongReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(null=True, blank=True, choices=[
        (1,1), (2,2), (3,3), (4,4), (5,5)
    ])
    review = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'song']

    def __str__(self):
        return f'{self.user.username} rated {self.song.title}: {self.rating}'




from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourited_by')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Favourite Entry: {self.content_object} added on {self.date_added}'


class Library(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='library_owner')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Library Entry: {self.content_object} added on {self.date_added}'

