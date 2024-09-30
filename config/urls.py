from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('new/', views.new_config, name='new_config'),
    path('', views.config, name="config"),
    path('edit/', views.edit_config, name="edit_config"),
    path('categoria_in/', views.categoria_in, name="categoria_in"),  # type: ignore
    path('categoria_out/', views.categoria_out, name="categoria_out"),  # type: ignore
    path('del_categoria_in/<int:id>', views.del_categoria_in, name="del_categoria_in"),
    path('del_categoria_out/<int:id>', views.del_categoria_out, name="del_categoria_out"),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
