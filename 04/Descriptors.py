# Stock market


class IncorrectType(Exception):
    pass


class Share_amount:
    # non negative integer
    def __set_name__(self, owner, name):
        self._instance_attr_name = f"_int_field_{name}"

    def __get__(self, obj, objtype):
        return getattr(obj, self._instance_attr_name)

    def __set__(self, obj, val):
        if not isinstance(val, int) or val < 0:
            raise IncorrectType(f"share_amount = {val} is not an integer!")
        return setattr(obj, self._instance_attr_name, val)

    def __delete__(self, obj):
        return delattr(obj, self._instance_attr_name)


class Company_name(Share_amount):
    # upper string
    def __set_name__(self, owner, name):
        self._instance_attr_name = f"_str_field_{name}"
        # print(f"IntField set_name {self._instance_attr_name}")

    def __set__(self, obj, val):
        if not isinstance(val, str):
            raise IncorrectType(f"company_name = {val} is not a upper string!")
        if not val.isupper() or not val.isalpha():
            raise IncorrectType(f"company_name = {val} is not a upper string!")
        return setattr(obj, self._instance_attr_name, val)


class Share_price(Share_amount):
    # positive number (int / float)
    def __set_name__(self, owner, name):
        self._instance_attr_name = f"_positive_number_field_{name}"

    def __set__(self, obj, val):
        if not isinstance(val, (float, int)) or val <= 0:
            raise IncorrectType(f"share_price = {val} is not a positive number!")
        return setattr(obj, self._instance_attr_name, float(val))


class Company:
    amount = Share_amount()
    name = Company_name()
    price = Share_price()

    def __init__(self, amount, name, price):
        self.amount = amount
        self.name = name
        self.price = price
