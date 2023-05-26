from urllib import response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.postgres.aggregates import ArrayAgg

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .permissions import IsAdminUserPermission
from .models import Role
from .serializer import UserSerializer

User = get_user_model()


class UserList(APIView):
    """
    GET ALL User list and add new roles to other user
    """
    model = User
    permission_classes = (IsAdminUserPermission, )
    authentication_classes = (TokenAuthentication, )

    def get(self, request):
        users = self.model.objects.filter(status='active').annotate(
                role_names = ArrayAgg(
                    'roles__role_name', distinct=True
                )
            ).exclude(id=request.user.id).values(
            'id', 'username', 'email', 'role_names'
        )
        return Response(
            {'message': 'All users data',
            'data': users
            },
            status= status.HTTP_200_OK
        )
    
    def post(self, request):
        data = request.data
        user_id = data.get('user')
        role = data.get('role')
        if not (user_id or role):
            return Response(
                {
                    'message': 'User And Role Details Required'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        user_obj = get_object_or_404(User, id=user_id)
        role = get_object_or_404(Role, id=role)
        if role.id not in user_obj.roles.all().values_list('id', flat=True):
            user_obj.roles.add(role.id)
            message = 'role addeed'
        else:
            user_obj.roles.remove(role.id)
            message = 'role removed'
        user_obj.save()
        return Response(
            {
                'message': message
            },
            status=status.HTTP_200_OK
        )

class UserCreation(APIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    
    def post(self, request):
        data = request.POST
        print(data)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'User created Sucessfully',
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

class UserDetails(APIView):
    model = User
    serializer = UserSerializer
    authentication_classes = [TokenAuthentication,]
    
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if user_id is None:
            user_id = request.user.id
        print(user_id)
        user_obj = get_object_or_404(User, id=user_id)
        ser = self.serializer(user_obj, many=False)
        return Response(
            {
                'data': ser.data
            },
            status=status.HTTP_200_OK
        )
