import ttkbootstrap as tb
from ttkbootstrap.constants import *
from manager import DBManager

class ProveedorApp(tb.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)               # <— sin themename aquí
        self.title("Proveedores")
        self.geometry("600x400")

        self.db = DBManager("papeleria.db")
        cols = ("ID","Nombre","Contacto","Teléfono")
        self.tree = tb.Treeview(self, columns=cols, show="headings", bootstyle="dark")

        self._load_data()
        self._build_form()

    def _load_data(self):
        for row in self.db.fetchall("SELECT * FROM proveedores"):
            self.tree.insert("", "end", values=(row["id"], row["nombre"], row["contacto"], row["telefono"]))

    def _build_form(self):
        frm = tb.Frame(self, padding=10)
        frm.pack(fill=X, pady=10, padx=10)

        tb.Label(frm, text="Nombre:").grid(row=0, column=0, sticky=E, padx=5, pady=4)
        self.nombre = tb.Entry(frm, bootstyle="dark")
        self.nombre.grid(row=0, column=1, sticky=EW, padx=5, pady=4)

        tb.Label(frm, text="Contacto:").grid(row=1, column=0, sticky=E, padx=5, pady=4)
        self.contacto = tb.Entry(frm, bootstyle="dark")
        self.contacto.grid(row=1, column=1, sticky=EW, padx=5, pady=4)

        tb.Label(frm, text="Teléfono:").grid(row=2, column=0, sticky=E, padx=5, pady=4)
        self.telefono = tb.Entry(frm, bootstyle="dark")
        self.telefono.grid(row=2, column=1, sticky=EW, padx=5, pady=4)

        frm.columnconfigure(1, weight=1)
        tb.Button(frm, text="Agregar Proveedor", bootstyle="success", command=self._add).grid(
            row=3, column=0, columnspan=2, sticky=EW, pady=8
        )

    def _add(self):
        n = self.nombre.get().strip()
        c = self.contacto.get().strip()
        t = self.telefono.get().strip()
        if not n:
            tb.Messagebox.show_error("Error", "El nombre es obligatorio")
            return
        self.db.execute(
            "INSERT INTO proveedores (nombre, contacto, telefono) VALUES (?, ?, ?)",
            (n, c, t)
        )
        tb.Messagebox.show_info("Listo", "Proveedor agregado")
        for item in self.tree.get_children():
            self.tree.delete(item)
        self._load_data()
        self.nombre.clear(); self.contacto.clear(); self.telefono.clear()
