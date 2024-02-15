from csv import DictReader, DictWriter
from math import ceil

# Заголовки файла CSV
fieldnames = ["surname", "name", "patronymic", "org_name", "work_tel", "mobile_tel"]

# Количество контактов по странице
PAGINATION_NO = 10


def print_headers() -> None:
    """Печатает заголовки csv файла"""

    headers = ["ФИО", "Организация", "Раб. тел", "Моб. тел"]
    print(f"{headers[0]:^50} | {headers[1]:^20} | {headers[2]:^20} | {headers[3]:^20}")
    print("-" * 120)


def print_contacts(contacts: list[dict[str, str]], paginate=False) -> None:
    """Печатает все контакты из полученного списка контактов"""

    if paginate:
        print_headers()

    for contact in contacts:
        full_name = f"{contact['surname']} {contact['name']} {contact['patronymic']}"
        print(
            f"{full_name:^50} | {contact['org_name']:^20} | {contact['work_tel']:^20} | {contact['mobile_tel']:^20}"
        )


def get_contact_details() -> dict[str, str]:
    """Получает контактную информацию от пользователя и возвращает контакт в виде словаря"""

    while True:
        surname = input("Фамилия: ").strip()
        if surname:
            break
        else:
            print("Пустые данные недопустимы")
    while True:
        name = input("Имя: ").strip()
        if name:
            break
        else:
            print("Пустые данные недопустимы")
    while True:
        patronymic = input("Отчество: ").strip()
        if patronymic:
            break
        else:
            print("Пустые данные недопустимы")
    while True:
        org_name = input("Название организации: ").strip()
        if org_name:
            break
        else:
            print("Пустые данные недопустимы")
    while True:
        work_tel = input("Телефон рабочий: ").strip()
        if work_tel:
            break
        else:
            print("Пустые данные недопустимы")
    while True:
        mobile_tel = input("Телефон личный: ").strip()
        if mobile_tel:
            break
        else:
            print("Пустые данные недопустимы")

    contact = {
        "surname": surname,
        "name": name,
        "patronymic": patronymic,
        "org_name": org_name,
        "work_tel": work_tel,
        "mobile_tel": mobile_tel,
    }

    return contact


def add_contact(path) -> None:
    """Добавляет контакт в файл"""

    contact = get_contact_details()

    # Подтверждает, что контактов с введенными телефонными номерами нет в файле
    with open(path, mode="r") as file:
        reader = DictReader(file, fieldnames=fieldnames)

        for row in reader:
            if (
                row["mobile_tel"] == contact["mobile_tel"]
                or row["work_tel"] == contact["work_tel"]
            ):
                print(
                    "Существует контакт с введенными телефонными номерами. Проверьте данные."
                )
                return

    with open(path, mode="a") as file:
        writer = DictWriter(file, fieldnames=fieldnames)
        writer.writerow(contact)

    print("\nКонтакт успешно добавлен!")


def delete_contact(path) -> None:
    """Удаляет контакт из файла"""

    old_phone = input(
        "Введите мобильный телефонный контакта, которого вы хотите удалить: "
    ).strip()

    with open(path, mode="r") as file:
        reader = DictReader(file, fieldnames=fieldnames)
        new_data = []
        contact_found = False
        for row in reader:
            if row.get("mobile_tel") == old_phone:
                print(
                    f"Найден контакт: {row['surname']} {row['name']} {row['patronymic']} — {row['mobile_tel']}\n"
                )
                contact_found = True

                while True:
                    confirm_delete = input(
                        "Вы действительно хотите удалить данный контакт? y/n: "
                    ).strip()
                    match confirm_delete:
                        case "y":
                            break
                        case "n":
                            return
                        case _:
                            print("Ошибочный ответ. Введите y/n")
            else:
                new_data.append(row)
        if not contact_found:
            print("Данного номера телефона нет в справочнике")

    with open(path, mode="w") as new_file:
        writer = DictWriter(new_file, fieldnames=fieldnames)
        writer.writerows(new_data)

        print("Контакт успешно удален")


def edit_contact(path) -> None:
    """Редактирует контакт в файле"""

    old_phone = input(
        "Введите мобильный телефонный контакта, которого вы хотите отредактировать: "
    ).strip()

    # Считывает все контакты в память, редактирует нужный контакт
    with open(path, mode="r") as file:
        reader = DictReader(file, fieldnames=fieldnames)
        new_data = []
        contact_found = False
        for row in reader:
            if row.get("mobile_tel") == old_phone:
                print("Найден контакт: ")
                print_contacts([row])
                print("Введите новые данные контакта: ")
                new_data.append(get_contact_details())
                contact_found = True
            else:
                new_data.append(row)
        if not contact_found:
            print("Данного номера телефона нет в справочнике")

    # Сохраняет контакты в файл
    with open(path, mode="w") as new_file:
        writer = DictWriter(new_file, fieldnames=fieldnames)
        writer.writerows(new_data)

        print("Контакт успешно отредактирован")


def find_contact(path) -> None:
    """Находит контакт в файле"""

    with open(path, mode="r") as file:
        reader = DictReader(file, fieldnames=fieldnames)
        data = [row for row in reader]

    print("Выберите фильтр, по которым хотите искать контакт: ")

    while True:
        filter = input(
            """
1 – По фамилию
2 – По имя
3 – По отчетству
4 – По названию организации
5 – По рабочему тел
6 – По мобильному тел
0 — Выйти

>> """
        ).strip()

        match filter:
            case "1":
                surname = input("Введите фамилию: ").strip()
                contacts = [d for d in data if d["surname"].lower() == surname.lower()]
                if not contacts:
                    print("Не найден контакт")
                else:
                    print_headers()
                    for contact in contacts:
                        print_contacts([contact])
            case "2":
                name = input("Введите имя: ").strip()
                contacts = [d for d in data if d["name"].lower() == name.lower()]
                if not contacts:
                    print("Не найден контакт")
                else:
                    print_headers()
                    for contact in contacts:
                        print_contacts([contact])
            case "3":
                patronymic = input("Введите отчетство: ").strip()
                contacts = [
                    d for d in data if d["patronymic"].lower() == patronymic.lower()
                ]
                if not contacts:
                    print("Не найден контакт")
                else:
                    print_headers()
                    for contact in contacts:
                        print_contacts([contact])
            case "4":
                org_name = input("Введите название организации: ").strip()
                contacts = [
                    d for d in data if d["org_name"].lower() == org_name.lower()
                ]
                if not contacts:
                    print("Не найден контакт")
                else:
                    print_headers()
                    for contact in contacts:
                        print_contacts([contact])
            case "5":
                work_tel = input("Введите рабочий телефон: ").strip()
                contacts = [d for d in data if d["work_tel"] == work_tel]
                if not contacts:
                    print("Не найден контакт")
                else:
                    print_headers()
                    for contact in contacts:
                        print_contacts([contact])
            case "6":
                mobile_tel = input("Введите мобильный телефон: ").strip()
                contacts = [d for d in data if d["mobile_tel"] == mobile_tel]
                if not contacts:
                    print("Не найден контакт")
                else:
                    print_headers()
                    for contact in contacts:
                        print_contacts([contact])
            case "0":
                break
            case _:
                print("Ошибочный выбор. Введите фильтр от 1 до 6")


def view_contacts(path) -> None:
    """Считывает и печатает все контакты в файле"""

    with open(path, mode="r") as file:
        reader = DictReader(file)
        contacts = [row for row in reader]
        total = len(contacts)

        print("\nКонтакты")
        start = 0
        end = PAGINATION_NO

        # Текущая страница
        cur_page = 1

        # Количество страниц
        pages = ceil(total / PAGINATION_NO)

        # Постраничный вывод в консоль
        for i in range(pages):
            print(f"\nСтр. {cur_page} из {pages}")
            print_contacts(contacts[start:end], paginate=True)
            start += PAGINATION_NO
            end += PAGINATION_NO

            if cur_page < pages:
                while True:
                    next = input(
                        "\nВведите любую клавишу, чтобы листать или 0, чтобы выйти: "
                    ).strip()
                    if next != "0":
                        cur_page += 1
                        break
                    else:
                        return
            else:
                break
