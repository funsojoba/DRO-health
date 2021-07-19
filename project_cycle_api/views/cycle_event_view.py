import math
from datetime import datetime, timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from period_cycle_api.models import PeriodCylceModel
from period_cycle_api.serializers.event_serializer import EventSerializer


class CycleEvent(APIView):
    serializer_class = EventSerializer
    db_data = PeriodCylceModel.objects.get(id=1)

    last_period_date = db_data.last_period_date
    start_date = db_data.start_date
    end_date = db_data.end_date
    cycle_average = db_data.cycle_average
    period_average = db_data.period_average
    total_created_cycle = db_data.total_created_cycle

    def get(self, request):
        date = request.GET.get('date')
        
        if date:
            period_start_date = datetime.strptime(
                str(self.last_period_date), "%Y-%m-%d")

            start_end_day_diff = self.end_date - self.start_date

            # List of numbers from the time range
            cycle_list = [i for i in range(1, start_end_day_diff.days + 1) if i % (
                int(self.cycle_average) + int(self.period_average)) == 0]
            cycle_date_list = [str(self.last_period_date + timedelta(days=i)) for i in cycle_list]

            # get the list of ovulation dates
            ovulation_list = [math.floor(
                i + (self.cycle_average / 2)) for i in cycle_list]
            ovulation_date_list = [str(self.start_date + timedelta(days=i)) for i in ovulation_list]

            # get the list of fertility window dates
            fertility_window = []
            for i in cycle_list:
                fertility_window.append(str(self.start_date + timedelta(days=i + self.period_average + 4)))
                fertility_window.append(str(self.start_date + timedelta(days=i - 4)))

            events_dict = {
                "fertility_window": fertility_window,
                "ovulation_period": ovulation_date_list,
                "mestral_cycle_starts": cycle_date_list
            }

            answer_dict = {}
            if date in fertility_window:
                answer_dict['event'] = "fertility window"
                answer_dict["date"] = date
            elif date in ovulation_date_list:
                answer_dict['event'] = "ovulation period"
                answer_dict["date"] = date
            elif date in cycle_date_list:
                answer_dict['event'] = "mentral cycle starts"
                answer_dict["date"] = date
            else:
                answer_dict["event"] = "No event for this date"
                answer_dict["date"] = date

            return Response([answer_dict])
        return Response({"error":"Please input a valid date"}, status=status.HTTP_400_BAD_REQUEST)
