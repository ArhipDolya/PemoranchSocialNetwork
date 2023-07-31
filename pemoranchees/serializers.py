from rest_framework import serializers
from django.conf import settings

from .models import Pemoran

PEMORAN_ACTION_OPTIONS = settings.PEMORAN_ACTION_OPTIONS


class PemoranActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in PEMORAN_ACTION_OPTIONS:
            raise serializers.ValidationError('This action is not valid')
        else:   
            return value
        
        
class PemoranCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Pemoran
        fields = ['id', 'content', 'likes']

    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(value) > settings.MAX_CONTENT_LENGTH:
            raise serializers.ValidationError('This pemoran is very long')
        else:
            return value
        

class PemoranSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    parent = PemoranCreateSerializer(read_only=True)

    class Meta:
        model = Pemoran
        fields = ['id', 'content', 'likes', 'is_repemo', 'parent']

    def get_likes(self, obj):
        return obj.likes.count()