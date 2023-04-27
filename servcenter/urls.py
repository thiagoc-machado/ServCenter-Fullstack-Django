
from django import views
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("login.urls")),
    path('dashboard/', include("dashboard.urls")),
    path('clients/', include("clients.urls")),
    path('users/', include("users.urls")),
    path('employees/', include("employees.urls")),
    path('services/', include("services.urls")),
    path('work_order/', include("work_order.urls")),
    path('finance/', include("finance.urls")),
    path('finance_dia/', include("finance.urls")),
    path('backup/', include("backup.urls")),
    path('config/', include("config.urls")),
    path('documents/', include("documents.urls")),
]# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def handle_404(request, exception):
    return redirect('dashboard')

handler404 = 'servcenter.urls.handle_404'