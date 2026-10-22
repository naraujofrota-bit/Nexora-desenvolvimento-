from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from core.views import NexoraLoginView, dashboard, demand_create, demand_delete, demand_list

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", NexoraLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("demandas/", demand_list, name="demands"),
    path("demandas/nova/", demand_create, name="demand-create"),
    path("demandas/<int:pk>/excluir/", demand_delete, name="demand-delete"),
    path("", dashboard, name="dashboard"),
]
