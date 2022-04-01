from django.urls import path
from strawberry.django.views import GraphQLView

from api_graphql.schema import schema

urlpatterns = [
    path("", GraphQLView.as_view(schema=schema)),
]