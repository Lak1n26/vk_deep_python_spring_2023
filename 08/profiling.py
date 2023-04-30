import weakref
import cProfile
import pstats
from memory_profiler import profile


class DefaultClass:
    def __init__(self, attr1, attr2):
        self.attr1 = attr1
        self.attr2 = attr2


class SlotsClass:
    __slots__ = ("attr1", "attr2")

    def __init__(self, attr1, attr2):
        self.attr1 = attr1
        self.attr2 = attr2


class WeakRefClass:
    def __init__(self, attr1, attr2):
        self._attr1_ref = weakref.ref(attr1)
        self._attr2_ref = weakref.ref(attr2)

    @property
    def attr1(self):
        return self._attr1_ref()

    @property
    def attr2(self):
        return self._attr2_ref()


def operations_with_default_class():
    pr = cProfile.Profile()
    pr.enable()

    objects = []
    a1 = MyInt(1111)
    a2 = MyInt(2222)
    for i in range(500_000):
        obj = DefaultClass(a1, a2)
        objects.append(obj)
    for i in range(500_000):
        objects[i].attr1.value += 1
        objects[i].attr2.value = objects[i].attr1.value

    pr.disable()
    ps = pstats.Stats(pr).sort_stats("cumulative")
    print("ДЛЯ СТАНДАРТНОГО КЛАССА:")
    ps.print_stats()


def operations_with_slots_class():
    pr = cProfile.Profile()
    pr.enable()

    slots_examples = []
    a1 = MyInt(1111)
    a2 = MyInt(2222)
    for i in range(500_000):
        slot = SlotsClass(a1, a2)
        slots_examples.append(slot)
    for i in range(500_000):
        slots_examples[i].attr1.value += 1
        slots_examples[i].attr2.value = slots_examples[i].attr1.value

    pr.disable()
    ps = pstats.Stats(pr).sort_stats("cumulative")
    print("ДЛЯ КЛАССА СО СЛОТАМИ:")
    ps.print_stats()


class MyInt:
    def __init__(self, value):
        self.value = value


def operations_with_weakref_class():
    pr = cProfile.Profile()
    pr.enable()

    weakrefs = []
    a1 = MyInt(1111)
    a2 = MyInt(2222)
    for i in range(500_000):
        obj = WeakRefClass(a1, a2)
        weakrefs.append(obj)
    for i in range(500_000):
        weakrefs[i].attr1.value += 1
        weakrefs[i].attr2.value = weakrefs[i].attr1.value

    pr.disable()
    ps = pstats.Stats(pr).sort_stats("cumulative")
    print("ДЛЯ КЛАССА СО СЛАБЫМИ ССЫЛКАМИ:")
    ps.print_stats()


@profile
def memory_profiling_default_class():
    print("ДЛЯ СТАНДАРТНОГО КЛАССА:")
    objects = []
    a1 = MyInt(1111)
    a2 = MyInt(2222)
    for i in range(500_000):
        obj = DefaultClass(a1, a2)
        objects.append(obj)
    for i in range(500_000):
        objects[i].attr1.value += 1
        objects[i].attr2.value = objects[i].attr1.value


@profile
def memory_profiling_slots_class():
    print("ДЛЯ КЛАССА СО СЛОТАМИ:")
    slots_examples = []
    a1 = MyInt(1111)
    a2 = MyInt(2222)
    for i in range(500_000):
        slot = SlotsClass(a1, a2)
        slots_examples.append(slot)
    for i in range(500_000):
        slots_examples[i].attr1.value += 1
        slots_examples[i].attr2.value = slots_examples[i].attr1.value


@profile
def memory_profiling_weakref_class():
    print("ДЛЯ КЛАССА СО СЛАБЫМИ ССЫЛКАМИ:")
    weakrefs = []
    a1 = MyInt(1111)
    a2 = MyInt(2222)
    for i in range(500_000):
        obj = WeakRefClass(a1, a2)
        weakrefs.append(obj)
    for i in range(500_000):
        weakrefs[i].attr1.value += 1
        weakrefs[i].attr2.value = weakrefs[i].attr1.value


if __name__ == "__main__":
    # task2
    memory_profiling_default_class()
    memory_profiling_slots_class()
    memory_profiling_weakref_class()

    # task1
    operations_with_default_class()
    operations_with_weakref_class()
    operations_with_slots_class()
