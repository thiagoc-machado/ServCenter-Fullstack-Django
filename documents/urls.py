from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.documents, name="documents"),
    path('del_documents/<int:id>', views.del_documents, name='del_documents'),
     path('documents/download_documents/<int:id>', views.download_documents, name='download_documents'),
    path('view_documents/<int:id>', views.view_documents, name='view_documents')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
