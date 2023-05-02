class CustomMeta(type):
    def __new__(mcs, name, bases, attrs):
        new_attrs = {}
        for attr_name, attr_value in attrs.items():
            if (
                not attr_name.startswith("__")
                and not attr_name.endswith("__")
            ):
                new_attrs[f"custom_{attr_name}"] = attr_value
            else:
                new_attrs[attr_name] = attr_value

        def custom_setattr(obj, name, value):
            if f"custom_{name}" in obj.__dict__:
                return
            if not name.startswith("__") and not name.endswith("__"):
                name = f"custom_{name}"
            super(obj.__class__, obj).__setattr__(name, value)

        new_attrs["__setattr__"] = custom_setattr

        return super().__new__(mcs, name, bases, new_attrs)


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"
