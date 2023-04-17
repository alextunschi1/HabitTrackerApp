# Description: A habit tracker app that allows users to create, complete, and delete habits. The app also allows users to view analytics for their habits. 
# The app uses a SQLite database to store habit information and completion dates. The app uses the HabitClass to store habit information and the analytics module to calculate habit analytics.

# Import the sqlite3 module to work with SQLite databases
# Import the analytics module to work with habit analytics
# Import the datetime module to work with dates and times
# Import the relativedelta module to work with relative dates and times

import sqlite3
from datetime import datetime
import analytics
from dateutil.relativedelta import relativedelta, MO


# Define the database name
Database_Name = "habits.db"

# Initialize a HabitClass instance with habit information
class HabitClass:
    # Initialize a habit with an id, name, frequency, creation date, and completion dates
    def __init__(self, id, name_of_habit, frequency_of_habit, creation_date, completion_dates):
        # Initialize the habit with the given id, name, frequency, creation date, and completion dates
        self.id = id
        self.habitname = name_of_habit
        self.habitfrequency = frequency_of_habit
        self.creation_date = creation_date
        self.completion_dates = completion_dates

    # Complete a habit if it is not already completed in the current period (today or this week)
    def complete(self):
        # Get the current date and time
        now = datetime.now()
        # If the habit is completed daily and it is not completed today, add the current date and time to the completion dates and return True
        if self.habitfrequency == "daily" and not self.is_completed_today():
            # Add the current date and time to the completion dates
            self.completion_dates.append(now)
            return True
        # If the habit is completed weekly and it is not completed this week, add the current date and time to the completion dates and return True
        elif self.habitfrequency == "weekly" and not self.is_completed_this_week():
            # Add the current date and time to the completion dates
            self.completion_dates.append(now)
            return True
        return False
    
    # Check if a habit is completed today
    def is_completed_today(self):
        # Get the current date
        today = datetime.now().date()
        # Check if the current date is in the completion dates
        return any(d.date() == today for d in self.completion_dates)

    # Check if a habit is completed this week
    def is_completed_this_week(self):
        # Get the current date
        now = datetime.now()
        # Get the start of the week
        week_start = now + relativedelta(weekday=MO(-1))
        # Get the end of the week
        week_end = week_start + relativedelta(days=6)
        # Check if the current date is in the completed weeks, return True if it is
        return any(week_start.date() <= d.date() <= week_end.date() for d in self.completion_dates)

# Initialize the SQLite database with habits and completions tables
def init_db():
    # Connect to the database
    conn = sqlite3.connect(Database_Name)
    # Create a cursor
    cur = conn.cursor()
    # Create the habits table if it does not exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            /* Define the id column as the primary key */
            id INTEGER PRIMARY KEY,
            /* Define the name column as a text field that cannot be null */
            name TEXT NOT NULL,
            /* Define the frequency column as a text field that cannot be null */
            frequency TEXT NOT NULL,
            /* Define the creation_date column as a text field that cannot be null */
            creation_date TEXT NOT NULL
        );
    """)
    # Create the completions table if it does not exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS completions (
            /* Define the id column as the primary key */
            id INTEGER PRIMARY KEY,
            /* Define the habit_id column as an integer that cannot be null */
            habit_id INTEGER NOT NULL,
            /* Define the completion_date column as a text field that cannot be null */
            completion_date DATE,
            /* Define the habit_id column as a foreign key that references the id column in the habits table */
            FOREIGN KEY (habit_id) REFERENCES habits (id)
        );
    """)
    # Commit the changes
    conn.commit()
    # Close the connection
    conn.close()

# Add a new habit to the database
def add_habit(name, frequency):
    # Connect to the database
    conn = sqlite3.connect(Database_Name)
    # Create a cursor
    cur = conn.cursor()

    # Insert the habit into the habits table
    cur.execute("INSERT INTO habits (name, frequency, creation_date) VALUES (?, ?, ?)", (name, frequency, datetime.now()))
    # Commit the changes
    conn.commit()

    # Get the id of the habit that was just added
    habit_id = cur.lastrowid

    # Close the connection
    conn.close()

    # Return a HabitClass instance with the habit information
    return HabitClass(habit_id, name, frequency, datetime.now(), [])

# Delete a habit from the database
def delete_habit(habit_id):
    # Connect to the database
    conn = sqlite3.connect(Database_Name)
    # Create a cursor
    cur = conn.cursor()

    # Delete the habit from the habits table and the completions table
    cur.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    # Delete the habit from the completions table
    cur.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))

    # Commit the changes
    conn.commit()
    # Close the connection
    conn.close()

# Get all habits from the database
def get_all_habits():
    # Connect to the database
    conn = sqlite3.connect(Database_Name)
    # Create a cursor
    cur = conn.cursor()

    # Get all habits from the habits table
    habits_data = cur.execute("SELECT * FROM habits").fetchall()

    
    # Create a list of HabitClass instances
    habits = []
    # Loop through each habit
    for habit_data in habits_data:
        # Get the habit id, name, frequency, and creation date
        id, name, frequency, creation_date = habit_data
        # Convert the creation date from a string to a datetime object
        creation_date = datetime.fromisoformat(creation_date)

        # Get all completion dates for the habit
        completion_dates_data = cur.execute("SELECT completion_date FROM completions WHERE habit_id = ?", (id,)).fetchall()
        # Convert the completion dates from strings to datetime objects
        completion_dates = [datetime.fromisoformat(cd[0]) for cd in completion_dates_data]
        # Add the habit to the list of habits
        habits.append(HabitClass(id, name, frequency, creation_date, completion_dates))

    # Close the connection
    conn.close()
    # Return the list of habits
    return habits

# Add a completion to the database
def add_completion(habit):
    # Connect to the database
    conn = sqlite3.connect(Database_Name)
    # Create a cursor
    cur = conn.cursor()

    # Insert the completion into the completions table
    cur.execute("INSERT INTO completions (habit_id, completion_date) VALUES (?, ?)", (habit.id, datetime.now().date()))
    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

# Main function that handles user input and interaction with the habit tracker
def main():
    # Initialize the database
    init_db()
    # Get all habits from the database
    habits = get_all_habits()

# Main loop for user interaction
    while True:
        # Print the main menu
        print("\n1. Create habit\n2. Delete habit\n3. Check all habits\n4. Complete habit\n5. Analyze habits\n6. Exit")
        # Get the user's choice
        choice = input("Enter your choice: ")

        # Create a new habit
        if choice == '1':
            # Get the habit name and frequency
            name = input("Enter habit name: ")
            if not (3 <= len(name) <= 20):
                print("Habit name must be between 3 and 20 characters.")
                continue

            frequency = input("Enter habit frequency (daily/weekly): ").lower()
            if frequency not in ["daily", "weekly"]:
                print("Invalid frequency. Please enter 'daily' or 'weekly'.")
                continue
            
            # Add the habit to the database
            habit = add_habit(name, frequency)
            # Add the habit to the list of habits
            habits.append(habit)
            # Print a success message
            print(f"Habit '{name}' added.")
        
        # Delete an existing habit
        elif choice == '2':
            # Get the habit id
            id = int(input("Enter habit ID: "))
            # Get the habit from the list of habits
            habit = next((h for h in habits if h.id == id), None)

            # Check if the habit exists
            if not habit:
                # Print an error message if the habit does not exist
                print("Habit not found.")
                continue

            # Delete the habit from the database
            delete_habit(id)
            # Remove the habit from the list of habits
            habits.remove(habit)
            # Print a success message
            print(f"Habit '{habit.habitname}' deleted.")
        
        # Check the status of all habits
        elif choice == '3':
            print("\nHabits:")
            # Loop through each habit
            for habit in habits:
                # Check if the habit has been completed for the current period
                status = "Completed" if (habit.habitfrequency == "daily" and habit.is_completed_today()) or (habit.habitfrequency == "weekly" and habit.is_completed_this_week()) else "Not completed"
                # Print the habit id, name, frequency, and status
                print(f"{habit.id}: {habit.habitname} ({habit.habitfrequency.capitalize()}) - {status}")
        
        # Complete a habit
        elif choice == '4':
            # Get the habit id
            id = int(input("Enter habit ID: "))
            # Get the habit from the list of habits
            habit = next((h for h in habits if h.id == id), None)

            # Check if the habit exists
            if not habit:
                # Print an error message if the habit does not exist
                print("Habit not found.")
                continue
            
            # Complete the habit
            if habit.complete():
                # Add the completion to the database
                add_completion(habit)
                # Print a success message
                print(f"Habit '{habit.habitname}' completed.")
            else:
                # Print an error message if the habit has already been completed for the current period
                print("Habit has already been completed for this period.")
        
        # Analyze habits
        elif choice == '5':
            # Print the analysis menu
            print("\n1. List all habits\n2. List habits by frequency\n3. Get longest streak of all habits\n4. Get longest streak for a habit")
            # Get the user's choice
            analysis_choice = input("Enter your choice: ")

            # List all habits
            if analysis_choice == '1':
                # Get all habits
                all_habits = analytics.get_all_habits(habits)
                print("All habits:")
                # Loop through each habit
                for habit in all_habits:
                    # Print the habit id and name
                    print(f"{habit.id}: {habit.habitname} ({habit.habitfrequency.capitalize()})")
            
            # List habits by frequency
            elif analysis_choice == '2':
                # Get daily and weekly habits
                daily_habits = analytics.get_habits_by_frequency(habits, "daily")
                weekly_habits = analytics.get_habits_by_frequency(habits, "weekly")
                # Print the daily and weekly habits
                print("Daily habits:")
                # Loop through each daily habit
                for habit in daily_habits:
                    # Print the habit id and name
                    print(f"{habit.id}: {habit.habitname}")

                print("\nWeekly habits:")
                # Loop through each weekly habit
                for habit in weekly_habits:
                    # Print the habit id and name
                    print(f"{habit.id}: {habit.habitname}")
            
            # Get longest streak of all habits
            elif analysis_choice == '3':
                # Get the longest streak
                longest_streak_habit, longest_streak = analytics.get_longest_streak(habits)
                # Print the longest streak based on frequency (daily or weekly)
                if longest_streak_habit.habitfrequency == "daily":
                    print(f"Longest streak of all habits: '{longest_streak_habit.habitname}' (daily, {longest_streak} days)")
                else:
                    print(f"Longest streak of all habits: '{longest_streak_habit.habitname}' (weekly, {longest_streak} weeks)")

            # Get longest streak for a habit
            elif analysis_choice == '4':
                # Get the habit id
                id = int(input("Enter habit ID: "))
                # Get the habit from the list of habits
                habit = next((h for h in habits if h.id == id), None)

                # Check if the habit exists
                if not habit:
                    # Print an error message if the habit does not exist
                    print("Habit not found.")
                    continue
                # Get the longest streak for habit
                longest_streak = analytics.get_longest_streak_for_habit(habit)
                # Print the longest streak based on frequency (daily or weekly)
                if habit.habitfrequency == "daily":
                    print(f"Longest streak for habit '{habit.habitname}': {longest_streak} days")
                else:
                    print(f"Longest streak for habit '{habit.habitname}': {longest_streak} weeks")
            else:
                # Print an error message if the user enters an invalid choice
                print("Invalid choice. Please try again.")
        
        # Exit the program
        elif choice == '6':
            # Print a goodbye message
            print("Have an amazing day!")
            # Exit the loop
            break
        else:
            # Print an error message if the user enters an invalid choice
            print("Invalid choice. Please try again.")

# Run the main function
if __name__ == "__main__":
    main()