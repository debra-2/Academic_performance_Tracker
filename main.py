import csv
import os
from datetime import datetime

# Configuration
SUBJECTS = ["Mathematics", "English", "Programming", "Business"]
DATA_FILE = "student_records.csv"
GRADING_SCALE = [
    (80, "A", "Excellent Performance"),
    (70, "B", "Very Good Performance"),
    (60, "C", "Good Performance"),
    (50, "D", "Needs Improvement"),
    (0, "E", "Poor Performance"),
]
VALID_MARKS_RANGE = (0, 100)


def get_student_input():
    """Get student name and validate it."""
    while True:
        name = input("\nEnter student name (or type 'back' to return to menu): ").strip()
        if name.lower() == "back":
            return None
        if len(name) < 2:
            print("Please enter a valid name (at least 2 characters).")
            continue
        return name


def get_marks_input():
    """Get marks for all subjects with validation."""
    marks = {}
    for subject in SUBJECTS:
        while True:
            try:
                mark = float(input(f"Enter {subject} marks (0-100): "))
                if not (VALID_MARKS_RANGE[0] <= mark <= VALID_MARKS_RANGE[1]):
                    print(f"Please enter marks between {VALID_MARKS_RANGE[0]} and {VALID_MARKS_RANGE[1]}.")
                    continue
                marks[subject] = mark
                break
            except ValueError:
                print("Please enter a valid number.")
    return marks


def calculate_stats(marks):
    """Calculate total, average, grade, and comment."""
    total = sum(marks.values())
    average = total / len(marks)
    
    for threshold, grade, comment in GRADING_SCALE:
        if average >= threshold:
            return total, average, grade, comment
    
    return total, average, "E", "Poor Performance"


def save_record(name, marks, total, average, grade):
    """Save student record to CSV file."""
    file_exists = os.path.isfile(DATA_FILE)
    
    with open(DATA_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        
        # Write header if file is new
        if not file_exists:
            header = ["Date", "Name"] + SUBJECTS + ["Total", "Average", "Grade"]
            writer.writerow(header)
        
        # Write student data
        row = [datetime.now().strftime("%Y-%m-%d %H:%M")] + [name] + list(marks.values()) + [total, round(average, 2), grade]
        writer.writerow(row)


def load_records():
    """Load all student records from CSV file."""
    if not os.path.isfile(DATA_FILE):
        return []
    
    records = []
    with open(DATA_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            records.append(row)
    
    return records


def search_student(name_query):
    """Search for students by name."""
    records = load_records()
    results = [r for r in records if name_query.lower() in r["Name"].lower()]
    return results


def display_report(name, marks, total, average, grade, comment):
    """Display formatted performance report."""
    print("\n" + "=" * 42)
    print("       PERFORMANCE REPORT")
    print("=" * 42)
    print(f"Student Name: {name}")
    print("-" * 42)
    for subject, mark in marks.items():
        print(f"{subject}: {mark}")
    print("-" * 42)
    print(f"Total Marks: {total}")
    print(f"Average: {round(average, 2)}")
    print(f"Grade: {grade}")
    print(f"Comment: {comment}")
    print("=" * 42)


def display_all_records():
    """Display all student records in a table format."""
    records = load_records()
    
    if not records:
        print("\nNo records found.")
        return
    
    print("\n" + "=" * 100)
    print(f"{'Date':<20} {'Name':<15} {'Math':<6} {'English':<8} {'Programming':<12} {'Business':<8} {'Avg':<6} {'Grade':<5}")
    print("=" * 100)
    
    for record in records:
        print(f"{record['Date']:<20} {record['Name']:<15} {record['Mathematics']:<6} {record['English']:<8} {record['Programming']:<12} {record['Business']:<8} {record['Average']:<6} {record['Grade']:<5}")
    
    print("=" * 100)


def class_statistics():
    """Display class-wide statistics."""
    records = load_records()
    
    if not records:
        print("\nNo records found.")
        return
    
    averages = [float(r["Average"]) for r in records]
    
    print("\n" + "=" * 50)
    print("       CLASS STATISTICS")
    print("=" * 50)
    print(f"Total Students: {len(records)}")
    print(f"Class Average: {sum(averages) / len(averages):.2f}")
    print(f"Highest Average: {max(averages):.2f}")
    print(f"Lowest Average: {min(averages):.2f}")
    
    # Subject-wise analysis
    subject_totals = {subject: 0 for subject in SUBJECTS}
    for record in records:
        for subject in SUBJECTS:
            subject_totals[subject] += float(record[subject])
    
    print("\nSubject Averages:")
    for subject, total in subject_totals.items():
        avg = total / len(records)
        print(f"  {subject}: {avg:.2f}")
    
    print("=" * 50)


def main_menu():
    """Display main menu and handle user choice."""
    while True:
        print("\n" + "=" * 42)
        print("   ACADEMIC PERFORMANCE TRACKER")
        print("=" * 42)
        print("1. Add New Student")
        print("2. View All Records")
        print("3. Search Student")
        print("4. Class Statistics")
        print("5. Exit")
        print("=" * 42)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            add_student()
        elif choice == "2":
            display_all_records()
        elif choice == "3":
            search_menu()
        elif choice == "4":
            class_statistics()
        elif choice == "5":
            print("\nThank you for using Academic Performance Tracker!")
            break
        else:
            print("Invalid choice. Please try again.")


def add_student():
    """Add a new student record."""
    name = get_student_input()
    if name is None:
        return
    
    marks = get_marks_input()
    total, average, grade, comment = calculate_stats(marks)
    
    display_report(name, marks, total, average, grade, comment)
    save_record(name, marks, total, average, grade)
    
    print("\nRecord saved successfully!")


def search_menu():
    """Search for student records."""
    name_query = input("\nEnter student name to search: ").strip()
    
    if not name_query:
        return
    
    results = search_student(name_query)
    
    if not results:
        print(f"\nNo records found for '{name_query}'.")
        return
    
    print(f"\nFound {len(results)} record(s):")
    print("\n" + "=" * 100)
    print(f"{'Date':<20} {'Name':<15} {'Math':<6} {'English':<8} {'Programming':<12} {'Business':<8} {'Avg':<6} {'Grade':<5}")
    print("=" * 100)
    
    for record in results:
        print(f"{record['Date']:<20} {record['Name']:<15} {record['Mathematics']:<6} {record['English']:<8} {record['Programming']:<12} {record['Business']:<8} {record['Average']:<6} {record['Grade']:<5}")
    
    print("=" * 100)


if __name__ == "__main__":
    main_menu()