from django.core.management import BaseCommand
from acl.models import *
from acl.permissions import PERMISSIONS, ROLE_CODES

LAB_ADMIN_PERMS = [
    'appointment_list',
    'appointment_create',
    'appointment_edit',
    'appointment_delete',

    'role_list',
    'role_create',
    'role_edit',
    'role_delete',

    'doctors_list',
    'doctors_create',
    'doctors_edit',
    'doctors_delete',
]


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='clear old states and cities',
        )

    def handle(self, *args, **options):
        if options['clear']:
            Role.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f"CLEAR"))

        role, created = Role.objects.update_or_create(name='ادمین آزمایشگاه', code=ROLE_CODES.DOCTOR)
        role.permissions.set(Permission.objects.filter(code__in=LAB_ADMIN_PERMS))

        self.stdout.write(self.style.SUCCESS(f"DONE..."))
