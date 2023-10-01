from django.urls import path

from . import views

app_name = "t_photo_app"
urlpatterns = [
    path("index", views.index, name=""),
    path("image_detection", views.image_detection, name=""),
    path("emotion", views.emotion, name=""),
    path("info", views.info, name=""),
    path("intro", views.intro, name=""),
    path("contact", views.contact, name=""),
    path("manage_login", views.manage_login, name=""),
    path("manage_logout", views.manage_logout, name=""),
    path("manage_data", views.manage_data, name=""),
    path("introdata_add", views.introdata_add, name=""),
    path("introdata_edit", views.introdata_edit, name=""),
    path("introdata_delete", views.introdata_delete, name=""),
    path("infodata_add", views.infodata_add, name=""),
    path("infodata_edit", views.infodata_edit, name=""),
    path("infodata_delete", views.infodata_delete, name=""),
]