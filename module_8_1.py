def add_everything_up(a, b):
    try:
        if isinstance(a, (int, float)) and isinstance(b, str):
            raise TypeError
        elif isinstance(a, str) and isinstance(b, (int, float)):
            raise TypeError

        return a + b

    except TypeError:
           return str(a) + str(b)


print(add_everything_up(123.456, 'строка'))  # 123.456строка
print(add_everything_up('яблоко', 4215))  # яблоко4215
print(add_everything_up(123.456, 7))  # 130.456