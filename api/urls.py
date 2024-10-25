'''
Create:
HTTP Method: POST
URL: /api/modelname/

Retrieve (single instance):
HTTP Method: GET
URL: /api/modelname/{id}/

Update:
HTTP Method: PUT (full update) or PATCH (partial update)
URL: /api/modelname/{id}/

4. Delete:
HTTP Method: DELETE
URL: /api/modelname/{id}/

List (multiple instances):
HTTP Method: GET
URL: /api/modelname/

Here's a breakdown for each model:

1. Users:
Create: POST to /api/users/
Retrieve: GET to /api/users/{id}/
Update: PUT/PATCH to /api/users/{id}/
Delete: DELETE to /api/users/{id}/
List: GET to /api/users/

Artists:
Create: POST to /api/artists/
Retrieve: GET to /api/artists/{id}/
Update: PUT/PATCH to /api/artists/{id}/
Delete: DELETE to /api/artists/{id}/
List: GET to /api/artists/

Albums:
Create: POST to /api/albums/
Retrieve: GET to /api/albums/{id}/
Update: PUT/PATCH to /api/albums/{id}/
Delete: DELETE to /api/albums/{id}/
List: GET to /api/albums/

Songs:
Create: POST to /api/songs/
Retrieve: GET to /api/songs/{id}/
Update: PUT/PATCH to /api/songs/{id}/
Delete: DELETE to /api/songs/{id}/
List: GET to /api/songs/

Playlists:
Create: POST to /api/playlists/
Retrieve: GET to /api/playlists/{id}/
Update: PUT/PATCH to /api/playlists/{id}/
Delete: DELETE to /api/playlists/{id}/
List: GET to /api/playlists/

'''


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ArtistViewSet, AlbumViewSet, SongViewSet, PlaylistViewSet,
    GenreViewSet, UserActivityViewSet, SubscriptionViewSet, UserPreferencesViewSet,
    RadioViewSet, PodcastViewSet, PodcastEpisodeViewSet, UserFollowingViewSet,
    SongRatingViewSet
)
from .views import login, get_profile


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'artists', ArtistViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'songs', SongViewSet)
router.register(r'playlists', PlaylistViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'user-activities', UserActivityViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'user-preferences', UserPreferencesViewSet)
router.register(r'radios', RadioViewSet)
router.register(r'podcasts', PodcastViewSet)
router.register(r'podcast-episodes', PodcastEpisodeViewSet)
router.register(r'user-following', UserFollowingViewSet)
router.register(r'song-ratings', SongRatingViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

# Custom action URL patterns
urlpatterns += [
    # User-related custom actions
    path('users/<int:pk>/playlists/', UserViewSet.as_view({'get': 'playlists'}), name='user-playlists'),
    path('users/<int:pk>/activity/', UserViewSet.as_view({'get': 'activity'}), name='user-activity'),
    
    # Artist-related custom actions
    path('artists/<int:pk>/albums/', ArtistViewSet.as_view({'get': 'albums'}), name='artist-albums'),
    path('artists/<int:pk>/songs/', ArtistViewSet.as_view({'get': 'songs'}), name='artist-songs'),
    
    # Album-related custom actions
    path('albums/<int:pk>/songs/', AlbumViewSet.as_view({'get': 'songs'}), name='album-songs'),
    
    # Song-related custom actions
    path('songs/<int:pk>/rate/', SongViewSet.as_view({'post': 'rate'}), name='song-rate'),
    
    # Playlist-related custom actions
    path('playlists/<int:pk>/add-song/', PlaylistViewSet.as_view({'post': 'add_song'}), name='playlist-add-song'),
    
    # UserFollowing-related custom actions
    path('user-following/follow/', UserFollowingViewSet.as_view({'post': 'follow'}), name='user-follow'),
    path('user-following/unfollow/', UserFollowingViewSet.as_view({'post': 'unfollow'}), name='user-unfollow'),
]

# Logins
urlpatterns += [
    path('login/', login, name='login'),
    path('me/', get_profile, name='me'),
]

# urlpatterns += [
#     path('auth/google/', google_auth, name='google_auth'),
# ]



