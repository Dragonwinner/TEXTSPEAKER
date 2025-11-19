from rest_framework import serializers


class GenerateVideoSerializer(serializers.Serializer):
    text = serializers.CharField()
