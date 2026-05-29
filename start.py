import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Session
load_dotenv()

DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DB_URL)

class Base(DeclarativeBase):
    pass

class Client(Base):
    __tablename__ = "clients"
    id     = Column(Integer, primary_key=True)
    name   = Column(String(100))
    phone  = Column(String(20))
    budget = Column(Integer)

    def info(self):
        return f"{self.name} | {self.phone} | {self.budget} грн"

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
            session.add(new_client)
            session.commit()
        print(f"Клиент {client_name} добавлен!")
    
    
    elif choice == "2":
        with Session(engine) as session:
            clients = session.query(Client).all()
        if not clients:
            print("Список клиентов пуст")
        else:
            print("=== Список клиентов ===")
            for c in clients:
                print(c.info())

    elif choice == "3":
        search_name = input("Введите имя клиента для поиска: ").lower().strip()
        with Session(engine) as session:
            results = session.query(Client).filter(
                Client.name.ilike(f"%{search_name}%")
            ).all()
        if results:
            print("=== Результаты поиска ===")
            for c in results:
                print(c.info())
        else:
            print("Клиенты не найдены")

    elif choice == "4":
        names_input = input("Введите имена для удаления (через запятую): ")
        names_remove = [name.strip() for name in names_input.split(",")]
         with Session(engine) as session:
            clients_remove = session.query(Client).filter(
                Client.name.in_(names_remove)
            ).all()
        if clients_remove:
            removed_names = ", ".join([c.name for c in clients_remove])
            for c in clients_remove:
                session.delete(c)
            session.commit()
            print(f"Удалены клиенты: {removed_names}")
        else:
            print("Клиенты с такими именами не найдены")
    elif choice == "5":
        print("Выход из программы")
        break
    else:
        print("Выберите корректный пункт меню")