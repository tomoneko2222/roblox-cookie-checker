from tkinter import Frame, Label
import requests
import threading

class Tab3(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.cookie = None

    def set_cookie(self, cookie):
        self.cookie = cookie
        threading.Thread(target=self.get_player_info).start()

    def get_player_info(self):
        headers = {
            'Cookie': f'.ROBLOSECURITY={self.cookie}',
            'Content-Type': 'application/json'
        }
        user_info_response = requests.get('https://users.roblox.com/v1/users/authenticated', headers=headers)
        if user_info_response.status_code != 200:
            self.display_message("Failed to authenticate user.")
            return

        user_info = user_info_response.json()
        user_id = user_info['id']
        username = user_info['name']
        display_name = user_info['displayName']

        # セキュリティ情報を取得
        security_info_response = requests.get('https://accountsettings.roblox.com/v1/email', headers=headers)
        if security_info_response.status_code != 200:
            self.display_message("Failed to retrieve security information.")
            return

        security_info = security_info_response.json()
        email = security_info.get('emailAddress', 'No email')
        is_verified = security_info.get('verified', False)

        # Robuxの残高を取得
        robux_info_response = requests.get('https://economy.roblox.com/v1/user/currency', headers=headers)
        if robux_info_response.status_code != 200:
            self.display_message("Failed to retrieve Robux information.")
            return

        robux_info = robux_info_response.json()
        robux = robux_info.get('robux', 0)

        self.display_player_info(user_id, username, display_name, email, is_verified, robux)

    def display_message(self, message):
        Label(self, text=message, anchor="w").pack(fill='x')

    def display_player_info(self, user_id, username, display_name, email, is_verified, robux):
        Label(self, text=f"User ID: {user_id}", anchor="w").pack(fill='x')
        Label(self, text=f"Username: {username}", anchor="w").pack(fill='x')
        Label(self, text=f"Display Name: {display_name}", anchor="w").pack(fill='x')
        Label(self, text=f"Email: {email}", anchor="w").pack(fill='x')
        Label(self, text=f"Email Verified: {is_verified}", anchor="w").pack(fill='x')
        Label(self, text=f"Robux: {robux}", anchor="w").pack(fill='x')
