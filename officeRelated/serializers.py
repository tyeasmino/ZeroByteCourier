from rest_framework import serializers
from .models import Location, Branch, Parcel


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
    


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

    

class ParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = '__all__'

    # def validate_receiving_branch(self, value):
    #     user = self.context['request'].user
    #     senderbranch = Branch.objects.get(branch_incharge=user)
    #     if value == senderbranch:
    #         raise serializers.ValidationError("You cannot set the receiving branch to your branch")
    #     return value

