from django.contrib import admin

from .models import Favorite, Follow, Ingredient, Recipe, ShoppingList, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_filter = ['author', 'name', 'tags']
    list_display = ['name', 'followers']

    @admin.display(empty_value=None)
    def followers(self, obj):
        return obj.favorite_recipe.all().count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_filter = ['name']


admin.site.register(Follow)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(ShoppingList)
