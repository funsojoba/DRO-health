from django.urls import path

from period_cycle_api.views.cycle_view import EstimateCycleView
from period_cycle_api.views.cycle_event_view import CycleEvent

urlpatterns = [
    path('create-cycles/', EstimateCycleView.as_view(), name="create-cycles"),
    path('cycle-event/', CycleEvent.as_view(), name="cycle_event"),
    ]
