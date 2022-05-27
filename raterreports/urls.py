from django.urls import path
from .views import GameList, CategoryGameList, ReviewGame

urlpatterns = [
    path('reports/games', GameList.as_view()),
    path('reports/games/themostreview', ReviewGame.as_view()),
    path('reports/categories', CategoryGameList.as_view()),
]