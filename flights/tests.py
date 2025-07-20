from django.test import TestCase, Client
from django.db.models import Max
from django.urls import reverse
from .models import Flight, Passenger, Airport

# Create your tests here.
class FlightTest(TestCase):
    def setUp(self):
        a1 = Airport.objects.create(code='AAA', city='City A')
        a2 = Airport.objects.create(code='BBB', city='City B')

        Flight.objects.create(origin=a1, destination=a2, duration=200)
        Flight.objects.create(origin=a1, destination=a1, duration=100)
        Flight.objects.create(origin=a1, destination=a2, duration=-200)

    def test_departures_count(self):
        '''Check departures in City A are equal to 3''' 
        a = Airport.objects.get(code='AAA')
        self.assertEqual(a.departures.count(), 3)

    def test_arrivals_count(self):
        '''Check arrivals in City B are equal to 3''' 
        a = Airport.objects.get(code='BBB')
        self.assertEqual(a.arrivals.count(), 2)

    def test_is_valid_flight(self):
        '''Check that flight 1 is valid''' 
        a1 = Airport.objects.get(code='AAA')
        a2 = Airport.objects.get(code='BBB')
        f = Flight.objects.get(origin=a1, destination=a2, duration=200)
        self.assertTrue(f.is_valid_flight())

    def test_is_invalid_flight_destination(self):
        '''Check that flight 2 is not valid''' 
        a1 = Airport.objects.get(code='AAA')
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())
    
    def test_is_invalid_flight_duration(self):
        '''Check that flight 3 is not valid''' 
        a1 = Airport.objects.get(code='AAA')
        a2 = Airport.objects.get(code='BBB')
        f = Flight.objects.get(origin=a1, destination=a2, duration=-200)
        self.assertFalse(f.is_valid_flight())

    def test_index(self):
        c = Client()
        response = c.get('/flights/')
        self.assertTrue(response.status_code, 200)
        self.assertEqual(response.context["flights"].count(), 3)

    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code='AAA')
        a2 = Airport.objects.get(code='BBB')
        f = Flight.objects.get(origin=a1, destination=a2, duration=200)

        c = Client()
        url = reverse("flight", args=[f.id])    # reverse to figure out the correct path
        response = c.get(url)
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight_page(self):
        max_id = Flight.objects.all().aggregate(Max('id'))['id__max']

        c = Client()
        response = c.get(f'/flights/{max_id + 1} /')
        self.assertEqual(response.status_code, 404)

    def test_flight_page_passenger(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first='Mike', last='Hawk')
        f.passengers.add(p)

        c = Client()
        '''url = reverse("flight", args=[f.id])
        response = c.get(url)'''
        response = c.get(f'/flights/{f.id}')    # Hardcoded url
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['passengers'].count(), 1)

    def test_flight_page_nonpassenger(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first='Mike', last='Hawk')

        c = Client()
        url = reverse("flight", args=[f.id])
        response = c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['passengers'].count(), 0)
        self.assertEqual(response.context['non_passengers'].count(), 1)

