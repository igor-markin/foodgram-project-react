import django_filters.rest_framework
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import RecipeFilter
from .models import *
from .paginators import PageNumberPaginatorModified
from .permissions import AdminOrAuthorOrReadOnly
from .serializers import *
from .utils import get_shopping_list

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = PageNumberPaginatorModified
    permission_classes = [AdminOrAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ListRecipeSerializer
        return CreateRecipeSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class FollowList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination()

    def list(self, request, *args, **kwargs):
        serializer = ShowFollowersSerializer(
            many=True, context={'current_user': request.user}
        )
        return Response(serializer.data)

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)


class FollowViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        """ Начал переделывать на сериалайзер и всё отвалилось :( """
        user = self.request.user
        author = get_object_or_404(User, id=user_id)
        if Follow.objects.filter(user=user, author=author).exists():
            return Response('Вы уже подписаны',
                            status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.create(user=user, author=author)
        serializer = UserSerializer(author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        user = self.request.user
        author = get_object_or_404(User, id=user_id)
        get_object_or_404(Follow, user=user, author=author).delete()
        return Response('Удалено', status=status.HTTP_204_NO_CONTENT)


class FavouriteViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, recipe_id):
        """
        Понял, что ты предложил, но задачи со звёздочкой пока не готов :(
        Хорошо, что останется доступ сюда, потому что в рабочем проекте хочу
        переделать часть реализации на то, что ты здесь подсказал.
        Мне совсем не понравился проект, он высосал всю энергию...
        """
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            return Response('Вы уже добавили рецепт в избранное',
                            status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.create(user=user, recipe=recipe)
        serializer = AddFavouriteRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        favorite_obj = get_object_or_404(Favorite, user=user, recipe=recipe)
        if not favorite_obj:
            return Response('Рецепт не был в избранном',
                            status=status.HTTP_400_BAD_REQUEST)
        favorite_obj.delete()
        return Response('Удалено', status=status.HTTP_204_NO_CONTENT)


class ShoppingListViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, recipe_id):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if ShoppingList.objects.filter(user=user, recipe=recipe).exists():
            return Response('Вы уже добавили рецепт в список покупок',
                            status=status.HTTP_400_BAD_REQUEST)
        ShoppingList.objects.create(user=user, recipe=recipe)
        serializer = AddFavouriteRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        shopping_list_obj = get_object_or_404(ShoppingList, user=user,
                                              recipe=recipe)
        if not shopping_list_obj:
            return Response('Рецепт не был в списке покупок',
                            status=status.HTTP_400_BAD_REQUEST)
        shopping_list_obj.delete()
        return Response('Удалено', status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCart(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return get_shopping_list(self.request.user)
