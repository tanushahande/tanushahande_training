import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('courses.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    instructor TEXT NOT NULL,
    duration TEXT NOT NULL
)
''')
conn.commit()

def add_course():
    name = input("Enter course name: ").strip()
    instructor = input("Enter instructor name: ").strip()
    duration = input("Enter course duration (e.g., 10 weeks): ").strip()

    cursor.execute('INSERT INTO courses (name, instructor, duration) VALUES (?, ?, ?)', (name, instructor, duration))
    conn.commit()
    print("Course added successfully.\n")

def view_courses():
    cursor.execute('SELECT * FROM courses')
    courses = cursor.fetchall()
    if not courses:
        print("No courses found.\n")
        return
    print("\nCourses:")
    print("-" * 40)
    for course in courses:
        print(f"ID: {course[0]}")
        print(f"Name: {course[1]}")
        print(f"Instructor: {course[2]}")
        print(f"Duration: {course[3]}")
        print("-" * 40)
    print()

def update_course():
    course_id = input("Enter course ID to update: ").strip()
    cursor.execute('SELECT * FROM courses WHERE id = ?', (course_id,))
    course = cursor.fetchone()
    if not course:
        print("Course not found.\n")
        return

    print("Leave blank to keep current value.")
    new_name = input(f"Enter new name [{course[1]}]: ").strip()
    new_instructor = input(f"Enter new instructor [{course[2]}]: ").strip()
    new_duration = input(f"Enter new duration [{course[3]}]: ").strip()

    updated_name = new_name if new_name else course[1]
    updated_instructor = new_instructor if new_instructor else course[2]
    updated_duration = new_duration if new_duration else course[3]

    cursor.execute('''
        UPDATE courses
        SET name = ?, instructor = ?, duration = ?
        WHERE id = ?
    ''', (updated_name, updated_instructor, updated_duration, course_id))
    conn.commit()
    print("Course updated successfully.\n")

def delete_course():
    course_id = input("Enter course ID to delete: ").strip()
    cursor.execute('SELECT * FROM courses WHERE id = ?', (course_id,))
    course = cursor.fetchone()
    if not course:
        print("Course not found.\n")
        return

    confirm = input(f"Are you sure you want to delete course '{course[1]}'? (y/n): ").strip().lower()
    if confirm == 'y':
        cursor.execute('DELETE FROM courses WHERE id = ?', (course_id,))
        conn.commit()
        print("Course deleted successfully.\n")
    else:
        print("Deletion cancelled.\n")

def main_menu():
    while True:
        print("Course Management System")
        print("1. Add Course")
        print("2. View Courses")
        print("3. Update Course")
        print("4. Delete Course")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            add_course()
        elif choice == '2':
            view_courses()
        elif choice == '3':
            update_course()
        elif choice == '4':
            delete_course()
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main_menu()
    conn.close()
