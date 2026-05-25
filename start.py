import json

class Client:
    def __init__(self, name, phone, budget):
        self.name = name
        self.phone = phone
        self.budget = budget
    def info(self):
        return f"{self.name} | {self.phone} | {self.budget} грн"

try:
    with open("clients.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    clients = [Client(d["name"], d["phone"], d["budget"]) for d in data]
except FileNotFoundError:
    clients = []

while True:
    print ("=== Менеджер Клиентов ===")
    print("1. Добавить клиента")
    print("2. Показать всех клиентов")
    print("3. Найти клиента по имени")
    print("4. Удалить клиента")
    print("5. Выйти")
    choice = input("Выберите действие: ")
    if choice == "1":
        client_name = input("Имя клиента: ")
        client_phone = input("Телефон клиента: ")
        if not client_phone.isdigit():
            print("Телефон должен содержать только цифры")
            continue
        client_budget = input("Бюджет клиента (грн): ")
        while not client_budget.isdigit():
            if not client_budget.isdigit():
                print("Бюджет должен быть числом")
            client_budget = input("Бюджет клиента (грн): ")
        client_budget = int(client_budget)
        new_client = Client(client_name, client_phone, client_budget)
        clients.append(new_client)
        print(f"Клиент {client_name} добавлен!")
    elif choice == "2":
        print("=== Список клиентов ===")
        if len(clients) == 0:
            print("Список клиентов пуст")
        else:
            for c in clients:
                print(c.info())
    elif choice == "3":
        search_name = input("Введите имя клиента для поиска: ")
        found = None
        for c in clients:
            if c.name == search_name:
                found = c
                break
        if found:
            print(found.info())
        else:
            print("Клиент не найден")
    elif choice == "4":
        search_name = input("Имя клиента для удаления: ")
        found = None
        for c in clients:
            if c.name == search_name:
                found = c
                break    
        if found:
            clients.remove(found)
            print(f"Клиент {search_name} удалён")
        else:
            print("Клиент не найден")
    elif choice == "5":
        data =[]
        for c in clients:
            data.append({"name": c.name, "phone": c.phone, "budget": c.budget})
        with open("clients.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Выход из программы")
        break