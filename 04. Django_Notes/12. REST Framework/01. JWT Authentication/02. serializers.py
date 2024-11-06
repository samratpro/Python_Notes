from app.models import DataList
from rest_framework import serializers



# Serializer without Django Models
class GenerateTextSerializer(serializers.Serializer):
    input_text = serializers.CharField(max_length=1000


# Serializer for making post request to retrive data from django Model
class DataListSerializers(serializers.ModelSerializer):
    website_name = serializers.CharField(source='login_site.website_name', read_only=True)  # Data from Foreign Model
    class Meta:
        model = DataList
        # fields = '__all__'   # Return All Field 
        fields = ['id', 'website_name', 'login_link', 'username', 'password']  
        # makesure same field name, website_name comes from Foreign Model, 
        # otherwise we can use ` login_site ` but it will return Foreign model ` number `

