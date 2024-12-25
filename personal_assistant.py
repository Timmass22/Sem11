import sys

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
            manage_notes()
        elif choice == "2":
            manage_tasks()
        elif choice == "3":
            manage_contacts()
        elif choice == "4":
            manage_finances()
        elif choice == "5":
            calculator()
        elif choice == "6":
            print("Спасибо за использование Персонального помощника. До свидания!")
            sys.exit()
        else:
            print("Некорректный ввод. Пожалуйста, выберите действие от 1 до 6.")

def manage_notes():
    print("\nУправление заметками:")
    print()

def manage_tasks():
    print("\nУправление задачами:")
    print()

def manage_contacts():
    print("\nУправление контактами:")
    print()

def manage_finances():
    print("\nУправление финансовыми записями:")
    print()

def calculator():
    print("\nКалькулятор:")
    print()

if __name__ == "__main__":
    main_menu()
