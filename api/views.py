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
            'token': token.key,
            'user': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)

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
    

@api_view(['POST'])
@permission_classes([AllowAny])
def login_with_email(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if email is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        return Response({'error': 'Invalid email or password'},
                        status=status.HTTP_404_NOT_FOUND)

    user = authenticate(username=user.username, password=password)

    if not user:
        return Response({'error': 'Invalid email or password'},
                        status=status.HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)

    return Response({
        'token': token.key,
        'user': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_with_username(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Invalid username or password'},
                        status=status.HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)

    return Response({
        'token': token.key,
        'user': serializer.data
    }, status=status.HTTP_200_OK)


# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter
#     client_class = OAuth2Client

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def google_auth(request):
#     code = request.data.get('code', None)
#     if code is None:
#         return Response({'error': 'Code not provided'}, status=400)

#     try:
#         # Use the GoogleOAuth2Adapter to validate the code
#         adapter = GoogleOAuth2Adapter(request)
#         app = adapter.get_provider().app
#         token = adapter.get_provider().get_app(request).client.get_access_token(code)
        
#         # Get or create the social account
#         social_account = adapter.complete_login(request, app, token)
#         social_account.save()

#         # Get or create the user account
#         user = social_account.user
#         if not user.is_active:
#             return Response({'error': 'User account is disabled'}, status=400)

#         # Get or create the auth token
#         token, _ = Token.objects.get_or_create(user=user)

#         # Log the user in
#         login(request, user)

#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })
#     except Exception as e:
#         return Response({'error': str(e)}, status=400)
