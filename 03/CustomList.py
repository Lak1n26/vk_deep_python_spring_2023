class CustomList(list):
    def __add__(self, other):
        """
        Поочередно складываем элементы списков, а после вставляем все оставшиеся
        Случай когда CustomList - первое слагаемое
        """
        summ = CustomList(
            [self[i] + other[i] for i in range(min(len(self), len(other)))]
        )
        if len(other) > len(self):
            summ.extend([other[i] for i in range(len(self), len(other))])
        else:
            summ.extend([self[i] for i in range(len(other), len(self))])
        return summ

    def __radd__(self, other):
        """
        Поочередно складываем элементы списков, а после вставляем все оставшиеся
        Случай когда CustomList - второе слагаемое
        """
        summ = CustomList(
            [self[i] + other[i] for i in range(min(len(self), len(other)))]
        )
        if len(other) > len(self):
            summ.extend([other[i] for i in range(len(self), len(other))])
        else:
            summ.extend([self[i] for i in range(len(other), len(self))])
        return summ

    def __sub__(self, other):
        """
        Поочередно вычитаем элементы списков, а после вставляем все оставшиеся
        Случай когда CustomList - уменьшаемое
        """
        diff = CustomList(
            [self[i] - other[i] for i in range(min(len(self), len(other)))]
        )
        if len(other) > len(self):
            diff.extend([-other[i] for i in range(len(self), len(other))])
        else:
            diff.extend([self[i] for i in range(len(other), len(self))])
        return diff

    def __rsub__(self, other):
        """
        Поочередно вычитаем элементы списков, а после вставляем все оставшиеся
        Случай когда CustomList - вычитаемое
        """
        diff = CustomList(
            [other[i] - self[i] for i in range(min(len(self), len(other)))]
        )
        if len(other) > len(self):
            diff.extend([other[i] for i in range(len(self), len(other))])
        else:
            diff.extend([-self[i] for i in range(len(other), len(self))])
        return diff

    def __eq__(self, other):
        """сравнивает длины списков"""
        return len(self) == len(other)

    def __ne__(self, other):
        return len(self) != len(other)

    def __gt__(self, other):
        return len(self) > len(other)

    def __ge__(self, other):
        return len(self) >= len(other)

    def __lt__(self, other):
        return len(self) < len(other)

    def __le__(self, other):
        return len(self) <= len(other)

    def __str__(self):
        return f"{super().__str__()}, сумма = {sum(self)}"
