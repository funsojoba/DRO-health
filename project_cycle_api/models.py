from django.db import models


class PeriodCylceModel(models.Model):
    last_period_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    cycle_average = models.IntegerField()
    period_average = models.IntegerField()
    total_created_cycle = models.DecimalField(max_digits=10, decimal_places=2)
