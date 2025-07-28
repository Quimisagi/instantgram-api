from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Post
from .serializer import UserSerializer, PostSerializer
from django.utils.dateparse import parse_date


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        # Hash password before saving
        password = serializer.validated_data['password']
        serializer.save(password=make_password(password))


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                return Response({'id': user.id, 'username': user.username})
            else:
                return Response({'error': 'Invalid password'}, status=400)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request

        # Author filter
        author_id = request.query_params.get('author')
        if author_id and author_id.isdigit():
            queryset = queryset.filter(author_id=int(author_id))

        # Category filter
        category_name = request.query_params.get('category')
        if category_name:
            queryset = queryset.filter(categories__name__iexact=category_name)

        # Exact date filter
        date = request.GET.get("date")
        if date:
            parsed_date = parse_date(date)
            if parsed_date:
                queryset = queryset.filter(date=parsed_date)

        queryset = queryset.order_by('-date', '-id')

        return queryset
