import string, random
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Location(models.Model):
    location_name = models.CharField(max_length = 50)
    slug = models.SlugField(max_length = 80)

    def __str__(self):
        return self.location_name


class Branch(models.Model):
    # Personal Details
    branch_incharge = models.OneToOneField(User, on_delete=models.CASCADE)
    branch_incharge_phone = models.CharField(max_length = 11, blank=True, null=True)

    # Branch Details
    branch_under_location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    branch_name = models.CharField(max_length = 50, blank=True, null=True)
    branch_phone = models.CharField(max_length = 11, blank=True, null=True)
    slug = models.SlugField(max_length = 80, blank=True, null=True)

    def __str__(self):
        return f"{self.branch_incharge.first_name} {self.branch_incharge.last_name} - {self.branch_name}"


PARCEL_STATUS_CHOICES = [
    ('On the way', 'On the way'),
    ('Arrived', 'Arrived'),
    ('Received', 'Received'),
    ('Delivered', 'Delivered'),
]


class Parcel(models.Model):
    # Sender Information 
    sender_name = models.CharField(max_length = 50)
    sender_phone = models.CharField(max_length = 11)
    sender_address = models.CharField(max_length = 100)
    sending_branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING, related_name="sending_branch", editable=False) 
    
    # Receiver Information 
    receiver_name = models.CharField(max_length = 50)     
    receiver_phone = models.CharField(max_length = 11)
    receiver_address = models.CharField(max_length = 100)
    receiving_branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING, related_name="receiving_branch",) 
    
    # Parcel Information
    tracking_number = models.CharField(max_length=20, unique=True, blank=True)
    parcel_type = models.CharField(max_length = 100)
    parcel_weight = models.DecimalField(max_digits=6, decimal_places=2)
    isHomeDelivery = models.BooleanField(default=False)
    parcel_bill = models.IntegerField()
    parcel_status = models.CharField(max_length=15, choices=PARCEL_STATUS_CHOICES, default='On the way')
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now_add=True) 
    isSoftDelete = models.BooleanField(default=False)
    estimated_delivery_time = models.DateTimeField(blank=True, null=True)
    
    def generate_tracking_number(self): 
        while True:
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            tracking_number = f"ZBT#{random_string}"    #ZBT - Zero Byte Tracking  
            if not Parcel.objects.filter(tracking_number=tracking_number).exists():
                return tracking_number


    def save(self, *args, **kwargs):
        if not self.sending_branch:
            self.sending_branch = self.sender.branch_incharge
            
        if self.isHomeDelivery:
            self.parcel_bill += 100
        
        if not self.tracking_number:  
            self.tracking_number = self.generate_tracking_number()

        if self.parcel_status in ['Received', 'Delivered']:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        


    def delete(self, *args, **kwargs):
        self.isSoftDelete = True
        self.save()


    def __str__(self):
        return f"{self.sending_branch.branch_name} - {self.tracking_number}"


 