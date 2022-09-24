from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import Apartment
import json
from datetime import datetime
from django.db.models import Sum, Avg, Count


class ApartmentsView(View):
    def get_request_body(self, request):
        return json.loads(request.body)

    def get(self, request):
        apartments = Apartment.objects.all()
        serialized_data = [apartment.serialize() for apartment in apartments]
        return JsonResponse(serialized_data, safe=False)

    def post(self, request):
        data = self.get_request_body(request)
        new_apartment = Apartment.objects.create(**data)
        new_apartment.save()
        return JsonResponse(data, safe=False)

    def put(self, request, pk):
        data = self.get_request_body(request)
        apartment = Apartment.objects.filter(id=pk)
        apartment.update(**data)
        return JsonResponse(apartment[0].serialize(), safe=False)

    def delete(self, request, pk):
        apartment = Apartment.objects.get(id=pk)
        apartment.delete()
        return HttpResponse('<h1>apartment deleted</h1>')


class Buildings(View):
    """
    Create buildings based on apartment location
        if apartments share the same city, street and street_number
        or alternatively share the same latitude and longitude
        then they can be grouped into a single building
    """

    def get(self, request):
        apartments = Apartment.objects.values(
            'city', 'street', 'street_number'
        ).annotate(
            average_rent_per_apartment=Avg('rent'),
            total_number_of_rooms=Sum('rooms'),
            total_area_of_apartments=Sum('area'),
            total_apartments_in_building=Count('id')
        )
        result = [apartment for apartment in apartments]
        return JsonResponse(result, safe=False)


class RentalAgreement(View):
    def get(self, request, pk):
        apartment = Apartment.objects.get(id=pk)
        return HttpResponse(self.get_rental_agreement(apartment))

    @staticmethod
    def get_rental_agreement(apartment):
        return f'''
            <h2>Rental Agreement</h2>
        
            <p>The Property is located at {apartment.street_number} {apartment.street}
            in the city of {apartment.city}.</p>

            <p>The Tenant shall pay the Landlord the monthly rent of {apartment.rent}.</p>

            <p>The apartment contains {apartment.rooms} rooms and its area is {apartment.area}.</p>

            <h3>Signature: ................</h3>
            <h3>Date: {datetime.today().strftime('%d-%m-%Y')}</h3>
        '''
