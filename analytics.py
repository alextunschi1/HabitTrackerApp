# Description: This file contains the analytics functions for the Habit Tracker app

# Import the datetime module to work with dates and times
# Import the relativedelta module to work with relativedelta objects

from dateutil.relativedelta import relativedelta, MO

# Define a function that returns True if the two dates are in the same week
def are_dates_in_same_week(date1, date2):
    # Get the start of the week for each date
    week_start1 = date1 + relativedelta(weekday=MO(-1))
    week_start2 = date2 + relativedelta(weekday=MO(-1))
    # Return True if the dates are in the same week
    return week_start1.date() == week_start2.date()

# Define a function that returns all habits
def get_all_habits(habits):
    return habits

# Define a function that returns all habits by frequency
def get_habits_by_frequency(habits, frequency):
    # Return all habits that match the frequency
    return [habit for habit in habits if habit.habitfrequency == frequency]

# Define a function that returns the longest streak for a habit
def get_longest_streak(habits):
    max_streak = 0
    max_habit = None
    # Loop through all habits
    for habit in habits:
        # Calculate the longest streak for the habit
        streak = get_longest_streak_for_habit(habit)
        # Update the max streak and max habit if the current streak is greater than the max streak
        if streak > max_streak:
            max_streak = streak
            max_habit = habit
    # Return the max habit and max streak
    return max_habit, max_streak

# Define a function that returns the longest streak for a habit
def get_longest_streak_for_habit(habit):
    streak = 0
    longest_streak = 0
    prev_date = None
    # Loop through all completion dates
    for completion_date in sorted(habit.completion_dates):
        # Check if the completion date is the next day or week
        if prev_date:
            # Check if the habit is completed daily and the completion date is the next day
            #if habit.habitfrequency == "daily" and completion_date.date() == prev_date.date() + timedelta(days=1):
            if habit.habitfrequency == "daily" and completion_date.date() == prev_date.date() + relativedelta(days=1):

                streak += 1
            # Check if the habit is completed weekly and the completion date is the next week
            #elif habit.habitfrequency == "weekly" and are_dates_in_same_week(completion_date, prev_date + timedelta(weeks=1)):
            elif habit.habitfrequency == "weekly" and are_dates_in_same_week(completion_date, prev_date + relativedelta(weeks=1)):

                streak += 1
            else:
                streak = 1
        else:
            streak = 1
        # Update the longest streak
        longest_streak = max(longest_streak, streak)
        # Update the previous date
        prev_date = completion_date
    # Return the longest streak
    return longest_streak