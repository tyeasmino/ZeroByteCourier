from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LocationViewSet, BranchViewSet, ParcelViewSet, ParcelReceivingViewSet, parcel_status  


router = DefaultRouter()
router.register(r'locations', LocationViewSet)
router.register(r'branches', BranchViewSet)
router.register(r'parcels', ParcelViewSet, basename='parcels')
router.register(r'parcels-receiving', ParcelReceivingViewSet, basename='parcels-receiving')

urlpatterns = [
    path('', include(router.urls)), 
    path('tracking/<str:tracking_number>/', parcel_status, name='tracking'),
]

