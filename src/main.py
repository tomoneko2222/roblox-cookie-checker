from tkinter import Tk, messagebox, ttk
import requests
from views.tab1 import Tab1
from views.tab2 import Tab2
from views.tab3 import Tab3

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("roblox cookie checker")
        self.root.geometry("600x400")

        # スタイルの設定
        style = ttk.Style()
        style.theme_use('clam')  # 'clam', 'alt', 'default', 'classic' などから選択
        style.configure('TNotebook.Tab', padding=[10, 10], font=('Helvetica', 12, 'bold'))
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('TButton', font=('Helvetica', 10, 'bold'))

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.tab1 = Tab1(self.notebook, self.validate_cookie)
        self.tab2 = Tab2(self.notebook)
        self.tab3 = Tab3(self.notebook)

        self.notebook.add(self.tab1, text='Input Cookie')
        self.notebook.add(self.tab2, text='Friend Info')
        self.notebook.add(self.tab3, text='Player Info')

    def validate_cookie(self, cookie):
        headers = {
            'Cookie': f'.ROBLOSECURITY={cookie}',
            'Content-Type': 'application/json'
        }
        response = requests.get('https://users.roblox.com/v1/users/authenticated', headers=headers)
        if response.status_code == 200:
            self.tab2.set_cookie(cookie)
            self.tab3.set_cookie(cookie)
            return True
        else:
            messagebox.showerror("Error", "Invalid cookie.")
            return False

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()