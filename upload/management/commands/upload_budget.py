from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kws):
        print "bla for the win"
