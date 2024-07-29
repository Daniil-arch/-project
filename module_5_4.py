class House:
    houses_history = []

    def __new__(cls, *args):
        obj = super().__new__(cls)
        cls.houses_history.append(args[0])
        return obj

    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __del__(self):
        print(f"{self.name} снесён, но он останется в истории")

    def __str__(self):
        return f"Дом {self.name}, номер {self.number}"

    def __add__(self, other):
        return self.number + other.number

    def __eq__(self, other):
        return self.number == other.number

# Создание объектов класса House
h1 = House('ЖК Эльбрус', 10)
print(House.houses_history)
h2 = House('ЖК Акация', 20)
print(House.houses_history)
h3 = House('ЖК Матрёшки', 20)
print(House.houses_history)

# Удаление объектов
del h2
del h3

print(House.houses_history)

# Удаление последнего объекта
del h1