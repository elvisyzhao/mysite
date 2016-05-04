from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class MyBackend(ModelBackend):
    def authenticate(self, username=None, vericode=None, request=None):
        veri_code = request.get('veri_code', None)

