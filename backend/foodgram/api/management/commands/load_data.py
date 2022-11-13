import json

from api.models import Ingredient
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('ingredients.json', 'rb') as ingredient:
            data = json.load(ingredient)
            for i in data:
                ingredient = Ingredient()
                ingredient.name = i['name']
                ingredient.measurement_unit = i['measurement_unit']
                ingredient.save()
                print(i['name'], i['measurement_unit'])
