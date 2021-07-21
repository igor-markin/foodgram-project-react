from django.contrib import admin

from .models import (Favorite, Follow, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    fields = ['user', 'recipe']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    fields = ['user', 'author']


@admin.register(Ingredient)
class Ingredient(admin.ModelAdmin):
    fields = ['name', 'measurement_unit']
    list_filter = ['name']


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    fields = ['ingredient', 'recipe', 'amount']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = ['name', 'author']
    list_filter = ['author', 'name', 'tags']


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    fields = ['user', 'recipe']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ['name', 'color', 'slug']
