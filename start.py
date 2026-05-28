import json
import os

class Client:
    def __init__(self, name, phone, budget):
        self.name = name
        self.phone = phone
        self.budget = budget
    def info(self):
        return f"{self.name} | {self.phone} | {self.budget} грн"

def save_data(clients):
    data = [{"name": c.name, "phone": c.phone, "budget": c.budget} for c in clients]
    with open("clients.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def valid_phone(phone):
            if phone.startswith("+"):
                return phone[1:].isdigit()
            return phone.isdigit()

clients = []
if os.path.exists("clients.json"):
    with open("clients.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        clients = [Client(d["name"], d["phone"], d["budget"]) for d in data]

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
        new_client = Client(client_name, int(client_phone), int(client_budget))
        clients.append(new_client)
        save_data(clients)
        print(f"Клиент {client_name} добавлен!")
    
    elif choice == "2":
        print("=== Список клиентов ===")
        if len(clients) == 0:
            print("Список клиентов пуст")
        else:
            for c in clients:
                print(c.info())

    elif choice == "3":
        search_name = input("Введите имя клиента для поиска: ").lower().strip()
        results = [c for c in clients if search_name in c.name.lower()]
        if results:
            print("=== Результаты поиска ===")
            for c in results:
                print(c.info())
        else:
            print("Клиенты не найдены")
    elif choice == "4":
        names_input = input("Введите имена для удаления (через запятую): ")
        names_remove = [name.strip() for name in names_input.split(",")]
        clients_remove = [c for c in clients if c.name in names_remove]
        if clients_remove:
            for c in clients_remove:
                clients.remove(c)
            save_data(clients)
            removed_names = ", ".join([c.name for c in clients_remove])
            print(f"Удалены клиенты: {removed_names}")
        else:
            print("Клиенты с такими именами не найдены.")
    elif choice == "5":
        print("Выход из программы")
        save_data(clients)
        break
    else:
        print("Выберите корректный пункт меню")