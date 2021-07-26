from django.http import HttpResponse

from api.models import IngredientInRecipe


def get_shopping_list(user):
    shopping_cart = user.purchases.all()
    buying_list = {}
    for record in shopping_cart:
        recipe = record.recipe
        ingredients = IngredientInRecipe.objects.filter(recipe=recipe)
        for ingredient in ingredients:
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            if name not in buying_list:
                buying_list[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount
                }
            else:
                buying_list[name]['amount'] = (
                        buying_list[name]['amount'] + amount)

    wishlist = []
    for item in buying_list:
        wishlist.append(f'{item} - {buying_list[item]["amount"]} '
                        f'{buying_list[item]["measurement_unit"]} \n')
    wishlist.append('\n')
    wishlist.append('Yandex Foodgram, 2021')
    response = HttpResponse(wishlist, 'Content-Type: text/plain')
    response['Content-Disposition'] = 'attachment; filename="shoplist.txt"'

    return response
