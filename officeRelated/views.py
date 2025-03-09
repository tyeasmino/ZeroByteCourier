from rest_framework import viewsets
from .models import Location, Branch, Parcel
from .serializers import LocationSerializer, BranchSerializer, ParcelSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import FileResponse
from rest_framework.permissions import IsAuthenticated 
from rest_framework.exceptions import NotFound
import os


# Create your views here.
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class ParcelReceivingViewSet(viewsets.ModelViewSet):
    serializer_class = ParcelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        receiving_branch = Branch.objects.get(branch_incharge=user)
        return Parcel.objects.filter(receiving_branch=receiving_branch)

 
class ParcelViewSet(viewsets.ModelViewSet):
    serializer_class = ParcelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        sending_branch = Branch.objects.get(branch_incharge=user)
        return Parcel.objects.filter(sending_branch=sending_branch)
    

    def perform_create(self, serializer):
        user = self.request.user
        sending_branch = Branch.objects.get(branch_incharge=user)
        serializer.save(sending_branch = sending_branch)
    

    


@api_view(['GET'])
def parcel_status(request, tracking_number): 
    full_tracking_number = f"ZBT#{tracking_number}"

    try:
        parcel = Parcel.objects.get(tracking_number=full_tracking_number)
        return Response({"tracking_number": parcel.tracking_number, "status": parcel.parcel_status})
    except Parcel.DoesNotExist:
        raise NotFound(detail = "Parcel not found", code = 404)

