from django.urls import path

from . import views

app_name="department"

urlpatterns = [
    path('departments/', views.DepartmentViewSet.as_view(
        {'get': 'list', 'post': 'create'}), name='posts-all'),
    path('departments/<pk>/', views.DepartmentViewSet.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
    ), name="single-post"),
    path("single-department/", views.DepartmentAPIView.as_view(), name="single departmen"),
    path('departments/<pk>/reviews/', views.ReviewViewSet.as_view(
        {'get': 'list', "post": "create"}), name='reviews-all'),
    path('departments/<pk>/reviews/<id>/', views.ReviewViewSet.as_view(
        {'get': 'retrieve', "put": "update",
         "delete": "destroy", "post": "create_reply"}), name='single-comment'),
    path('rate/<id>/', views.RatingAPIView.as_view(), name='rating'),

]
