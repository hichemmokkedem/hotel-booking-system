from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from datetime import date
from .models import Hotel, Room, Reservation
from .serializers import HotelSerializer, RoomSerializer, ReservationSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    
    def get_queryset(self):
        queryset = Hotel.objects.all()
        destination = self.request.query_params.get('destination', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)

        if destination:
            queryset = queryset.filter(address__icontains=destination)
        if min_price:
            queryset = queryset.filter(rooms__price_per_night__gte=min_price).distinct()
        if max_price:
            queryset = queryset.filter(rooms__price_per_night__lte=max_price).distinct()
            
        return queryset
    
    def get_permissions(self):
        # Allow anyone to read (list, retrieve), but only staff can create/update/delete
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    
    def get_queryset(self):
        queryset = Room.objects.all()
        
        # Filter by destination (Hotel address)
        destination = self.request.query_params.get('destination', None)
        if destination:
            queryset = queryset.filter(hotel__address__icontains=destination)
            
        # Filter by price range
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        
        if min_price:
            queryset = queryset.filter(price_per_night__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)
            
        return queryset
    
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        room = self.get_object()
        reservations = Reservation.objects.filter(room=room, check_out__gte=date.today())
        booked_dates = [
            {'check_in': r.check_in, 'check_out': r.check_out} 
            for r in reservations
        ]
        return Response(booked_dates)

    def get_permissions(self):
        # Allow anyone to read, but only staff can create/update/delete
        if self.action in ['list', 'retrieve', 'availability']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            if self.request.user.is_staff:
                return Reservation.objects.all()
            return Reservation.objects.filter(user=self.request.user)
        except Exception as e:
            print(f"Error in ReservationViewSet.get_queryset: {e}")
            raise e

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
