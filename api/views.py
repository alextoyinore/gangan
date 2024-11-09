from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import (
    User, Artist, Album, Song, Playlist, Genre, UserActivity, 
    Subscription, UserPreferences, Radio, Podcast, PodcastEpisode, 
    UserFollowing, SongRating, PlaylistSong, Favourite, Library
)
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .serializers import UserSerializer
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
    DetailedPodcastSerializer, LibrarySerializer, FavouriteSerializer
)
from .permissions import IsAuthenticatedOrCreateOnly
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from dj_rest_auth.registration.views import SocialLoginView


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrCreateOnly]

    def perform_create(self, serializer):
        return serializer.save()

    def perform_update(self, serializer):
        return serializer.save()

    def get_queryset(self):
        if not self.request.user.is_staff:
            return User.objects.filter(is_staff=False)
        return User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_staff and not request.user.is_staff:
            return Response({'error':'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def playlists(self, request, slug=None):
        user = self.get_object()
        playlists = Playlist.objects.filter(user=user)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def favourites(self, request, slug=None):
        user = self.get_object()
        favourites = Favourite.objects.filter(user=user)
        serializer = FavouriteSerializer(favourites, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def library(self, request, slug=None):
        user = self.get_object()
        items = Library.objects.filter(user=user)
        serializer = LibrarySerializer(items, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def activity(self, request, slug=None):
        user = self.get_object()
        activities = UserActivity.objects.filter(user=user)
        serializer = UserActivitySerializer(activities, many=True)
        return Response(serializer.data)


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        account_id = request.data.get('account')
        stage_name = request.data.get('stage_name')

        if account_id is None or stage_name is None:
            return super().create(request, *args, **kwargs)

        if Artist.objects.filter(account__id=account_id).exists():
            return Response({'error':'This user is already an artist. Duplicate  artist accounts are prohibited'}, status=status.HTTP_403_FORBIDDEN)
        
        if User.objects.filter(id=account_id).exists():
            account = User.objects.get(id=account_id)
            if account == request.user:
                artist = Artist.objects.create(account=account, stage_name=stage_name)
                user = User.objects.get(username=request.user.username)
                user.is_artist = True
                user.save()
                serializer = ArtistSerializer(artist)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
              return Response({'error':'Only account owners may perfrom this action'}, status=status.HTTP_403_FORBIDDEN)  
        else:
            return Response({'error':'The user you are attempting to upgrade to artist status does not exist. Verify that this user exists and try again.'}, status=status.HTTP_404_NOT_FOUND)
        

    def destroy(self, request, *args, **kwargs):
        slug = request.path.split('/')[3]
        print(slug)
        account = Artist.objects.get(slug=slug).account
        if account == request.user:
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({'error':'You do not have permission to perform this operation'}, status=status.HTTP_401_UNAUTHORIZED)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        return serializer.save()

    @action(detail=True, methods=['get'])
    def albums(self, request, slug=None):
        artist = self.get_object()
        albums = Album.objects.filter(artist=artist)
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def songs(self, request, slug=None):
        artist = self.get_object()
        songs = Song.objects.filter(artist=artist)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        title = request.data.get('title')
        artist_id = request.data.get('artist')
        artist = Artist.objects.get(id=artist_id)
        if artist is None and request.user.is_artist and request.user==artist.account:
            album = Album.objects.create(title=title, artist=artist)
            serializer = AlbumSerializer(album)
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        else:
            return Response({'error':'Only artists can create albums'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['get'])
    def songs(self, request, slug=None):
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
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def rate(self, request, slug=None):
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
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DetailedPlaylistSerializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_song(self, request, slug=None):
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
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]

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
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]

class PodcastViewSet(viewsets.ModelViewSet):
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DetailedPodcastSerializer(instance)
        return Response(serializer.data)


class PodcastEpisodeViewSet(viewsets.ModelViewSet):
    queryset = PodcastEpisode.objects.all()
    serializer_class = PodcastEpisodeSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]

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


from django.contrib.contenttypes.models import ContentType

class LibraryViewSet(viewsets.ViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        model_type = request.data.get('model_type')  # e.g., 'book' or 'album'
        model_id = request.data.get('model_id')  # ID of the instance to add

        # Determine the content type
        try:
            content_type = ContentType.objects.get(model=model_type)
            library_entry = Library.objects.create(
                content_type=content_type,
                object_id=model_id
            )
            return Response({'message': 'Added to library', 'id': library_entry.id}, status=status.HTTP_201_CREATED)
        except ContentType.DoesNotExist:
            return Response({'error': 'Invalid model type'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FavouriteViewSet(viewsets.ViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        model_type = request.data.get('model_type')  # e.g., 'book' or 'album'
        model_id = request.data.get('model_id')  # ID of the instance to add

        # Determine the content type
        try:
            content_type = ContentType.objects.get(model=model_type)
            library_entry = Favourite.objects.create(
                content_type=content_type,
                object_id=model_id
            )
            return Response({'message': 'Added to Favourite', 'id': library_entry.id}, status=status.HTTP_201_CREATED)
        except ContentType.DoesNotExist:
            return Response({'error': 'Invalid model type'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username_or_email = request.data.get('username_or_email')
    password = request.data.get('password')

    if username_or_email is None or password is None:
        return Response({'error': 'Please provide both username/email and password'}, status=status.HTTP_400_BAD_REQUEST)

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
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Authenticate the user
    authenticated_user = authenticate(request, username=user.username, password=password)

    if not authenticated_user:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=authenticated_user)
    # serializer = UserSerializer(authenticated_user)

    return Response({
        'token': token.key,
        # 'user': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Log out the user by deleting their authentication token.
    """
    try:
        # Get the token for the authenticated user
        token = Token.objects.get(user=request.user)
        # Delete the token to log out the user
        token.delete()
        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({'error': 'Token does not exist. You may already be logged out.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Handle any other exceptions that may occur
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

