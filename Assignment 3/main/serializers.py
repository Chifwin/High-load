from rest_framework import serializers
from main.models import KeyValue


class KeyValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyValue
        fields = ['key', 'value']
