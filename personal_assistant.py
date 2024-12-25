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
    def manage_tasks(self):
        print("\nУправление задачами:")
        print("(Функциональность будет добавлена позже)")
        print()

class ContactsManager:
    def manage_contacts(self):
        print("\nУправление контактами:")
        print("(Функциональность будет добавлена позже)")
        print()

class FinancesManager:
    def manage_finances(self):
        print("\nУправление финансовыми записями:")
        print("(Функциональность будет добавлена позже)")
        print()

class Calculator:
    def manage_calculator(self):
        print("\nКалькулятор:")
        print("(Функциональность будет добавлена позже)")
        print()

def main_menu():
    tasks_manager = TasksManager()
    contacts_manager = ContactsManager()
    finances_manager = FinancesManager()
    calculator = Calculator()

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
            tasks_manager.manage_tasks()
        elif choice == "3":
            contacts_manager.manage_contacts()
        elif choice == "4":
            finances_manager.manage_finances()
        elif choice == "5":
            calculator.manage_calculator()
        elif choice == "6":
            print("Спасибо за использование Персонального помощника. До свидания!")
            sys.exit()
        else:
            print("Некорректный ввод. Пожалуйста, выберите действие от 1 до 6.")

if __name__ == "__main__":
    main_menu()

