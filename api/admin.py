from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Artist, Album, Song, Playlist, Genre, UserActivity, 
    Subscription, UserPreferences, Radio, Podcast, PodcastEpisode, 
    UserFollowing, SongRating
)

# Register your models here.

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'firstname', 'lastname', 'is_staff', 'is_active', 'date_joined', 'last_login')
    list_filter = ('is_staff', 'is_active', 'is_premium')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'firstname', 'lastname', 'avatar', 'bio', 'date_of_birth', 'country', 'language')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Additional info', {'fields': ('slug', 'is_premium', 'last_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'username', 'firstname', 'lastname')
    ordering = ('email',)

admin.site.register(User, UserAdmin)

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('stage_name', 'account', 'verified', 'date_created')
    search_fields = ('stage_name', 'account__email')
    list_filter = ('verified', 'genres')

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date', 'is_single')
    search_fields = ('title', 'artist__stage_name')
    list_filter = ('release_date', 'genres', 'is_single')

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'duration', 'release_date')
    search_fields = ('title', 'artist__stage_name', 'album__title')
    list_filter = ('release_date', 'genres', 'explicit')

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_public', 'date_created', 'date_updated')
    search_fields = ('name', 'user__username')
    list_filter = ('is_public', 'date_created')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'song', 'listened_at', 'duration_listened', 'source')
    search_fields = ('user__username', 'song__title')
    list_filter = ('listened_at', 'source')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_type', 'start_date', 'end_date', 'is_active')
    search_fields = ('user__username', 'user__email')
    list_filter = ('subscription_type', 'is_active')

@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'audio_quality', 'language', 'enable_explicit_content')
    search_fields = ('user__username', 'user__email')
    list_filter = ('audio_quality', 'language', 'enable_explicit_content')

@admin.register(Radio)
class RadioAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'is_active', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active', 'genre')

@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ('title', 'host', 'language', 'is_explicit')
    search_fields = ('title', 'host')
    list_filter = ('language', 'is_explicit', 'genres')

@admin.register(PodcastEpisode)
class PodcastEpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'podcast', 'duration', 'release_date')
    search_fields = ('title', 'podcast__title')
    list_filter = ('release_date',)

@admin.register(UserFollowing)
class UserFollowingAdmin(admin.ModelAdmin):
    list_display = ('user', 'artist', 'followed_at')
    search_fields = ('user__username', 'artist__stage_name')
    list_filter = ('followed_at',)

@admin.register(SongRating)
class SongRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'song', 'rating', 'created_at')
    search_fields = ('user__username', 'song__title')
    list_filter = ('rating', 'created_at')


