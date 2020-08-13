from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from django.contrib.auth.models import *

def get_user_permissions(user):
    if user[0].is_superuser:
        return Permission.objects.all().values_list('id',flat=True)
    userID = user[0].id
    userPerms = Permission.objects.filter(user__id=userID).values_list('id',flat=True)
    groupPerms = Permission.objects.filter(group__user__id=userID).values_list('id',flat=True)
    return userPerms.union(groupPerms)

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        u_ser = serializer.validated_data['user']
        user = User.objects.filter(id=u_ser.id)
        token, created = Token.objects.get_or_create(user=u_ser)
        #print('user:', get_user_permissions(user))
        return Response({
            'token': token.key,
            'userID': u_ser.pk,
            'email': u_ser.email,
            'ime': u_ser.first_name,
            'prezime': u_ser.last_name,
            'permissions': get_user_permissions(user)
        })