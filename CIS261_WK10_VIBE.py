# Joshua Goering
# CIS261
# WK10 VIBE Coding

import os
import sys

STORAGE_FILE = "student_grades.txt"

class Student:
    def __init__(self, name: str, student_id: str, test1: float, test2: float, test3: float):
        self.name = name.strip()
        self.student_id = student_id.strip()
        self.test1 = float(test1)
        self.test2 = float(test2)
        self.test3 = float(test3)
        self.average = self.calculate_average()
        self.grade = self.calculate_grade()

    def calculate_average(self) -> float:
        return round((self.test1 + self.test2 + self.test3) / 3.0, 2)

    def calculate_grade(self) -> str:
        average = self.average
        if average >= 90:
            return "A"
        if average >= 80:
            return "B"
        if average >= 70:
            return "C"
        if average >= 60:
            return "D"
        return "F"

    def to_pipe_record(self) -> str:
        return "|".join([
            self.name,
            self.student_id,
            f"{self.test1:.2f}",
            f"{self.test2:.2f}",
            f"{self.test3:.2f}",
            f"{self.average:.2f}",
            self.grade,
        ])

    @classmethod
    def from_pipe_record(cls, record: str):
        parts = [part.strip() for part in record.split("|")]
        if len(parts) != 7:
            raise ValueError("Invalid record format")
        name, student_id, test1, test2, test3, average, grade = parts
        student = cls(name, student_id, test1, test2, test3)
        # Keep the calculated average/grade consistent with the file if needed.
        student.average = float(average)
        student.grade = grade
        return student


def clear_screen() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def get_single_key(prompt: str = "") -> str:
    try:
        if os.name == "nt":
            import msvcrt
            sys.stdout.write(prompt)
            sys.stdout.flush()
            char = msvcrt.getch()
            if char in {b"\x00", b"\xe0"}:
                msvcrt.getch()
                return ""
            return char.decode("utf-8", errors="ignore")
        else:
            import termios
            import tty
            sys.stdout.write(prompt)
            sys.stdout.flush()
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                char = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return char
    except Exception:
        return input(prompt).strip()


def load_students() -> list[Student]:
    students: list[Student] = []
    if not os.path.exists(STORAGE_FILE):
        return students
    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    students.append(Student.from_pipe_record(line))
                except ValueError:
                    print(f"Warning: skipping malformed record: {line}")
    except OSError as error:
        print(f"Error loading records: {error}")
    return students


def save_students(students: list[Student]) -> None:
    try:
        with open(STORAGE_FILE, "w", encoding="utf-8") as file:
            for student in students:
                file.write(student.to_pipe_record() + "\n")
    except OSError as error:
        print(f"Error saving records: {error}")


def format_student_table(students: list[Student]) -> str:
    if not students:
        return "No student records available."
    widths = {
        "name": 20,
        "id": 12,
        "score": 8,
        "avg": 8,
        "grade": 6,
    }
    lines = []
    header = (
        f"{'Name':<{widths['name']}} | {'ID':<{widths['id']}} | {'Test1':>{widths['score']}} | "
        f"{'Test2':>{widths['score']}} | {'Test3':>{widths['score']}} | {'Average':>{widths['avg']}} | {'Grade':<{widths['grade']}}"
    )
    separator = "-" * len(header)
    lines.extend([header, separator])
    for student in students:
        lines.append(
            f"{student.name:<{widths['name']}} | {student.student_id:<{widths['id']}} | "
            f"{student.test1:>{widths['score']}.2f} | {student.test2:>{widths['score']}.2f} | "
            f"{student.test3:>{widths['score']}.2f} | {student.average:>{widths['avg']}.2f} | {student.grade:<{widths['grade']}}"
        )
    return "\n".join(lines)


def display_students(students: list[Student]) -> None:
    clear_screen()
    print("Student Records")
    print("===============\n")
    print(format_student_table(students))
    print()
    input("Press Enter to return to the menu...")


def display_statistics(students: list[Student]) -> None:
    clear_screen()
    print("Class Statistics")
    print("================\n")
    if not students:
        print("No student records to calculate statistics.")
    else:
        averages = [student.average for student in students]
        highest = max(averages)
        lowest = min(averages)
        class_average = round(sum(averages) / len(averages), 2)
        print(f"Highest average: {highest:.2f}")
        print(f"Lowest average : {lowest:.2f}")
        print(f"Class average  : {class_average:.2f}")
    print()
    input("Press Enter to return to the menu...")


def find_students_by_name(students: list[Student], search_name: str) -> list[Student]:
    search_lower = search_name.lower().strip()
    return [student for student in students if search_lower in student.name.lower()]


def print_search_results(results: list[Student], search_name: str) -> None:
    clear_screen()
    print(f"Search results for '{search_name}':")
    print("===============================\n")
    if not results:
        print("No matching students found.")
    else:
        print(format_student_table(results))
    print()
    input("Press Enter to return to the menu...")


def safe_float_input(prompt: str) -> float:
    while True:
        value = input(prompt).strip()
        try:
            score = float(value)
            if score < 0 or score > 100:
                print("Please enter a score between 0 and 100.")
                continue
            return score
        except ValueError:
            print("Invalid number. Enter a numeric score like 87.50.")


def add_student(students: list[Student]) -> None:
    clear_screen()
    print("Add New Student")
    print("===============\n")
    name = input("Student name: ").strip()
    if not name:
        print("Name cannot be blank.")
        input("Press Enter to continue...")
        return
    student_id = input("Student ID: ").strip()
    if not student_id:
        print("Student ID cannot be blank.")
        input("Press Enter to continue...")
        return
    test1 = safe_float_input("Test 1 score: ")
    test2 = safe_float_input("Test 2 score: ")
    test3 = safe_float_input("Test 3 score: ")
    student = Student(name, student_id, test1, test2, test3)
    students.append(student)
    print(f"\nStudent '{student.name}' added with average {student.average:.2f} and grade {student.grade}.")
    input("Press Enter to continue...")


def menu_choice() -> str:
    print("Choose an option or press ESC to exit:")
    print("1. Add new student")
    print("2. Display all students")
    print("3. Search student by name")
    print("4. Class statistics")
    print("5. Save records now")
    print("ESC. Exit program")
    choice = get_single_key("Enter choice: ")
    if choice == "\x1b":
        return "exit"
    return choice.strip()


def main() -> None:
    students = load_students()
    while True:
        clear_screen()
        print("WELCOME TO STUDENT GRADE CALCULATOR")
        print("=======================================\n")
        print("STUDENT GRADE CALCULATOR")
        print("========================\n")
        print(f"Loaded {len(students)} students from {STORAGE_FILE}.\n")
        choice = menu_choice()
        if choice == "exit":
            save_students(students)
            print("Student records saved. Exiting program.")
            break
        if choice == "1":
            add_student(students)
            continue
        if choice == "2":
            display_students(students)
            continue
        if choice == "3":
            search_name = input("Enter name to search: ").strip()
            if search_name:
                results = find_students_by_name(students, search_name)
                print_search_results(results, search_name)
            else:
                print("Search term cannot be blank.")
                input("Press Enter to continue...")
            continue
        if choice == "4":
            display_statistics(students)
            continue
        if choice == "5":
            save_students(students)
            print(f"Records saved to {STORAGE_FILE}.")
            input("Press Enter to continue...")
            continue
        print("Invalid selection. Please try again.")
        input("Press Enter to continue...")


if __name__ == "__main__":
    main()

