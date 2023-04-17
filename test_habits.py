# Description: Unit tests for the HabitClass and analytics functions

# Import the datetime module to work with dates and times
# Import the pytest module to run unit tests
# Import the sqlite3 module to work with SQLite databases
# Import the HabitClass from the habit_app module
# Import the init_db, add_habit, delete_habit, get_all_habits, and add_completion functions from the habit_app module
# Import the analytics functions from the analytics module
import pytest
import sqlite3
from datetime import datetime, timedelta
import analytics
from habit_app import HabitClass, init_db, add_habit, delete_habit, get_all_habits, add_completion

def test_habit_creation():
    habit = HabitClass(1, "Test Habit Creation", "daily", datetime.now(), [])
    assert habit.habitname == "Test Habit Creation"
    assert habit.habitfrequency == "daily"
    assert len(habit.completion_dates) == 0

def test_complete_daily_habit():
    habit = HabitClass(1, "Test Habit Complete Daily", "daily", datetime.now(), [])
    assert habit.complete() == True
    assert habit.is_completed_today() == True
    assert len(habit.completion_dates) == 1

def test_complete_weekly_habit():
    habit = HabitClass(1, "Test Habit Complete Weekly", "weekly", datetime.now(), [])
    assert habit.complete() == True
    assert habit.is_completed_this_week() == True
    assert len(habit.completion_dates) == 1

def test_get_longest_streak_for_habit():
    completion_dates = [
        datetime.now() - timedelta(days=4),
        datetime.now() - timedelta(days=3),
        datetime.now() - timedelta(days=2),
        datetime.now() - timedelta(days=1),
    ]
    habit = HabitClass(1, "Test Habit Get Longest Streak for habit", "daily", datetime.now(), completion_dates)
    assert analytics.get_longest_streak_for_habit(habit) == 4

def test_get_longest_streak():
    completion_dates1 = [
        datetime.now() - timedelta(days=4),
        datetime.now() - timedelta(days=3),
        datetime.now() - timedelta(days=2),
        datetime.now() - timedelta(days=1),
    ]
    completion_dates2 = [
        datetime.now() - timedelta(weeks=2),
        datetime.now() - timedelta(weeks=1),
    ]
    habits = [
        HabitClass(1, "Test Habit 1 Get Longest Streak", "daily", datetime.now(), completion_dates1),
        HabitClass(2, "Test Habit 2 Get Longest Streak", "weekly", datetime.now(), completion_dates2),
    ]
    longest_streak_habit, longest_streak = analytics.get_longest_streak(habits)
    assert longest_streak_habit.habitname == "Test Habit 1 Get Longest Streak"
    assert longest_streak == 4

@pytest.fixture
def db_connection():
    init_db()
    connection = sqlite3.connect("habits.db")
    yield connection
    connection.close()


def test_add_habit(db_connection):
    habit_name = "Test Habit"
    habit_frequency = "daily"
    habit = add_habit(habit_name, habit_frequency)
    assert habit.habitname == habit_name
    assert habit.habitfrequency == habit_frequency

    cur = db_connection.cursor()
    habit_data = cur.execute("SELECT * FROM habits WHERE id = ?", (habit.id,)).fetchone()
    assert habit_data is not None
    assert habit_data[1] == habit_name
    assert habit_data[2] == habit_frequency

def test_delete_habit(db_connection):
    habit_name = "Test Habit"
    habit_frequency = "daily"
    habit = add_habit(habit_name, habit_frequency)
    delete_habit(habit.id)

    cur = db_connection.cursor()
    habit_data = cur.execute("SELECT * FROM habits WHERE id = ?", (habit.id,)).fetchone()
    assert habit_data is None

def test_get_all_habits(db_connection):
    habit_name = "Test Habit"
    habit_frequency = "daily"
    habit = add_habit(habit_name, habit_frequency)
    all_habits = get_all_habits()
    habit_found = False
    for h in all_habits:
        if h.id == habit.id:
            habit_found = True
            assert h.habitname == habit_name
            assert h.habitfrequency == habit_frequency
            assert len(h.completion_dates) == 0
    assert habit_found

def test_add_completion(db_connection):
    habit_name = "Test Habit"
    habit_frequency = "daily"
    habit = add_habit(habit_name, habit_frequency)
    habit.complete()
    add_completion(habit)

    cur = db_connection.cursor()
    completion_data = cur.execute("SELECT completion_date FROM completions WHERE habit_id = ?", (habit.id,)).fetchall()
    assert len(completion_data) == 1

def test_get_longest_streak_for_habit_various_dates():
    completion_dates = [
        datetime.now() - timedelta(days=6),
        datetime.now() - timedelta(days=5),
        datetime.now() - timedelta(days=4),
        datetime.now() - timedelta(days=1),
    ]
    habit = HabitClass(1, "Test Habit", "daily", datetime.now(), completion_dates)
    assert analytics.get_longest_streak_for_habit(habit) == 3

def test_get_longest_streak_for_weekly_habit():
    completion_dates = [
        datetime.now() - timedelta(weeks=4),
        datetime.now() - timedelta(weeks=3),
        datetime.now() - timedelta(weeks=1),
    ]
    habit = HabitClass(1, "Test Habit", "weekly", datetime.now(), completion_dates)
    assert analytics.get_longest_streak_for_habit(habit) == 2
