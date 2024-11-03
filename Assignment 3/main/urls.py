from django.urls import path

from main.views import KeyValueAddView, KeyValueView

urlpatterns = [
    path("", KeyValueAddView.as_view()),
    path("<str:key>/", KeyValueView.as_view()),
]

