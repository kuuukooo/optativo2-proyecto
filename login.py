# login.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from manager import DBManager
import index

class LoginApp(tb.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Login - Papeleraía Ueno Bank HD 4K")
        self.geometry("360x240")
        self.resizable(False, False)
        self.db = DBManager()
        
        frame = tb.Frame(self, padding=20)
        frame.pack(expand=True)
        
        # Labels sin font directo, usando el tema por defecto
        tb.Label(frame, text="Usuario:").pack(anchor=W, pady=(0,5))
        self.user_entry = tb.Entry(frame, bootstyle="dark")
        self.user_entry.pack(fill=X, pady=5)
        
        tb.Label(frame, text="Contraseña:").pack(anchor=W, pady=(10,5))
        self.pass_entry = tb.Entry(frame, show="*", bootstyle="dark")
        self.pass_entry.pack(fill=X, pady=5)
        
        # Botón simplificado sin font
        tb.Button(
            frame,
            text="Ingresar",
            command=self.login,
            bootstyle="success"
        ).pack(fill=X, pady=5)
    
    def login(self):
        u = self.user_entry.get()
        p = self.pass_entry.get()
        user = self.db.fetchone(
            "SELECT * FROM usuarios WHERE username=? AND password=?", (u, p)
        )
        if user:
            self.destroy()
            app = index.MainApp(user)
            app.mainloop()
        else:
            Messagebox.show_error("Error", "Credenciales inválidas")

if __name__ == "__main__":
    LoginApp().mainloop()