from rest_framework import serializers
from django.conf import settings

from .models import Pemoran

class PemoranSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pemoran
        fields = ['content']

    def validate_content(self, value):
        if len(value) > settings.MAX_CONTENT_LENGTH:
            raise serializers.ValidationError('This pemoran is very long')
        else:
            return value