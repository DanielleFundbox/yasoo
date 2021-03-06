from collections import Mapping

from attr import attrs, attrib


@attrs
class AttrsClass:
    pass


@attrs
class FooContainer:
    foo = attrib()


class MyMapping(Mapping):
    def __init__(self, m) -> None:
        super().__init__()
        self._data = dict(m)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def __eq__(self, o: object) -> bool:
        return isinstance(o, MyMapping) and o._data == self._data

    def __iter__(self):
        return self._data.__iter__()

    def __len__(self):
        return len(self._data)

    def __getitem__(self, k):
        return self._data[k]
