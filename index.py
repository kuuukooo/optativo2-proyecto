# index.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from inventario import InventarioApp
from proveedor import ProveedorApp
from ventas import VentasApp
from informacion import InformacionApp

class MainApp(tb.Window):
    def __init__(self, user):
        super().__init__(themename="darkly")
        self.title("Sistema Libreria Ueno Bank HD 4K")
        self.geometry("640x400")

        tb.Label(self, text=f"Bienvenido, {user['username']}", 
                 font=("Segoe UI", 16, "bold")).pack(pady=20)

        grid = tb.Frame(self)
        grid.pack(expand=True, pady=10)

        opciones = [
            ("📦 Inventario", InventarioApp),
            ("🤝 Proveedores", ProveedorApp),
            ("💰 Ventas", VentasApp),
            ("🧾 Facturación", InformacionApp),
        ]
        for idx, (text, cls) in enumerate(opciones):
            btn = tb.Button(grid, text=text, bootstyle="info-outline", width=20,
                            command=lambda c=cls: c(self))
            btn.grid(row=idx//2, column=idx%2, padx=30, pady=15)
