from django.urls import path
from .views import request_reservation, verify_identity, reservation_success


app_name = "events"

urlpatterns = [
    path('reserve/', request_reservation, name='request_reservation'),
    path('verify/', verify_identity, name='verify_identity'),
    path('success/<int:reservation_id>/', reservation_success, name='reservation_success'),
]
