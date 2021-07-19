from django.db import models
from rest_framework import serializers

from period_cycle_api.models import PeriodCylceModel


class CycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodCylceModel
        fields = ['last_period_date', 'start_date','end_date',
                  'cycle_average', 'period_average']
