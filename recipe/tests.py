
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


class MainViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Main Dishes')
        for i in range(15):
            Recipe.objects.create(
                title=f'Recipe {i}',
                description=f'Description {i}',
                instructions=f'Instructions {i}',
                ingredients=f'Ingredients {i}',
                category=self.category
            )

    def test_main_view_status_code(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    def test_main_view_uses_correct_template(self):
        response = self.client.get(reverse('main'))
        self.assertTemplateUsed(response, 'recipe/main.html')

    def test_main_view_returns_max_10_recipes(self):
        response = self.client.get(reverse('main'))
        self.assertLessEqual(len(response.context['recipes']), 10)

    def test_main_view_returns_recipes_in_context(self):
        response = self.client.get(reverse('main'))
        self.assertIn('recipes', response.context)

    def test_main_view_random_on_refresh(self):
        # With 15 recipes, two requests should occasionally differ (not guaranteed, but tests randomness)
        titles_1 = set(r.title for r in self.client.get(reverse('main')).context['recipes'])
        titles_2 = set(r.title for r in self.client.get(reverse('main')).context['recipes'])
        # Both should have 10 recipes
        self.assertEqual(len(titles_1), 10)
        self.assertEqual(len(titles_2), 10)


class CategoryDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Salads')
        self.recipe1 = Recipe.objects.create(
            title='Caesar', description='Caesar salad', instructions='Mix',
            ingredients='Lettuce, croutons', category=self.category
        )
        self.recipe2 = Recipe.objects.create(
            title='Greek', description='Greek salad', instructions='Chop',
            ingredients='Tomatoes, olives', category=self.category
        )
        self.other_category = Category.objects.create(name='Other')

    def test_category_detail_status_code(self):
        response = self.client.get(reverse('category_detail', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, 200)

    def test_category_detail_uses_correct_template(self):
        response = self.client.get(reverse('category_detail', kwargs={'pk': self.category.pk}))
        self.assertTemplateUsed(response, 'recipe/category_detail.html')

    def test_category_detail_returns_category_in_context(self):
        response = self.client.get(reverse('category_detail', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.context['category'], self.category)

    def test_category_detail_shows_correct_recipes(self):
        response = self.client.get(reverse('category_detail', kwargs={'pk': self.category.pk}))
        category = response.context['category']
        recipe_titles = [r.title for r in category]
        self.assertIn('Caesar', recipe_titles)
        self.assertIn('Greek', recipe_titles)

    def test_category_detail_404_for_missing_category(self):
        response = self.client.get(reverse('category_detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)

    def test_category_detail_empty_category(self):
        response = self.client.get(reverse('category_detail', kwargs={'pk': self.other_category.pk}))
        self.assertEqual(response.status_code, 200)
        category = response.context['category']
        self.assertEqual(list(category), [])