import re
import django.apps
import graphene
from django.db.models import CharField, BigAutoField, IntegerField, TextField, ForeignKey, \
    BinaryField, DateField, BooleanField, DecimalField, DurationField, FloatField, \
    GenericIPAddressField, JSONField, SlugField, FileField, TimeField, UUIDField, OneToOneField, \
    ManyToManyField
from graphene import ObjectType, Field
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

def _make_resolver_one(model):
    def resolver(root, info, id):
        # return model.objects.order_by('-pub_date').first()
        return model.objects.get(pk=id)
    return resolver

def _make_resolver_filter(model):
    def resolver(root, info, **kwargs):
        q = model.objects.all()

        m2ms = getattr(model._meta, 'many_to_many', None)
        # TODO: Allow for multiple many-to-many relations
        if len(m2ms) != 0:
            for m2m in m2ms:
                value = kwargs.get(m2m.name, None)
                if value is not None:
                    kwargs_ = {m2m.name + '__in': [int(id_) for id_ in value]}
                    q = model.objects.filter(**kwargs_)
                    del kwargs[m2m.name]

        return q.filter(**kwargs)
    return resolver

class FlyingGraphQLView(GraphQLView):
    def __init__(self, *args, **kwargs):
        models = django.apps.apps.get_models()
        query_attrs = {}
        for model in models:
            fields = model._meta.fields + model._meta.many_to_many
            meta_class = type('Meta', (), {
                'model': model,
                'fields': [field.name for field in fields]
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

            query_attrs['one_' + _c2s(model_class_name)] = Field(type_class, id=graphene.ID(required=True))
            key = 'resolve_one_' + _c2s(model_class_name)
            query_attrs.update({key: _make_resolver_one(model)})

            kwargs_ = {}
            for field in fields:
                # for Django >= 5.0
                # if isinstance(field, GeneratedField):
                #     field_ = field.output_field
                # else:
                #     field_ = field
                field_ = field

                if isinstance(field_, BigAutoField) and field_.primary_key == True:
                    kwargs_[field.name] = graphene.ID()
                elif isinstance(
                        field_,
                        (ForeignKey, OneToOneField, )):
                    kwargs_[field.name] = graphene.ID()
                elif isinstance(
                        field_,
                        (
                            IntegerField,
                        )):
                    kwargs_[field.name] = graphene.Int()
                elif isinstance(
                        field_,
                        (
                            CharField,
                            BinaryField,
                            TextField,
                            DateField,
                            DecimalField,
                            DurationField,
                            FileField,
                            GenericIPAddressField,
                            JSONField,
                            SlugField,
                            TimeField,
                            UUIDField,
                        )):
                    kwargs_[field.name] = graphene.String()
                elif isinstance(field_, BooleanField):
                    kwargs_[field.name] = graphene.Boolean()
                elif isinstance(field_, FloatField):
                    kwargs_[field.name] = graphene.Float()
                elif isinstance(field_, FloatField):
                    kwargs_[field.name] = graphene.Float()

                # TODO: ManyToManyField DONE
                elif isinstance(field_, ManyToManyField):
                    # kwargs_[field.name] = graphene.String()
                    # TODO: change this to graphene.Int?
                    kwargs_[field.name] = graphene.List(graphene.ID)


            query_attrs['filter_' + _c2s(model_class_name)] = graphene.List(type_class, **kwargs_)
            key = 'resolve_filter_' + _c2s(model_class_name)
            query_attrs.update({key: _make_resolver_filter(model)})

        query_class = type(
            'Query',
            (ObjectType, ),
            query_attrs,
        )
        schema = graphene.Schema(query=query_class)

        super().__init__(*args, **{**kwargs, 'schema': schema})
