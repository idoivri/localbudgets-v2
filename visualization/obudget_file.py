from django.core.management.base import BaseCommand
from server.models import get_flatten
from settings import STATICFILES_DIRS
from os.path import join
from server.utils.json_serialize import dumps

class ObudgetCommand(BaseCommand):
    def handle(self, *args, **options):
        print "bla for the win"
        with open(join(STATICFILES_DIRS[0], 'obudget'), 'w') as f:
            for item in get_flatten().find():
                f.write(dumps(item) + '\n')

