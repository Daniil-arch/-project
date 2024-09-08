import threading
import time

total_enemies = 100
enemies_lock = threading.Lock()

class Knight(threading.Thread):
    def __init__(self, name, power):
        super().__init__()
        self.name = name
        self.power = power
        self.days = 0

    def run(self):
        global total_enemies
        print(f"{self.name}, на нас напали!")

        while True:
            time.sleep(1)
            self.days += 1

            with enemies_lock:
                total_enemies -= self.power
                remaining_enemies = max(total_enemies, 0)

            print(f"{self.name}, сражается {self.days} день(дня)..., осталось {remaining_enemies} воинов.")

            if remaining_enemies <= 0:
                print(f"{self.name} одержал победу спустя {self.days} дней(дня)!")
                break


first_knight = Knight('Sir Lancelot', 10)
second_knight = Knight('Sir Galahad', 20)

first_knight.start()
second_knight.start()

first_knight.join()
second_knight.join()

print("Все битвы закончились!")