from django.core.management import BaseCommand
from acl.models import *
from acl.permissions import PERMISSIONS


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='clear old states and cities',
        )

    def handle(self, *args, **options):
        if options['clear']:
            Permission.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f"CLEAR"))

        perms = []
        [[perms.append(f) for f in item['permissions']] for item in PERMISSIONS]

        for item in perms:
            permission, created = Permission.objects.get_or_create(
                code=item['code']
            )
            permission.name = item['name']
            permission.description = item['description']
            permission.save()

        print('Done...')
