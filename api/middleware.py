from django.http import HttpResponse
from django.core.cache import cache
from django.conf import settings

class APIRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):
            ip = request.META.get('REMOTE_ADDR')
            key = f'rate_limit_{ip}'
            requests = cache.get(key, 0)
            
            if requests >= settings.API_RATE_LIMIT:
                return HttpResponse('Rate limit exceeded', status=429)
            
            requests += 1
            cache.set(key, requests, 60)  # Reset after 60 seconds

        response = self.get_response(request)
        return response
    
