# Important part for API serialization

# https://www.django-rest-framework.org/api-guide/fields/

from rest_framework import serializers

class DataSerializer(serializers.Serializer):
    input_text1 = serializers.CharField(max_length=1000)
    input_text2 = serializers.CharField(max_length=1000)

# ----- After any change or add serializer field need to do database migrations -----
