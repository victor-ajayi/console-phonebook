import csv
import sys
from pathlib import Path

from helpers import (
    add_contact,
    delete_contact,
    edit_contact,
    find_contact,
    view_contacts,
)

# Заголовки файла CSV
fieldnames = ["surname", "name", "patronymic", "org_name", "work_tel", "mobile_tel"]


def main():
    print("Телефоный справочник")

    # Создает файл если не существует
    if not FILEPATH.exists():
        with open(FILEPATH, "w") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
    else:
        pass

    while True:
        print(
            """
Для работы со справочником выберите команду

1 — Посмотреть контакты
2 — Добавить контакт
3 — Редактировать контакт
4 — Удалить контакт
5 – Найти контакт
0 — Выйти
    """
        )

        command = input(">> ").strip()

        match command:
            case "1":
                view_contacts(FILEPATH)
            case "2":
                add_contact(FILEPATH)
            case "3":
                edit_contact(FILEPATH)
            case "4":
                delete_contact(FILEPATH)
            case "5":
                find_contact(FILEPATH)
            case "0":
                break
            case _:
                print("Ошибка: Вы ввели ошибочную команду! Выберите команду от 1 до 5")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Правило использования: python main.py <filename>")

    filename = sys.argv[1]

    # Путь к файлу
    FILEPATH = Path(__name__).parent.resolve() / filename

    main()
