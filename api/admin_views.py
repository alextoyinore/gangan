from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import User, Song, Album, Artist

@staff_member_required
def dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'total_songs': Song.objects.count(),
        'total_albums': Album.objects.count(),
        'total_artists': Artist.objects.count(),
    }
    return render(request, 'admin/dashboard.html', context)
