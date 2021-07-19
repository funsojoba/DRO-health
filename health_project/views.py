from django.http import JsonResponse


def index(request):
    message = 'Welcome to Period Cycle Rest API. Visit /womens-health/api'
    return JsonResponse(dict(message=message))
