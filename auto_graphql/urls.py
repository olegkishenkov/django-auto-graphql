from django.urls import re_path
from .views import FlyingGraphQLView

urlpatterns = [
    re_path(r"graphql", FlyingGraphQLView.as_view(graphiql=True)),
]