# informacion.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from manager import DBManager

class InformacionApp(tb.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Facturación – Papelería")
        self.geometry("600x450")

        self.db = DBManager("papeleria.db")

        frm = tb.Frame(self, padding=10)
        frm.pack(fill=X)

        tb.Label(frm, text="ID de Venta:", font=("Segoe UI", 11)).grid(row=0, column=0, sticky=E, padx=5, pady=5)
        self.venta_id = tb.Entry(frm, bootstyle="dark")
        self.venta_id.grid(row=0, column=1, sticky=EW, padx=5, pady=5)

        frm.columnconfigure(1, weight=1)
        tb.Button(frm, text="Generar Factura", bootstyle="primary", command=self._generate).grid(
            row=1, column=0, columnspan=2, sticky=EW, pady=10
        )

        self.text = tk.Text(self, wrap="word", bg="#2b2b2b", fg="white", font=("Consolas", 10))
        self.text.pack(fill=BOTH, expand=True, padx=10, pady=(0,10))

    def _generate(self):
        vid = self.venta_id.get().strip()
        venta = self.db.fetchone("SELECT * FROM ventas WHERE id=?", (vid,))
        if not venta:
            tb.Messagebox.show_error("Error", "Venta no encontrada")
            return

        detalles = self.db.fetchall("""
            SELECT p.nombre, dv.cantidad, p.precio, dv.subtotal
            FROM detalle_ventas dv
            JOIN productos p ON dv.producto_id = p.id
            WHERE dv.venta_id = ?
        """, (vid,))

        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, f"----- FACTURA #{venta['id']} -----\n")
        self.text.insert(tk.END, f"Fecha: {venta['fecha']}\n\n")
        self.text.insert(tk.END, "Productos:\n")
        for d in detalles:
            self.text.insert(
                tk.END,
                f" • {d['nombre']}  |  Cant: {d['cantidad']}  |  P.U.: {d['precio']:.2f}  |  Subt: {d['subtotal']:.2f}\n"
            )
        self.text.insert(tk.END, f"\nTOTAL: {venta['total']:.2f}\n")
