from unittest import TestCase

from attr import attrs, attrib

from tests.test_classes import AttrsClass
from yasoo import deserialize


class TestAttrsDeserialization(TestCase):
    def test_attr_deserialization(self):
        @attrs
        class Foo:
            a = attrib()

        f = deserialize({'a': 5}, Foo)
        self.assertEqual(type(f), Foo)
        self.assertEqual(f.a, 5)

    def test_attr_missing_fields(self):
        @attrs
        class Foo:
            a = attrib()
            bar = attrib(default=None)

        try:
            deserialize({'a': 5}, Foo)
        except:
            self.fail('Failed to deserialize with non-mandatory field missing')

        try:
            deserialize({'bar': 5}, Foo)
            self.fail('Deserialized even though mandatory field is missing')
        except:
            pass

    def test_attr_extraneous_fields(self):
        @attrs
        class Foo:
            pass

        try:
            deserialize({'a': 5}, Foo)
            self.fail('Deserialized with extraneous fields')
        except:
            pass

    def test_attr_deserialization_with_type_in_data(self):
        @attrs
        class Foo:
            a = attrib()

        @attrs
        class Bar:
            foo = attrib()

        b = deserialize({'__type': 'Bar', 'foo': {'a': 5, '__type': 'Foo'}}, type_key='__type', globals=locals())
        self.assertEqual(type(b), Bar)
        self.assertEqual(type(b.foo), Foo)
        self.assertEqual(b.foo.a, 5)

    def test_attr_deserialization_with_fully_qualified_type_in_data(self):
        @attrs
        class Bar:
            foo = attrib()

        fully_qualified_name = '.'.join([AttrsClass.__module__, AttrsClass.__name__])
        b = deserialize({'__type': 'Bar', 'foo': {'__type': fully_qualified_name}},
                        obj_type=Bar,
                        type_key='__type',
                        globals=locals())
        self.assertEqual(type(b), Bar)
        self.assertEqual(type(b.foo), AttrsClass)

    def test_attr_deserialization_with_type_hint(self):
        @attrs
        class Foo:
            a = attrib()

        @attrs
        class Bar:
            foo: Foo = attrib()

        b = deserialize({'foo': {'a': 5}}, Bar, globals=locals())
        self.assertEqual(type(b), Bar)
        self.assertEqual(type(b.foo), Foo)
        self.assertEqual(b.foo.a, 5)

    def test_attr_deserialization_with_type_hint_and_type_in_data(self):
        @attrs
        class Foo:
            a = attrib()

        @attrs
        class FakeFoo:
            a = attrib()

        @attrs
        class Bar:
            foo: FakeFoo = attrib()

        b = deserialize({'__type': 'Bar', 'foo': {'a': 5, '__type': 'Foo'}}, type_key='__type', globals=locals())
        self.assertEqual(type(b), Bar)
        self.assertEqual(type(b.foo), Foo)
        self.assertEqual(b.foo.a, 5)
