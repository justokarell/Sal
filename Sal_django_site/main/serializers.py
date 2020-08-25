from rest_framework import serializers
from .models import UserPost, DonorPost, RecipientPost, Availability

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ('assigned_post','post_day','start_min','end_min',)

class UserPostSerializer(serializers.ModelSerializer):
    availability_set = AvailabilitySerializer(many=True, read_only=True)
    class Meta:
        model = UserPost
        fields = ('post_title','post_lat','post_long','post_deliver','donor_or_recip', 'post_desc', 'availability_set')

class DonorPostSerializer(serializers.ModelSerializer):
    # foreignModel2 = MModelSerializer(many=True) # as it is many to many field
    class Meta:
        model = DonorPost
        fields =  '__all__'

class RecipientPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipientPost
        fields =  '__all__'




