from .models import Config

def conf(request):
    logo = Config.objects.all().first
 
    return {'logo': logo}
