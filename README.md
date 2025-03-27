# Tkinter App

This project is an application created using Tkinter that allows users to input a cookie and verify its validity. Additionally, it uses the entered cookie to retrieve and display the user's friend information, player information, and owned game passes.

## Project Structure

- `src/app.py`: Entry point of the application. Sets up the Tkinter window and Notebook.
- `src/views/__init__.py`: Initialization file to import the views of the tabs.
- `src/views/tab1.py`: Defines the view of the first tab with an input field for the user to enter a cookie.
- `src/views/tab2.py`: Defines the view of the second tab that uses the cookie entered in the first tab to retrieve and display the account's friend information.
- `src/views/tab3.py`: Defines the view of the third tab that uses the cookie entered in the first tab to retrieve and display the player information.
- `src/views/tab_gamepasses.py`: Defines the view of the fourth tab that displays the owned game passes of the authenticated user.

## Setup Instructions

1. Clone the repository. Run the following command:
   ```
   git clone https://github.com/tomoneko2222/roblox-cookie-checker.git
   cd roblox-cookie-checker
   ```
2. Start the application. Run the following command:
   ```
   python src/main.py
   ```

## Note

This tool was created with the assistance of AI.
