from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name="master"

urlpatterns = [
    path('', views.redirect_to_dashboard, name='homepage'),
    path('dashboard', views.homepage, name='homepage'),

    # routes for province
    path('<slug:slug>/list', views.crud_list, name='crud_list'),
    path('<slug:slug>/list/filter', views.filter_crud_list, name='filter_crud_list'),
    path('<slug:slug>/create', views.crud_create_or_update, name='crud_create'),
    path('<slug:slug>/<int:id>/edit', views.crud_create_or_update, name='crud_update'),
    path('<slug:slug>/<int:id>/delete', views.crud_delete, name='crud_delete'),
    path('<slug:slug>/upload', views.upload, name='upload_file'),
    
    path('get-districts/<int:province_id>', views.get_districts, name='get_districts'),
    path('get-local-levels/<int:district_id>', views.get_local_levels, name='get_local_levels'),
    path('get-district-locallevel/<int:entry_id>', views.get_district_locallevel, name='get_district_locallevel'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
