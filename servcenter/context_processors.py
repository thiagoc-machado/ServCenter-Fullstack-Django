from config.models import Config

def project_settings(request):
    config = Config.objects.first()
    return {
        'config': config,
        # adicione outras configurações aqui
    }