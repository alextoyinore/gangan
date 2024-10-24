from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import (
    User, Artist, Album, Song, Playlist, Genre, UserActivity, 
    Subscription, UserPreferences, Radio, Podcast, PodcastEpisode, 
    UserFollowing, SongRating, PlaylistSong
)
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from .models import User
from .serializers import UserSerializer
from django.contrib.auth import login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import (
    UserSerializer, ArtistSerializer, AlbumSerializer, SongSerializer, 
    PlaylistSerializer, GenreSerializer, UserActivitySerializer, 
    SubscriptionSerializer, UserPreferencesSerializer, RadioSerializer, 
    PodcastSerializer, PodcastEpisodeSerializer, UserFollowingSerializer, 
    SongRatingSerializer, PlaylistSongSerializer,
    DetailedAlbumSerializer, DetailedPlaylistSerializer, 
    DetailedArtistSerializer, DetailedPodcastSerializer
)
from .permissions import IsAuthenticatedOrCreateOnly
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from dj_rest_auth.registration.views import SocialLoginView



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrCreateOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            # 'token': token.key,
            'user': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        return serializer.save()
    
    def perform_update(self, serializer):
        return serializer.save()

    @action(detail=True, methods=['get'])
    def playlists(self, request, pk=None):
        user = self.get_object()
        playlists = Playlist.objects.filter(user=user)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def activity(self, request, pk=None):
        user = self.get_object()
        activities = UserActivity.objects.filter(user=user)
        serializer = UserActivitySerializer(activities, many=True)
        return Response(serializer.data)

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    @action(detail=True, methods=['get'])
    def albums(self, request, pk=None):
        artist = self.get_object()
        albums = Album.objects.filter(artist=artist)
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def songs(self, request, pk=None):
        artist = self.get_object()
        songs = Song.objects.filter(artist=artist)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    @action(detail=True, methods=['get'])
    def songs(self, request, pk=None):
        album = self.get_object()
        songs = Song.objects.filter(album=album)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DetailedAlbumSerializer(instance)
        return Response(serializer.data)

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        song = self.get_object()
        user = request.user
        rating = request.data.get('rating')
        if rating is None:
            return Response({'error': 'Rating is required'}, status=status.HTTP_400_BAD_REQUEST)
        rating_obj, created = SongRating.objects.update_or_create(
            user=user, song=song, defaults={'rating': rating}
        )
        serializer = SongRatingSerializer(rating_obj)
        return Response(serializer.data)

class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DetailedPlaylistSerializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_song(self, request, pk=None):
        playlist = self.get_object()
        song_id = request.data.get('song_id')
        if song_id is None:
            return Response({'error': 'Song ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        song = get_object_or_404(Song, id=song_id)
        playlist_song, created = PlaylistSong.objects.get_or_create(playlist=playlist, song=song)
        if not created:
            return Response({'error': 'Song already in playlist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PlaylistSongSerializer(playlist_song)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class UserActivityViewSet(viewsets.ModelViewSet):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserActivity.objects.filter(user=self.request.user)

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

class UserPreferencesViewSet(viewsets.ModelViewSet):
    queryset = UserPreferences.objects.all()
    serializer_class = UserPreferencesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserPreferences.objects.filter(user=self.request.user)

class RadioViewSet(viewsets.ModelViewSet):
    queryset = Radio.objects.all()
    serializer_class = RadioSerializer

class PodcastViewSet(viewsets.ModelViewSet):
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DetailedPodcastSerializer(instance)
        return Response(serializer.data)

class PodcastEpisodeViewSet(viewsets.ModelViewSet):
    queryset = PodcastEpisode.objects.all()
    serializer_class = PodcastEpisodeSerializer

class UserFollowingViewSet(viewsets.ModelViewSet):
    queryset = UserFollowing.objects.all()
    serializer_class = UserFollowingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserFollowing.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def follow(self, request):
        artist_id = request.data.get('artist_id')
        if artist_id is None:
            return Response({'error': 'Artist ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        artist = get_object_or_404(Artist, id=artist_id)
        following, created = UserFollowing.objects.get_or_create(user=request.user, artist=artist)
        if not created:
            return Response({'error': 'Already following this artist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(following)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def unfollow(self, request):
        artist_id = request.data.get('artist_id')
        if artist_id is None:
            return Response({'error': 'Artist ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        following = get_object_or_404(UserFollowing, user=request.user, artist_id=artist_id)
        following.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SongRatingViewSet(viewsets.ModelViewSet):
    queryset = SongRating.objects.all()
    serializer_class = SongRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SongRating.objects.filter(user=self.request.user)
    

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username_or_email = request.data.get('username_or_email')
    password = request.data.get('password')

    # logger.debug(f"Login attempt for user: {username_or_email}")

    if username_or_email is None or password is None:
        return Response({'error': 'Please provide both username/email and password'},
                        status=status.HTTP_400_BAD_REQUEST)

    # Determine if the input is an email or username
    try:
        validate_email(username_or_email)
        is_email = True
    except ValidationError:
        is_email = False

    # Check if the user exists
    try:
        if is_email:
            user = User.objects.get(email=username_or_email)
        else:
            user = User.objects.get(username=username_or_email)
    except User.DoesNotExist:
        logger.warning(f"User not found: {username_or_email}")
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Authenticate the user
    authenticated_user = authenticate(request, username=user.username, password=password)

    if not authenticated_user:
        logger.warning(f"Failed login attempt for user: {username_or_email}")
        return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

    # logger.info(f"Successful login for user: {username_or_email}")
    token, _ = Token.objects.get_or_create(user=authenticated_user)
    serializer = UserSerializer(authenticated_user)

    return Response({
        'token': token.key,
        'user': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_token(request):
    user = request.user
    try:
        token = Token.objects.get(user=user)
        # Check if token is expired (assuming a 30-day expiry)
        is_expired = token.created < timezone.now() - timedelta(days=30)
        if is_expired:
            # Delete the old token
            token.delete()
            # Create a new token
            token = Token.objects.create(user=user)
    except Token.DoesNotExist:
        # If token doesn't exist, create a new one
        token = Token.objects.create(user=user)
    
    return Response({
        'token': token.key,
        'user_id': user.id,
        'email': user.email
    })


