from rest_framework import viewsets

from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class GetTokenViewSet(viewsets.ViewSet):
    def list(self, request):
        user = self.request.user
        print(user)
        if user is not None:
            try:
                token = Token.objects.get(user_id=user.id)

            except Token.DoesNotExist:
                token = Token.objects.create(user=user.id)

            return Response(token.key)
