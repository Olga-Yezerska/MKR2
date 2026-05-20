
# Create your tests here.
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Recipe


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Desserts')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Desserts')

    def test_category_iter(self):
        Recipe.objects.create(
            title='Cake', description='A cake', instructions='Bake it',
            ingredients='Flour, eggs', category=self.category
        )
        recipes = list(self.category)
        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipes[0].title, 'Cake')


class RecipeModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Soups')
        self.recipe = Recipe.objects.create(
            title='Borsch',
            description='Classic Ukrainian soup',
            instructions='Cook beets, add cabbage...',
            ingredients='Beets, cabbage, carrots',
            category=self.category
        )

    def test_recipe_str(self):
        self.assertEqual(str(self.recipe), 'Borsch')

    def test_recipe_has_category(self):
        self.assertEqual(self.recipe.category, self.category)

    def test_recipe_created_at(self):
        self.assertIsNotNone(self.recipe.created_at)

    def test_recipe_updated_at(self):
        self.assertIsNotNone(self.recipe.updated_at)


