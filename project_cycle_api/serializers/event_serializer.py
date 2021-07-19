from rest_framework import serializers


class EventSerializer(serializers.Serializer):
    event_date = serializers.DateField()