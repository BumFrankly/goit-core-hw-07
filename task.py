from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        sanitized_value = ''.join(char for char in value if char.isdigit() or char in {'+', '-', '(', ')'})
        if len(sanitized_value) != 10:
            raise ValueError("Phone number must contain 10 digits.")
        self.value = sanitized_value


class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        try:
            phone = Phone(phone)
            self.phones.append(phone)
        except ValueError as e:
            raise ValueError(f"Error adding phone: {e}")

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError("Phone number not found in record.")

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                try:
                    new_phone = Phone(new_phone)
                except ValueError as e:
                    raise ValueError(f"Error: {e}")
                p.value = new_phone.value
                return
        raise ValueError("Phone number not found in record.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        try:
            self.birthday = Birthday(birthday)
        except ValueError as e:
            raise ValueError(f"Error adding birthday: {e}")

    def __str__(self):
        phones_str = ', '.join(str(phone.value) for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {self.birthday.value if self.birthday else None}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete_record(self, name):
        if name in self.data:
            del self.data[name]
            print("Record removed successfully.")
        else:
            print("Record not found.")

    def find_record(self, name):
        return self.data.get(name)

    def show_all_records(self):
        if self.data:
            print("All records in the address book:")
            for name, record in self.data.items():
                print(f"{name}: {record}")
        else:
            print("Address book is empty.")

    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = datetime.now().date()
        for record in self.data.values():
            if record.birthday:
                if (record.birthday.date - today).days <= days:
                    upcoming_birthdays.append(record.name.value)
        return upcoming_birthdays


def add_birthday(args, book):
    if len(args) < 2:
        return "Not enough arguments. Please provide both name and birthday (DD.MM.YYYY)."
    
    name, birthday = args
    record = book.find_record(name)
    if record:
        if record.birthday:
            return f"Birthday already exists for {name}."
        else:
            try:
                record.add_birthday(birthday)
                return f"Birthday added successfully for {name}."
            except ValueError as e:
                return f"Error adding birthday: {e}"
    else:
        return "Record not found."



def show_birthday(args, book):
    name = args[0]
    record = book.find_record(name)
    if record and record.birthday:
        print(f"{name}'s birthday: {record.birthday.value}")
    elif record:
        print(f"{name} has no birthday information.")
    else:
        print("Record not found.")


def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        print("Upcoming birthdays:")
        for name in upcoming_birthdays:
            print(name)
    else:
        print("No upcoming birthdays in the next 7 days.")


def parse_input(user_input):
    return user_input.split()


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phones(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add_birthday":
            print(add_birthday(args, book))

        elif command == "show_birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


def add_contact(args, book: AddressBook):
    if len(args) < 2:
        return "Not enough arguments. Please provide both name and phone number."
    name, phone, *_ = args
    record = book.find_record(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


def change_contact(args, book: AddressBook):
    if len(args) < 2:
        return "Not enough arguments. Please provide both name and new phone number."
    name, new_phone = args
    record = book.find_record(name)
    if record:
        try:
            record.edit_phone(record.phones[0].value, new_phone)
            return f"Phone number updated for {name}."
        except ValueError as e:
            return f"Error: {e}"
    else:
        return "Record not found."


def show_phones(args, book: AddressBook):
    if len(args) < 1:
        return "Not enough arguments. Please provide a name."
    name = args[0]
    record = book.find_record(name)
    if record:
        phones = ', '.join(phone.value for phone in record.phones)
        return f"Phones for {name}: {phones}"
    else:
        return f"Record for {name} not found."


def show_all(book: AddressBook):
    if book.data:
        return "\n".join(f"{name}: {record}" for name, record in book.data.items())
    else:
        return "Address book is empty."


if __name__ == "__main__":
    main()
