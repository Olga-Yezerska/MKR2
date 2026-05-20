from django.shortcuts import render, get_object_or_404
from .models import Recipe, Category


def main(request):
    recipes = Recipe.objects.order_by('?')[:10]
    return render(request, 'recipe/main.html', {'recipes': recipes})


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'recipe/category_detail.html', {'category': category})