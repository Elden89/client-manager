import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Session
load_dotenv()

DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DB_URL)

class Base(DeclarativeBase):
    pass

class Client(Base):
    __tablename__ = "clients"
    id     = Column(Integer, primary_key=True)
    name   = Column(String(100), nullable=False)
    phone  = Column(String(20), nullable=False, unique=True)
    budget = Column(Integer, nullable=False)

    def __str__(self):
        return f"{self.name} | {self.phone} | {self.budget} грн"

    def __repr__(self):
        return f"Client(name={self.name!r}, phone={self.phone!r}, budget={self.budget})"

Base.metadata.create_all(engine)

def valid_phone(phone):
    if phone.startswith("+"):
        return phone[1:].isdigit()
    return phone.isdigit()

while True:
    print ("=== Менеджер Клиентов ===")
    print("1. Добавить клиента")
    print("2. Показать всех клиентов")
    print("3. Найти клиента по имени")
    print("4. Удалить клиента")
    print("5. Выйти")
    choice = input("Выберите действие: ")
    if choice == "1":
        client_name = input("Имя клиента: ").strip()
        while not client_name:
            print("Имя не может быть пустым")
            client_name = input("Имя клиента: ").strip()

        client_phone = input("Телефон клиента: ")
        while not valid_phone(client_phone):
            print("Телефон должен содержать только цифры(и + в начале)")
            client_phone = input("Телефон клиента: ")

        client_budget = input("Бюджет клиента (грн): ")
        while not client_budget.isdigit():
            print("Бюджет должен быть числом")
            client_budget = input("Бюджет клиента (грн): ")
        client_budget = int(client_budget)

        with Session(engine) as session:
            new_client = Client(name=client_name, phone=client_phone, budget=int(client_budget))
            try:
                session.add(new_client)
                session.commit()
                print(f"Клиент {client_name} добавлен!")
            except IntegrityError:
                session.rollback()
                print("Клиент с таким телефоном уже существует")
    
    
    elif choice == "2":
        with Session(engine) as session:
            clients = session.query(Client).all()
        if not clients:
            print("Список клиентов пуст")
        else:
            print("=== Список клиентов ===")
            for c in clients:
                print(f"{c.id}. {c}")

    elif choice == "3":
        search_name = input("Введите имя клиента для поиска: ").lower().strip()
        with Session(engine) as session:
            results = session.query(Client).filter(
                Client.name.ilike(f"%{search_name}%")
            ).all()
        if results:
            print("=== Результаты поиска ===")
            for c in results:
                print(f"{c.id}. {c}")
        else:
            print("Клиенты не найдены")

    elif choice == "4":
        client_id = input("Введите ID клиента для удаления: ")
        while not client_id.isdigit():
            print("ID должен быть числом")
            client_id = input("Введите ID клиента для удаления: ")
        client_id = int(client_id)

        with Session(engine) as session:
            client = session.get(Client, client_id)
            if client:
                removed_name = client.name
                session.delete(client)
                session.commit()
                print(f"Клиент {removed_name} удален")
            else:
                print("Клиент с таким ID не найден")
    elif choice == "5":
        print("Выход из программы")
        break
    else:
        print("Выберите корректный пункт меню")
