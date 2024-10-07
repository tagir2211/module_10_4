from queue import Queue
from random import randint
from threading import Thread
from time import sleep


class Table:
    def __init__(self, number, guest=None):
        self.number = number
        self.guest = guest


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        sleep(randint(3, 10))


class Cafe:
    def __init__(self, *tables):
        self.tables = []
        self.empty_tables = []
        self.que = Queue()
        for table in tables:
            self.tables.append(table)

    def empty_tab(self):
        self.empty_tables.clear()
        for table in self.tables:
            if table.guest is None:
                self.empty_tables.append(table)

    def guest_arrival(self, *guests):
        for guest in guests:
            self.empty_tab()
            if len(self.empty_tables) > 0:
                for table in self.empty_tables:
                    table.guest = guest
                    print(f'{guest.name} сел(-а) за стол номерe {table.number}')
                    guest.start()
                    break
            else:
                self.que.put(guest)
                print(f'{guest.name} в очереди')

    def discuss_guests(self):
        while not self.que.empty():
            for table in self.tables:
                if table.guest is not None and table.guest.is_alive():
                    table.guest.join()
                    print(f'{table.guest.name} окушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest = self.que.get()
                    table.guest.start()
                    print(f'{table.guest.name} вышл(-ла) из очереди и сел(-а) за стол номер {table.number}')
                    if self.que.qsize() > 0:
                        print(f'В очереди ожидают еще {self.que.qsize()} гостя')
                    else:
                        print('В очереди никого нет')

                    # Создание столов


tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
