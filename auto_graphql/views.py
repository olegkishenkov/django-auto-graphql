import re
import django.apps
import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType
from graphene_django.views import GraphQLView


def _plural_from_single(s):
    return s.rstrip('y') + 'ies' if s.endswith('y') else s + 's'


def _c2s(name):
    # camel to snake
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def _make_resolver(model):
    def resolver(root, info):
        return model.objects.all()
    return resolver


class FlyingGraphQLView(GraphQLView):
    def __init__(self, *args, **kwargs):
        models = django.apps.apps.get_models()
        query_attrs = {}
        for model in models:
            print(model._meta.model_name)
            meta_class = type('Meta', (), {
                'model': model,
                'fields': [field.name for field in model._meta.fields]
            })
            model_name, model_class_name = model._meta.model_name, model.__name__
            type_class = type(
                model_class_name + 'Type',
                (DjangoObjectType, ),
                {'Meta': meta_class},
            )

            query_attrs['all_' + _plural_from_single(_c2s(model_class_name))] = graphene.List(type_class)
            key = 'resolve_all_' + _plural_from_single(_c2s(model_class_name))
            query_attrs.update({key: _make_resolver(model)})

        query_class = type(
            'Query',
            (ObjectType, ),
            query_attrs,
        )
        schema = graphene.Schema(query=query_class)

        super().__init__(*args, **{**kwargs, 'schema': schema})
