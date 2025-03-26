from tkinter import Frame, Label, Scrollbar, VERTICAL, RIGHT, Y, BOTH, Canvas, LEFT
import requests
import threading

class Tab2(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.cookie = None

        self.canvas = Canvas(self)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.v_scrollbar = Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        self.content_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        self.content_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def set_cookie(self, cookie):
        self.cookie = cookie
        threading.Thread(target=self.get_friends_info).start()

    def get_friends_info(self):
        # Clear the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        headers = {
            'Cookie': f'.ROBLOSECURITY={self.cookie}',
            'Content-Type': 'application/json'
        }
        user_info_response = requests.get('https://users.roblox.com/v1/users/authenticated', headers=headers)
        if user_info_response.status_code != 200:
            self.display_message("Failed to authenticate user.")
            return

        user_id = user_info_response.json()['id']
        friends_response = requests.get(f'https://friends.roblox.com/v1/users/{user_id}/friends', headers=headers)
        if friends_response.status_code != 200:
            self.display_message("Failed to retrieve friends information.")
            return

        friends = friends_response.json()['data']
        for friend in friends:
            friend_id = friend['id']
            friend_name = friend['name']
            presence_response = requests.post('https://presence.roblox.com/v1/presence/users', headers=headers, json={"userIds": [friend_id]})
            if presence_response.status_code == 200:
                presence_data = presence_response.json()['userPresences'][0]
                status_code = presence_data['userPresenceType']
                place_name = presence_data.get('lastLocation', 'N/A')
                if place_name == "Website":
                    place_name = "N/A"
                status = ["Offline", "Online", "In Game", "In Studio"][status_code] if status_code < 4 else "Unknown"
            else:
                status = "Unknown"
                place_name = "N/A"

            self.display_friend_info(friend_id, friend_name, status, place_name)

    def display_message(self, message):
        Label(self.content_frame, text=message, anchor="w").pack(fill='x')

    def display_friend_info(self, friend_id, friend_name, status, place_name):
        Label(self.content_frame, text=f"ID: {friend_id}, Name: {friend_name}, Status: {status}, Place: {place_name}", anchor="w").pack(fill='x')