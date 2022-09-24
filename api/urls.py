from django.urls import path

from .views import ApartmentsView, RentalAgreement, Buildings

urlpatterns = [
    path("apartments/", ApartmentsView.as_view()),
    path("apartments/<int:pk>/", ApartmentsView.as_view()),
    path("buildings/", Buildings.as_view()),
    path("rental-agreement/<int:pk>/", RentalAgreement.as_view())
]
