import math
from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from period_cycle_api.serializers.cycle_serializer import CycleSerializer
from period_cycle_api.models import PeriodCylceModel


class EstimateCycleView(APIView):
    serializer_class = CycleSerializer
    date_format = "%Y-%m-%d"

    def calculate_cycle(self, cycle_average, period_average, date_difference):
        if (cycle_average + period_average) < date_difference:
            result = date_difference/(cycle_average + period_average)
            return math.floor(result)
        elif(date_difference < 30 and date_difference > 0):
            return 1
        elif date_difference < 0:
            return 0

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        last_period_date = data.get('last_period_date', '')
        start_date = data.get('start_date', '')
        end_date = data.get('end_date', '')
        period_average = data.get('period_average', '')
        cycle_average = data.get('cycle_average', '')

        if serializer.is_valid():
            start_date_time_obj = datetime.strptime(
                start_date, self.date_format)
            end_date_time_obj = datetime.strptime(end_date, self.date_format)

            date_difference = end_date_time_obj - start_date_time_obj

            cycles = self.calculate_cycle(cycle_average=int(cycle_average), period_average=int(
                period_average), date_difference=date_difference.days)

            period_cycle_data = PeriodCylceModel.objects.create(
                last_period_date=last_period_date, start_date=start_date, end_date=end_date,
                cycle_average=cycle_average, period_average=period_average, total_created_cycle=cycles)

            period_cycle_data.save()
            return Response({"total_created_cycles": cycles}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
