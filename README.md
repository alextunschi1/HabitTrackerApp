# HabitTrackerApp
Simple command-line habit tracking application

This is a  simple command-line habit tracking application that helps users build and maintain habits by keeping track of their progress.

Features
Add and delete habits
Set habit frequency (daily or weekly)
Mark habits as complete
View all habits and their completion status
Analyze habits (list all habits, list habits by frequency, get longest streak for all habits, get longest streak for a specific habit)

Installation
Clone the repository:
git clone https://github.com/yourusername/habit-tracker.git
Navigate to the project folder:
cd habit-tracker
Install the required Python libraries:
pip install -r requirements.txt

Usage
Run the application using Python:
python habit_app.py
The application presents a straightforward menu with options to create, delete, check, complete, or analyze habits. Follow the prompts to interact with your habits.

You can test the app by using this command:
pytest
After the tests, remember to delete the 3 test habits that are created in the database.

Dependencies
Python 3.6+
SQLite3
dateutil

Contributing
If you want to contribute to this project, feel free to fork the repository, make changes, and submit a pull request.

License
MIT License
