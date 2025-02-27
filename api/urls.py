'''
Create:
HTTP Method: POST
URL: /api/modelname/

Retrieve (single instance):
HTTP Method: GET
URL: /api/modelname/{slug}/

Update:
HTTP Method: PUT (full update) or PATCH (partial update)
URL: /api/modelname/{slug}/

4. Delete:
HTTP Method: DELETE
URL: /api/modelname/{slug}/

List (multiple instances):
HTTP Method: GET
URL: /api/modelname/

Here's a breakdown for each model:

1. Users:
Create: POST to /api/users/
Retrieve: GET to /api/users/{slug}/
Update: PUT/PATCH to /api/users/{slug}/
Delete: DELETE to /api/users/{slug}/
List: GET to /api/users/

Artists:
Create: POST to /api/artists/
Retrieve: GET to /api/artists/{slug}/
Update: PUT/PATCH to /api/artists/{slug}/
Delete: DELETE to /api/artists/{slug}/
List: GET to /api/artists/

Albums:
Create: POST to /api/albums/
Retrieve: GET to /api/albums/{slug}/
Update: PUT/PATCH to /api/albums/{slug}/
Delete: DELETE to /api/albums/{slug}/
List: GET to /api/albums/

Songs:
Create: POST to /api/songs/
Retrieve: GET to /api/songs/{slug}/
Update: PUT/PATCH to /api/songs/{slug}/
Delete: DELETE to /api/songs/{slug}/
List: GET to /api/songs/

Playlists:
Create: POST to /api/playlists/
Retrieve: GET to /api/playlists/{slug}/
Update: PUT/PATCH to /api/playlists/{slug}/
Delete: DELETE to /api/playlists/{slug}/
List: GET to /api/playlists/

'''


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ArtistViewSet, AlbumViewSet, SongViewSet, PlaylistViewSet,
    GenreViewSet, UserActivityViewSet, SubscriptionViewSet, UserPreferencesViewSet,
    RadioViewSet, PodcastViewSet, PodcastEpisodeViewSet, UserFollowingViewSet,
    SongRatingViewSet, LibraryViewSet, FavouriteViewSet, APIDocsView, UserAPIDocsView,
)
from .views import login, get_profile, logout


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
router.register(r'library', LibraryViewSet)
router.register(r'favourites', FavouriteViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

# Custom action URL patterns
urlpatterns += [
    # User-related custom actions
    path('users/<slug:slug>/playlists/', UserViewSet.as_view({'get': 'playlists'}), name='user-playlists'),
    path('users/<slug:slug>/favourites/', UserViewSet.as_view({'get': 'favourites'}), name='user-favourites'),
    path('users/<slug:slug>/library/', UserViewSet.as_view({'get': 'library'}), name='user-library'),
    path('users/<slug:slug>/activity/', UserViewSet.as_view({'get': 'activity'}), name='user-activity'),
    
    # Artist-related custom actions
    path('artists/<slug:slug>/albums/', ArtistViewSet.as_view({'get': 'albums'}), name='artist-albums'),
    path('artists/<slug:slug>/songs/', ArtistViewSet.as_view({'get': 'songs'}), name='artist-songs'),
    
    # Album-related custom actions
    path('albums/<slug:slug>/songs/', AlbumViewSet.as_view({'get': 'songs'}), name='album-songs'),
    
    # Song-related custom actions
    path('songs/<slug:slug>/rate/', SongViewSet.as_view({'post': 'rate'}), name='song-rate'),
    
    # Playlist-related custom actions
    path('playlists/<slug:slug>/add-song/', PlaylistViewSet.as_view({'post': 'add_song'}), name='playlist-add-song'),
    
    # UserFollowing-related custom actions
    path('user-following/follow/', UserFollowingViewSet.as_view({'post': 'follow'}), name='user-follow'),
    path('user-following/unfollow/', UserFollowingViewSet.as_view({'post': 'unfollow'}), name='user-unfollow'),
]

# Logins
urlpatterns += [
    path('login/', login, name='login'),
    path('me/', get_profile, name='me'),
    path('logout/', logout, name='logout'),
    path('docs/', APIDocsView.as_view(), name='api-docs'),
    path('docs/user/', UserAPIDocsView.as_view(), name='user-api-docs'),
]

# urlpatterns += [
#     path('auth/google/', google_auth, name='google_auth'),
# ]

