import logging
from urllib.parse import urlencode

import requests
from django.conf import settings as cfg
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from app.handlers import UserHandler, MagicLinkHandler
from app.models import User, MagicLinkAuth

log = logging.getLogger(__name__)


class LogIn(APIView):
    def get(self, request, magic_link):
        general_error = JsonResponse({"error": "wrong link"}, status=404)

        try:
            magic_link_auth = MagicLinkAuth.objects.get(token=magic_link)
        except MagicLinkAuth.DoesNotExist:
            return general_error

        magic_link = MagicLinkHandler(magic_link_auth)
        if not magic_link.validate():
            return general_error

        return JsonResponse(magic_link.get_info())


class CreateLink(APIView):
    def get(self, request, email):
        user = UserHandler(email).get_user()
        magic_link_auth = MagicLinkAuth(user=user)

        magic_link = MagicLinkHandler(magic_link_auth).generate_link()

        return JsonResponse({"magiclink": f"http://{request.get_host()}/login/{magic_link}"})

