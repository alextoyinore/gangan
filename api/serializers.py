from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import (
    User, Artist, Album, Song, Playlist, Genre, UserActivity, 
    Subscription, UserPreferences, Radio, Podcast, PodcastEpisode, 
    UserFollowing, SongRating, PlaylistSong
)
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    # token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['slug', 'date_joined', 'last_login', 'last_active']
    
    def get_token(self, obj):
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key


    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        user = User(
            email=validated_data['email'].lower(),
            username=validated_data['username'].lower(),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        
        # Handle many-to-many relationships
        if groups:
            user.groups.set(groups)  # Use set() to assign many-to-many relationships
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        groups = validated_data.pop('groups', None)

        if groups is not None:
            instance.groups.set(groups)  # Update many-to-many relationships
        return super(UserSerializer, self).update(instance, validated_data)
    

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'
        read_only_fields = ['slug']


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'
        read_only_fields = ['slug']


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'
        read_only_fields = ['slug']


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'
        read_only_fields = ['slug']


class PlaylistSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistSong
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
        read_only_fields = ['slug']


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = '__all__'


class RadioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Radio
        fields = '__all__'


class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = '__all__'


class PodcastEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastEpisode
        fields = '__all__'


class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = '__all__'


class SongRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongRating
        fields = '__all__'


# Nested serializers for more detailed views

class DetailedAlbumSerializer(AlbumSerializer):
    songs = SongSerializer(many=True, read_only=True)
    artist = ArtistSerializer(read_only=True)


class DetailedPlaylistSerializer(PlaylistSerializer):
    songs = SongSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)


class DetailedArtistSerializer(ArtistSerializer):
    albums = AlbumSerializer(many=True, read_only=True)
    songs = SongSerializer(many=True, read_only=True)


class DetailedPodcastSerializer(PodcastSerializer):
    episodes = PodcastEpisodeSerializer(many=True, read_only=True)


