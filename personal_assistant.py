import json
import csv
from datetime import datetime
import sys

class Note:
    NOTES_FILE = "notes.json"

    def __init__(self, id=None, title=None, content=None, timestamp=None):
        self.id = id
        self.title = title
        self.content = content
        self.timestamp = timestamp or datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "timestamp": self.timestamp,
        }

    @staticmethod
    def from_dict(data):
        return Note(
            id=data["id"],
            title=data["title"],
            content=data["content"],
            timestamp=data["timestamp"]
        )

    @classmethod
    def load_notes(cls):
        try:
            with open(cls.NOTES_FILE, "r") as file:
                return [cls.from_dict(note) for note in json.load(file)]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @classmethod
    def save_notes(cls, notes):
        with open(cls.NOTES_FILE, "w") as file:
            json.dump([note.to_dict() for note in notes], file, indent=4)

    @classmethod
    def create(cls):
        notes = cls.load_notes()
        note_id = max((note.id for note in notes), default=0) + 1
        title = input("Введите заголовок заметки: ").strip()
        content = input("Введите содержимое заметки: ").strip()
        note = cls(id=note_id, title=title, content=content)
        notes.append(note)
        cls.save_notes(notes)
        print("Заметка успешно создана!\n")

    @classmethod
    def view_all(cls):
        notes = cls.load_notes()
        if not notes:
            print("Нет доступных заметок.\n")
            return

        for note in notes:
            print(f"ID: {note.id}, Заголовок: {note.title}, Дата: {note.timestamp}")
        print()

    @classmethod
    def view_detail(cls):
        notes = cls.load_notes()
        note_id = int(input("Введите ID заметки для просмотра: ").strip())
        note = next((note for note in notes if note.id == note_id), None)
        if note:
            print(f"\nЗаголовок: {note.title}\nСодержимое: {note.content}\nДата: {note.timestamp}\n")
        else:
            print("Заметка не найдена.\n")

    @classmethod
    def edit(cls):
        notes = cls.load_notes()
        note_id = int(input("Введите ID заметки для редактирования: ").strip())
        note = next((note for note in notes if note.id == note_id), None)
        if note:
            note.title = input(f"Введите новый заголовок (текущий: {note.title}): ").strip() or note.title
            note.content = input(f"Введите новое содержимое (текущее: {note.content}): ").strip() or note.content
            note.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            cls.save_notes(notes)
            print("Заметка успешно обновлена!\n")
        else:
            print("Заметка не найдена.\n")

    @classmethod
    def delete(cls):
        notes = cls.load_notes()
        note_id = int(input("Введите ID заметки для удаления: ").strip())
        notes = [note for note in notes if note.id != note_id]
        cls.save_notes(notes)
        print("Заметка успешно удалена!\n")

    @classmethod
    def import_csv(cls):
        file_name = input("Введите имя CSV-файла для импорта: ").strip()
        try:
            with open(file_name, "r", newline="") as file:
                reader = csv.DictReader(file)
                notes = cls.load_notes()
                for row in reader:
                    notes.append(cls.from_dict(row))
                cls.save_notes(notes)
                print("Заметки успешно импортированы!\n")
        except FileNotFoundError:
            print("Файл не найден.\n")

    @classmethod
    def export_csv(cls):
        file_name = input("Введите имя CSV-файла для экспорта: ").strip()
        notes = cls.load_notes()
        with open(file_name, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "title", "content", "timestamp"])
            writer.writeheader()
            for note in notes:
                writer.writerow(note.to_dict())
        print("Заметки успешно экспортированы!\n")

    @classmethod
    def manage(cls):
        while True:
            print("\nУправление заметками:")
            print("1. Создать новую заметку")
            print("2. Просмотреть список заметок")
            print("3. Просмотреть подробности заметки")
            print("4. Редактировать заметку")
            print("5. Удалить заметку")
            print("6. Импорт заметок из CSV")
            print("7. Экспорт заметок в CSV")
            print("8. Назад")

            choice = input("Выберите действие: ").strip()

            if choice == "1":
                cls.create()
            elif choice == "2":
                cls.view_all()
            elif choice == "3":
                cls.view_detail()
            elif choice == "4":
                cls.edit()
            elif choice == "5":
                cls.delete()
            elif choice == "6":
                cls.import_csv()
            elif choice == "7":
                cls.export_csv()
            elif choice == "8":
                break
            else:
                print("Некорректный ввод. Пожалуйста, выберите действие от 1 до 8.")

class TasksManager:
    TASKS_FILE = "tasks.json"

    def __init__(self, id=None, title=None, description=None, done=False, priority="Средний", due_date=None):
        self.id = id
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "priority": self.priority,
            "due_date": self.due_date,
        }

    @staticmethod
    def from_dict(data):
        return TasksManager(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            done=data["done"],
            priority=data["priority"],
            due_date=data["due_date"]
        )

    @classmethod
    def load_tasks(cls):
        try:
            with open(cls.TASKS_FILE, "r") as file:
                return [cls.from_dict(task) for task in json.load(file)]
        except (FileNotFoundError):
            return []

    @classmethod
    def save_tasks(cls, tasks):
        with open(cls.TASKS_FILE, "w") as file:
            json.dump([task.to_dict() for task in tasks], file, indent=4)

    @classmethod
    def create(cls):
        tasks = cls.load_tasks()
        task_id = max((task.id for task in tasks), default=0) + 1
        title = input("Введите заголовок задачи: ").strip()
        description = input("Введите описание задачи: ").strip()
        priority = input("Введите приоритет задачи (Высокий/Средний/Низкий): ").strip()
        due_date = input("Введите срок выполнения (ДД-ММ-ГГГГ): ").strip()
        task = cls(id=task_id, title=title, description=description, priority=priority, due_date=due_date)
        tasks.append(task)
        cls.save_tasks(tasks)
        print("Задача успешно создана!")

    @classmethod
    def view_all(cls):
        tasks = cls.load_tasks()
        if not tasks:
            print("Нет доступных задач.")
            return

        for task in tasks:
            status = "Выполнено" if task.done else "Не выполнено"
            print(f"ID: {task.id}, Заголовок: {task.title}, Статус: {status}, Приоритет: {task.priority}, Срок: {task.due_date}")
        print()

    @classmethod
    def mark_done(cls):
        tasks = cls.load_tasks()
        task_id = int(input("Введите ID задачи для отметки как выполненной: ").strip())
        task = next((task for task in tasks if task.id == task_id), None)
        if task:
            task.done = True
            cls.save_tasks(tasks)
            print("Задача отмечена выполненной!")
        else:
            print("Задача не найдена.")

    @classmethod
    def edit(cls):
        tasks = cls.load_tasks()
        task_id = int(input("Введите ID задачи для редактирования: ").strip())
        task = next((task for task in tasks if task.id == task_id), None)
        if task:
            task.title = input(f"Введите новый заголовок (текущий: {task.title}): ").strip() or task.title
            task.description = input(f"Введите новое описание (текущее: {task.description}): ").strip() or task.description
            task.priority = input(f"Введите новый приоритет (текущий: {task.priority}): ").strip() or task.priority
            task.due_date = input(f"Введите новый срок выполнения (текущий: {task.due_date}): ").strip() or task.due_date
            cls.save_tasks(tasks)
            print("Задача успешно обновлена!")
        else:
            print("Задача не найдена.")

    @classmethod
    def delete(cls):
        tasks = cls.load_tasks()
        task_id = int(input("Введите ID задачи для удаления: ").strip())
        tasks = [task for task in tasks if task.id != task_id]
        cls.save_tasks(tasks)
        print("Задача успешно удалена!")

    @classmethod
    def import_csv(cls):
        file_name = input("Введите имя CSV-файла для импорта: ").strip()
        try:
            with open(file_name, "r", newline="") as file:
                reader = csv.DictReader(file)
                tasks = cls.load_tasks()
                for row in reader:
                    tasks.append(cls.from_dict(row))
                cls.save_tasks(tasks)
                print("Задачи успешно импортированы!")
        except FileNotFoundError:
            print("Файл не найден.")

    @classmethod
    def export_csv(cls):
        file_name = input("Введите имя CSV-файла для экспорта: ").strip()
        tasks = cls.load_tasks()
        with open(file_name, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "title", "description", "done", "priority", "due_date"])
            writer.writeheader()
            for task in tasks:
                writer.writerow(task.to_dict())
        print("Задачи успешно экспортированы!")

    @classmethod
    def manage(cls):
        while True:
            print("Управление задачами:")
            print("1. Создать новую задачу")
            print("2. Просмотреть список задач")
            print("3. Отметить задачу как выполненную")
            print("4. Редактировать задачу")
            print("5. Удалить задачу")
            print("6. Импорт задач из CSV")
            print("7. Экспорт задач в CSV")
            print("8. Назад")

            choice = input("Выберите действие: ").strip()

            if choice == "1":
                cls.create()
            elif choice == "2":
                cls.view_all()
            elif choice == "3":
                cls.mark_done()
            elif choice == "4":
                cls.edit()
            elif choice == "5":
                cls.delete()
            elif choice == "6":
                cls.import_csv()
            elif choice == "7":
                cls.export_csv()
            elif choice == "8":
                break
            else:
                print("Некорректный ввод. Пожалуйста, выберите действие от 1 до 8.")
        print()

class ContactsManager:
    CONTACTS_FILE = "contacts.json"

    def __init__(self, id=None, name=None, phone=None, email=None):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
        }

    @staticmethod
    def from_dict(data):
        return ContactsManager(
            id=data["id"],
            name=data["name"],
            phone=data["phone"],
            email=data["email"]
        )

    @classmethod
    def load_contacts(cls):
        try:
            with open(cls.CONTACTS_FILE, "r") as file:
                return [cls.from_dict(contact) for contact in json.load(file)]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @classmethod
    def save_contacts(cls, contacts):
        with open(cls.CONTACTS_FILE, "w") as file:
            json.dump([contact.to_dict() for contact in contacts], file, indent=4)

    @classmethod
    def create(cls):
        contacts = cls.load_contacts()
        contact_id = max((contact.id for contact in contacts), default=0) + 1
        name = input("Введите имя контакта: ").strip()
        phone = input("Введите номер телефона: ").strip()
        email = input("Введите адрес электронной почты: ").strip()
        contact = cls(id=contact_id, name=name, phone=phone, email=email)
        contacts.append(contact)
        cls.save_contacts(contacts)
        print("Контакт успешно создан!")

    @classmethod
    def view_all(cls):
        contacts = cls.load_contacts()
        if not contacts:
            print("Нет доступных контактов.")
            return

        for contact in contacts:
            print(f"ID: {contact.id}, Имя: {contact.name}, Телефон: {contact.phone}, Email: {contact.email}")
        print()

    @classmethod
    def search(cls):
        contacts = cls.load_contacts()
        search_term = input("Введите имя или номер телефона: ").strip().lower()
        results = [contact for contact in contacts if search_term in contact.name.lower() or search_term in contact.phone]

        if results:
            for contact in results:
                print(f"ID: {contact.id}, Имя: {contact.name}, Телефон: {contact.phone}, Email: {contact.email}")
        else:
            print("Контакты не найдены.")

    @classmethod
    def edit(cls):
        contacts = cls.load_contacts()
        contact_id = int(input("Введите ID контакта для редактирования: ").strip())
        contact = next((contact for contact in contacts if contact.id == contact_id), None)
        if contact:
            contact.name = input(f"Введите новое имя (текущее: {contact.name}): ").strip() or contact.name
            contact.phone = input(f"Введите новый номер телефона (текущий: {contact.phone}): ").strip() or contact.phone
            contact.email = input(f"Введите новый email (текущий: {contact.email}): ").strip() or contact.email
            cls.save_contacts(contacts)
            print("Контакт успешно обновлён!")
        else:
            print("Контакт не найден.")

    @classmethod
    def delete(cls):
        contacts = cls.load_contacts()
        contact_id = int(input("Введите ID контакта для удаления: ").strip())
        contacts = [contact for contact in contacts if contact.id != contact_id]
        cls.save_contacts(contacts)
        print("Контакт успешно удалён!")

    @classmethod
    def import_csv(cls):
        file_name = input("Введите имя CSV-файла для импорта: ").strip()
        try:
            with open(file_name, "r", newline="") as file:
                reader = csv.DictReader(file)
                contacts = cls.load_contacts()
                for row in reader:
                    contacts.append(cls.from_dict(row))
                cls.save_contacts(contacts)
                print("Контакты успешно импортированы!")
        except FileNotFoundError:
            print("Файл не найден.")

    @classmethod
    def export_csv(cls):
        file_name = input("Введите имя CSV-файла для экспорта: ").strip()
        contacts = cls.load_contacts()
        with open(file_name, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "name", "phone", "email"])
            writer.writeheader()
            for contact in contacts:
                writer.writerow(contact.to_dict())
        print("Контакты успешно экспортированы!")

    @classmethod
    def manage(cls):
        while True:
            print("Управление контактами:")
            print("1. Создать новый контакт")
            print("2. Просмотреть список контактов")
            print("3. Поиск контакта")
            print("4. Редактировать контакт")
            print("5. Удалить контакт")
            print("6. Импорт контактов из CSV")
            print("7. Экспорт контактов в CSV")
            print("8. Назад")

            choice = input("Выберите действие: ").strip()

            if choice == "1":
                cls.create()
            elif choice == "2":
                cls.view_all()
            elif choice == "3":
                cls.search()
            elif choice == "4":
                cls.edit()
            elif choice == "5":
                cls.delete()
            elif choice == "6":
                cls.import_csv()
            elif choice == "7":
                cls.export_csv()
            elif choice == "8":
                break
            else:
                print("Некорректный ввод. Пожалуйста, выберите действие от 1 до 8.")
        print()

class FinancesManager:
    FINANCES_FILE = "finance.json"

    def __init__(self, id=None, amount=None, category=None, date=None, description=None):
        self.id = id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description,
        }

    @staticmethod
    def from_dict(data):
        return FinancesManager(
            id=data["id"],
            amount=data["amount"],
            category=data["category"],
            date=data["date"],
            description=data["description"]
        )

    @classmethod
    def load_finances(cls):
        try:
            with open(cls.FINANCES_FILE, "r") as file:
                return [cls.from_dict(record) for record in json.load(file)]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @classmethod
    def save_finances(cls, finances):
        with open(cls.FINANCES_FILE, "w") as file:
            json.dump([record.to_dict() for record in finances], file, indent=4)

    @classmethod
    def create(cls):
        finances = cls.load_finances()
        finance_id = max((record.id for record in finances), default=0) + 1
        amount = float(input("Введите сумму операции (положительная для дохода, отрицательная для расхода): ").strip())
        category = input("Введите категорию операции: ").strip()
        date = input("Введите дату операции (ДД-ММ-ГГГГ): ").strip()
        description = input("Введите описание операции: ").strip()
        record = cls(id=finance_id, amount=amount, category=category, date=date, description=description)
        finances.append(record)
        cls.save_finances(finances)
        print("Финансовая запись успешно создана!")

    @classmethod
    def view_all(cls):
        finances = cls.load_finances()
        if not finances:
            print("Нет доступных финансовых записей.")
            return

        for record in finances:
            print(f"ID: {record.id}, Сумма: {record.amount}, Категория: {record.category}, Дата: {record.date}, Описание: {record.description}")
        print()

    @classmethod
    def filter_by_category(cls):
        finances = cls.load_finances()
        category = input("Введите категорию для фильтрации: ").strip().lower()
        filtered = [record for record in finances if record.category.lower() == category]
        if filtered:
            for record in filtered:
                print(f"ID: {record.id}, Сумма: {record.amount}, Категория: {record.category}, Дата: {record.date}, Описание: {record.description}")
        else:
            print("Записи с указанной категорией не найдены.")

    @classmethod
    def generate_report(cls):
        finances = cls.load_finances()
        start_date = input("Введите начальную дату (ДД-ММ-ГГГГ): ").strip()
        end_date = input("Введите конечную дату (ДД-ММ-ГГГГ): ").strip()
        filtered = [record for record in finances if start_date <= record.date <= end_date]

        total_income = sum(record.amount for record in filtered if record.amount > 0)
        total_expense = sum(record.amount for record in filtered if record.amount < 0)
        balance = total_income + total_expense

        print(f"Отчёт с {start_date} по {end_date}:")
        print(f"Общий доход: {total_income}")
        print(f"Общие расходы: {total_expense}")
        print(f"Баланс: {balance}")

    @classmethod
    def import_csv(cls):
        file_name = input("Введите имя CSV-файла для импорта: ").strip()
        try:
            with open(file_name, "r", newline="") as file:
                reader = csv.DictReader(file)
                finances = cls.load_finances()
                for row in reader:
                    finances.append(cls.from_dict(row))
                cls.save_finances(finances)
                print("Финансовые записи успешно импортированы!")
        except FileNotFoundError:
            print("Файл не найден.")

    @classmethod
    def export_csv(cls):
        file_name = input("Введите имя CSV-файла для экспорта: ").strip()
        finances = cls.load_finances()
        with open(file_name, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "amount", "category", "date", "description"])
            writer.writeheader()
            for record in finances:
                writer.writerow(record.to_dict())
        print("Финансовые записи успешно экспортированы!")

    @classmethod
    def manage(cls):
        while True:
            print("Управление финансовыми записями:")
            print("1. Создать новую запись")
            print("2. Просмотреть все записи")
            print("3. Фильтрация записей по категории")
            print("4. Генерация отчёта за период")
            print("5. Импорт финансовых записей из CSV")
            print("6. Экспорт финансовых записей в CSV")
            print("7. Назад")

            choice = input("Выберите действие: ").strip()

            if choice == "1":
                cls.create()
            elif choice == "2":
                cls.view_all()
            elif choice == "3":
                cls.filter_by_category()
            elif choice == "4":
                cls.generate_report()
            elif choice == "5":
                cls.import_csv()
            elif choice == "6":
                cls.export_csv()
            elif choice == "7":
                break
            else:
                print("Некорректный ввод. Пожалуйста, выберите действие от 1 до 7.")
        print()

class Calculator:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ZeroDivisionError("Деление на ноль недопустимо.")
        return a / b

    @staticmethod
    def manage_calculator():
        while True:
            print("Калькулятор:")
            print("1. Сложение")
            print("2. Вычитание")
            print("3. Умножение")
            print("4. Деление")
            print("5. Назад")

            choice = input("Выберите действие: ").strip()

            if choice in ["1", "2", "3", "4"]:
                try:
                    a = float(input("Введите первое число: ").strip())
                    b = float(input("Введите второе число: ").strip())

                    if choice == "1":
                        print(f"Результат: {Calculator.add(a, b)}")
                    elif choice == "2":
                        print(f"Результат: {Calculator.subtract(a, b)}")
                    elif choice == "3":
                        print(f"Результат: {Calculator.multiply(a, b)}")
                    elif choice == "4":
                        try:
                            print(f"Результат: {Calculator.divide(a, b)}")
                        except ZeroDivisionError as e:
                            print(f"Ошибка: {e}")

                except ValueError:
                    print("Ошибка: ввод должен быть числом.")

            elif choice == "5":
                break
            else:
                print("Некорректный ввод. Пожалуйста, выберите действие от 1 до 5.")
        print()

def main_menu():
    while True:
        print("Добро пожаловать в Персональный помощник!")
        print("Выберите действие:")
        print("1. Управление заметками")
        print("2. Управление задачами")
        print("3. Управление контактами")
        print("4. Управление финансовыми записями")
        print("5. Калькулятор")
        print("6. Выход")

        choice = input("Введите номер действия: ").strip()

        if choice == "1":
            Note.manage()
        elif choice == "2":
            TasksManager.manage()
        elif choice == "3":
            ContactsManager().manage()
        elif choice == "4":
            FinancesManager().manage()
        elif choice == "5":
            Calculator().manage_calculator()
        elif choice == "6":
            print("Спасибо за использование Персонального помощника!")
            sys.exit()
        else:
            print("Некорректный ввод. Пожалуйста, выберите действие от 1 до 6.")
if __name__ == "__main__":
    main_menu()