from ACL.permissions import ROLE_CODES
from ACL.models import Role
from django.test import TestCase
from django.test import Client
from rest_framework.test import APIClient
from User.models import User


class MainTestMixin(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(phone='09396988720', password='admin')
        user = User.objects.create(phone='09396988730', password='user')
        user.set_password('test')
        user.save()
        self.user = user
        self.apiclient = APIClient()
        self.client = Client()
        teacher_role, _ = Role.objects.get_or_create(
            name="مدرس",
            code=ROLE_CODES.TEACHER,
        )
        student_role, _ = Role.objects.get_or_create(
            name="هنرجو",
            code=ROLE_CODES.STUDENT,
        )
