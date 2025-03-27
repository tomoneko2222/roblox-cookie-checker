from tkinter import Frame, Label, Scrollbar, Canvas, VERTICAL, RIGHT, Y, BOTH, LEFT
import requests
import threading

class GamePassTab(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.cookie = None

        self.canvas = Canvas(self)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.content_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        self.content_frame.bind("<Configure>", self.on_frame_configure)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def set_cookie(self, cookie):
        self.cookie = cookie
        threading.Thread(target=self.get_gamepasses).start()

    def get_gamepasses(self):
        # Clear the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        headers = {
            'Cookie': f'.ROBLOSECURITY={self.cookie}',
            'Content-Type': 'application/json'
        }

        user_info_response = requests.get('https://users.roblox.com/v1/users/authenticated', headers=headers)
        if user_info_response.status_code != 200:
            Label(self.content_frame, text="Failed to authenticate user.", anchor="w").pack(fill='x')
            return

        user_id = user_info_response.json().get('id')

        gamepasses_url = f'https://apis.roblox.com/game-passes/v1/users/{user_id}/game-passes?count=100'
        gamepasses_response = requests.get(gamepasses_url, headers=headers)
        if gamepasses_response.status_code == 200:
            gamepasses = gamepasses_response.json()
            if not gamepasses or 'gamePasses' not in gamepasses:
                Label(self.content_frame, text="No game passes found.", anchor="w").pack(fill='x')
                return

            gamepasses_list = gamepasses['gamePasses']  # 修正: 正しいキーを使用
            Label(self.content_frame, text="Owned Game Passes:", anchor="w", font=("Helvetica", 12, "bold")).pack(fill='x', pady=10)
            for gamepass in gamepasses_list:
                name = gamepass.get('name', 'Unknown Name')
                gamepass_id = gamepass.get('id', 'Unknown ID')
                creator = gamepass.get('creator', {}).get('name', 'Unknown Creator')
                price = gamepass.get('price', 'Unknown Price')

                Label(
                    self.content_frame,
                    text=f"- {name} (ID: {gamepass_id})\n  Creator: {creator}, Price: {price} Robux",
                    anchor="w",
                    justify="left"
                ).pack(fill='x', pady=5)
        else:
            Label(self.content_frame, text="Failed to retrieve game passes.", anchor="w").pack(fill='x')