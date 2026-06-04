from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Hotel, Room, Reservation
from .serializers import UserSerializer
from datetime import date, timedelta

class HotelModelTest(TestCase):
    def setUp(self):
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            description="A test hotel",
            address="123 Test St",
            rating=4.5
        )

    def test_hotel_creation(self):
        """Test that a hotel instance is correctly created."""
        self.assertEqual(self.hotel.name, "Test Hotel")
        self.assertEqual(str(self.hotel), "Test Hotel")

class RoomModelTest(TestCase):
    def setUp(self):
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            description="A test hotel",
            address="123 Test St",
            rating=4.5
        )
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_number="101",
            room_type="SINGLE",
            price_per_night=100.00,
            capacity=1
        )

    def test_room_creation(self):
        """Test that a room is correctly linked to a hotel."""
        self.assertEqual(self.room.room_number, "101")
        self.assertEqual(self.room.hotel, self.hotel)

class HotelAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hotel = Hotel.objects.create(
            name="API Hotel",
            description="Testing API",
            address="456 API Ave",
            rating=5.0
        )
        self.url = reverse('hotel-list')

    def test_get_hotels(self):
        """Test retrieving the list of hotels."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

class ReservationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser_res', password='password')
        self.client.force_authenticate(user=self.user)
        
        self.hotel = Hotel.objects.create(name="Res Hotel", address="Test Addr", rating=4)
        self.room = Room.objects.create(hotel=self.hotel, room_number="202", price_per_night=100.0, capacity=2)
        
    def test_create_reservation(self):
        """Test creating a valid reservation via API"""
        check_in = date.today() + timedelta(days=1)
        check_out = date.today() + timedelta(days=3)
        data = {
            'room': self.room.id,
            'check_in': check_in,
            'check_out': check_out
        }
        url = reverse('reservation-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Reservation.objects.first().user, self.user)
        
    def test_reservation_validation(self):
        """Test that check-out cannot be before check-in"""
        check_in = date.today() + timedelta(days=5)
        check_out = date.today() + timedelta(days=2) # Invalid: checkout before checkin
        data = {
            'room': self.room.id,
            'check_in': check_in,
            'check_out': check_out
        }
        url = reverse('reservation-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class AvailabilityTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hotel = Hotel.objects.create(name="Avail Hotel", address="Test Addr", rating=4)
        self.room = Room.objects.create(hotel=self.hotel, room_number="303", price_per_night=100.0, capacity=2)
        self.user = User.objects.create_user(username='testuser_avail', password='password')
        
        # Create a manually existing reservation
        self.check_in = date.today() + timedelta(days=10)
        self.check_out = date.today() + timedelta(days=15)
        Reservation.objects.create(
            user=self.user,
            room=self.room,
            check_in=self.check_in,
            check_out=self.check_out
        )

    def test_room_availability(self):
        """Test the custom action availability endpoint"""
        # The URL for custom action 'availability' on 'room' ViewSet is likely 'room-availability'
        url = reverse('room-availability', args=[self.room.id]) 
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return list of booked dates
        self.assertEqual(len(response.data), 1)
        # response date format is string 'YYYY-MM-DD'
        self.assertEqual(response.data[0]['check_in'], self.check_in)
        # Note: self.check_in is date object, response.data keeps it as object in TestClient

class LogoutTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='logoutuser', password='password')
        self.url = reverse('auth_logout')
        self.login_url = reverse('token_obtain_pair')

    def test_logout(self):
        """Test that logout blacklists the refresh token."""
        # 1. Login to get tokens
        resp_login = self.client.post(self.login_url, {'username': 'logoutuser', 'password': 'password'})
        refresh_token = resp_login.data['refresh']
        access_token = resp_login.data['access']

        # 2. Authenticate and Logout
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        resp_logout = self.client.post(self.url, {'refresh_token': refresh_token})
        
        self.assertEqual(resp_logout.status_code, status.HTTP_205_RESET_CONTENT)

        # 3. Try to use blacklisted token (Verify it fails)
        refresh_url = reverse('token_refresh')
        resp_refresh = self.client.post(refresh_url, {'refresh': refresh_token})
        self.assertEqual(resp_refresh.status_code, status.HTTP_401_UNAUTHORIZED)

class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('auth_register')
        self.me_url = reverse('current_user')
        self.user_data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'new@example.com',
            'date_of_birth': '2000-01-01'
        }

    def test_register_user(self):
        """Test user registration endpoint"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_current_user(self):
        """Test retrieving current authenticated user details"""
        user = User.objects.create_user(username='meuser', password='password')
        self.client.force_authenticate(user=user)
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'meuser')

class FilterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hotel1 = Hotel.objects.create(name="Paris Hotel", address="Paris, France", rating=5)
        self.hotel2 = Hotel.objects.create(name="London Hotel", address="London, UK", rating=4)
        
        self.room1 = Room.objects.create(hotel=self.hotel1, room_number="101", price_per_night=200.00, capacity=2)
        self.room2 = Room.objects.create(hotel=self.hotel2, room_number="102", price_per_night=100.00, capacity=2)

    def test_filter_hotel_by_destination(self):
        """Test filtering hotels by destination (address)"""
        url = reverse('hotel-list')
        response = self.client.get(url, {'destination': 'Paris'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Paris Hotel')

    def test_filter_room_by_price(self):
        """Test filtering rooms by price range"""
        url = reverse('room-list')
        # Filter rooms cheaper than or equal to 150
        response = self.client.get(url, {'max_price': 150})
        self.assertEqual(len(response.data), 1)
        # DRF DecimalField usually returns string, adapt if necessary
        self.assertEqual(float(response.data[0]['price_per_night']), 100.00)

class PermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='regular', password='password')
        self.admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='password')
        self.hotel_url = reverse('hotel-list')
        self.hotel_data = {
            'name': 'New Hotel', 
            'address': 'New Place', 
            'description': 'Desc', 
            'rating': 3
        }

    def test_regular_user_cannot_create_hotel(self):
        """Test that a regular user cannot create a hotel"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.hotel_url, self.hotel_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_hotel(self):
        """Test that an admin user can create a hotel"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.hotel_url, self.hotel_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class AdvancedReservationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_a = User.objects.create_user(username='userA', password='password')
        self.user_b = User.objects.create_user(username='userB', password='password')
        self.admin = User.objects.create_superuser(username='admin_adv', email='admin@test.com', password='password')
        
        self.hotel = Hotel.objects.create(name="Advanced Hotel", address="Test Addr", rating=5)
        self.room = Room.objects.create(hotel=self.hotel, room_number="505", price_per_night=100.0, capacity=2)
        
        # Create initial reservation for User A
        self.check_in = date.today() + timedelta(days=1)
        self.check_out = date.today() + timedelta(days=5)
        self.reservation_a = Reservation.objects.create(
            user=self.user_a,
            room=self.room,
            check_in=self.check_in,
            check_out=self.check_out
        )
        self.url_list = reverse('reservation-list')
        self.url_detail = reverse('reservation-detail', args=[self.reservation_a.id])

    def test_double_booking_prevention(self):
        """Ensure overlapping reservations are rejected."""
        self.client.force_authenticate(user=self.user_b)
        
        # Overlap case 1: Inside existing booking
        data = {
            'room': self.room.id,
            'check_in': self.check_in + timedelta(days=1),
            'check_out': self.check_out - timedelta(days=1)
        }
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Overlap case 2: Exact Match
        data = {
            'room': self.room.id,
            'check_in': self.check_in,
            'check_out': self.check_out
        }
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reservation_privacy_user_b(self):
        """User B should not see User A's reservation."""
        self.client.force_authenticate(user=self.user_b)
        
        # List check
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should be empty for User B
        self.assertEqual(len(response.data), 0)
        
        # Detail check (should be 404 because get_queryset filters it out)
        response = self.client.get(self.url_detail)
        # Typically 404 if not found in queryset, or 403 if found but denied. 
        # Since get_queryset filters by user, it won't be found -> 404.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_reservation_visibility_admin(self):
        """Admin should see all reservations."""
        self.client.force_authenticate(user=self.admin)
        
        # List check
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)
        
        # Detail check
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.reservation_a.id)

class UserSerializerTest(TestCase):
    def test_validate_age(self):
        """Test that users under 18 cannot register"""
        data = {
            'username': 'younguser',
            'email': 'young@test.com',
            'password': 'password123',
            'date_of_birth': date.today() - timedelta(days=365*17) # 17 years old
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('date_of_birth', serializer.errors)

class AdminPermissionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='reguser', password='password')
        self.admin = User.objects.create_superuser(username='adminuser', email='admin@test.com', password='password')
        self.hotel = Hotel.objects.create(name="Delete Me Hotel", address="Address", rating=1)

    def test_delete_hotel_permission(self):
        url = reverse('hotel-detail', args=[self.hotel.id])
        
        # Regular user -> 403
        self.client.force_authenticate(user=self.user)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin -> 204
        self.client.force_authenticate(user=self.admin)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

class ReservationSecurityTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='u1', password='password')
        self.user2 = User.objects.create_user(username='u2', password='password')
        self.hotel = Hotel.objects.create(name="H", address="A", rating=5)
        self.room = Room.objects.create(hotel=self.hotel, room_number="1", price_per_night=100, capacity=2)
        
        self.res1 = Reservation.objects.create(
            user=self.user1, 
            room=self.room, 
            check_in=date.today()+timedelta(days=1),
            check_out=date.today()+timedelta(days=2)
        )
        self.url_detail = reverse('reservation-detail', args=[self.res1.id])

    def test_user_cannot_access_other_reservation(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.url_detail)
        # Should be 404 because get_queryset filters it out
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_access_own_reservation(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
