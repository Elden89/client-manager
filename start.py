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
        return f"{self.name} | {self.phone} | {self.budget} UAH"

    def __repr__(self):
        return f"Client(name={self.name!r}, phone={self.phone!r}, budget={self.budget})"

Base.metadata.create_all(engine)

def valid_phone(phone):
    if phone.startswith("+"):
        return phone[1:].isdigit()
    return phone.isdigit()

while True:
    print("=== Client Manager ===")
    print("1. Add client")
    print("2. Show all clients")
    print("3. Find client by name")
    print("4. Delete client")
    print("5. Exit")
    choice = input("Select an option: ")
    
    if choice == "1":
        client_name = input("Client name: ").strip()
        while not client_name:
            print("Name cannot be empty")
            client_name = input("Client name: ").strip()

        client_phone = input("Client phone: ")
        while not valid_phone(client_phone):
            print("Phone must contain only digits (and + at the start)")
            client_phone = input("Client phone: ")

        client_budget = input("Client budget (UAH): ")
        while not client_budget.isdigit():
            print("Budget must be a number")
            client_budget = input("Client budget (UAH): ")
        client_budget = int(client_budget)

        with Session(engine) as session:
            new_client = Client(name=client_name, phone=client_phone, budget=int(client_budget))
            try:
                session.add(new_client)
                session.commit()
                print(f"Client {client_name} added!")
            except IntegrityError:
                session.rollback()
                print("Client with this phone number already exists")
    
    elif choice == "2":
        with Session(engine) as session:
            clients = session.query(Client).all()
        if not clients:
            print("Client list is empty")
        else:
            print("=== Client List ===")
            for c in clients:
                print(f"{c.id}. {c}")

    elif choice == "3":
        search_name = input("Enter client name to search: ").lower().strip()
        with Session(engine) as session:
            results = session.query(Client).filter(
                Client.name.ilike(f"%{search_name}%")
            ).all()
        if results:
            print("=== Search Results ===")
            for c in results:
                print(f"{c.id}. {c}")
        else:
            print("Clients not found")

    elif choice == "4":
        with Session(engine) as session:
            clients = session.query(Client).all()
            if not clients:
                print("Client list is empty")
                continue
            print("=== Client List ===")
            for c in clients:
                print(f"{c.id}. {c}")

            client_id = input("Enter client ID to delete: ")
            while not client_id.isdigit():
                print("ID must be a number")
                client_id = input("Enter client ID to delete: ")
            client_id = int(client_id)

            client = session.get(Client, client_id)
            if client:
                removed_name = client.name
                session.delete(client)
                session.commit()
                print(f"Client {removed_name} deleted")
            else:
                print("Client with this ID not found")
                
    elif choice == "5":
        print("Exiting program")
        break
    else:
        print("Please select a valid menu option")