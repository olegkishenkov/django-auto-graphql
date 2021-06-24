from django.conf.urls import url
from .views import FlyingGraphQLView

urlpatterns = [
    url(r"graphql", FlyingGraphQLView.as_view(graphiql=True)),
]