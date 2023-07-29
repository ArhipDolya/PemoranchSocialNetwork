from rest_framework import serializers
from django.conf import settings

from .models import Pemoran

PEMORAN_ACTION_OPTIONS = settings.PEMORAN_ACTION_OPTIONS

class PemoranSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pemoran
        fields = ['content']

    def validate_content(self, value):
        if len(value) > settings.MAX_CONTENT_LENGTH:
            raise serializers.ValidationError('This pemoran is very long')
        else:
            return value

class PemoranActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validation_action(self, value):
        value = value.lower().strip()
        if not value in PEMORAN_ACTION_OPTIONS:
            raise serializers.ValidationError('This action is not valid')
        else:
            return value