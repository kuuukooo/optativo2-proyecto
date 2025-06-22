# ventas.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from manager import DBManager
from datetime import datetime

class VentasApp(tb.Toplevel):
    def __init__(self, parent):
        super().__init__(parent) 
        self.title("Ventas")
        self.geometry("800x600")

        self.db = DBManager("papeleria.db")
        self.cart = []

        self._build_selection_frame()
        self._build_cart_tree()
        self._build_total_frame()

    def _build_selection_frame(self):
        frm = tb.Labelframe(self, text="Agregar al carrito", padding=10)
        frm.pack(fill=X, padx=10, pady=(10, 0))

        tb.Label(frm, text="Producto:").grid(row=0, column=0, sticky=E, padx=5, pady=4)
        products = self.db.fetchall("SELECT id, nombre FROM productos WHERE cantidad>0")
        self.product_map = {row["nombre"]: row["id"] for row in products}
        self.prod_combo = tb.Combobox(frm, values=list(self.product_map.keys()), bootstyle="dark", state="readonly")
        self.prod_combo.grid(row=0, column=1, sticky=EW, padx=5, pady=4)

        tb.Label(frm, text="Cantidad:").grid(row=1, column=0, sticky=E, padx=5, pady=4)
        self.qty_entry = tb.Entry(frm, bootstyle="dark")
        self.qty_entry.grid(row=1, column=1, sticky=EW, padx=5, pady=4)

        frm.columnconfigure(1, weight=1)
        tb.Button(frm, text="Agregar", bootstyle="info", command=self._add_to_cart).grid(
            row=2, column=0, columnspan=2, sticky=EW, pady=8
        )

    def _build_cart_tree(self):
        cols = ("Producto", "Cantidad", "Precio U.", "Subtotal")
        self.tree = tb.Treeview(self, columns=cols, show="headings", bootstyle="dark")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=180, anchor=CENTER)
        self.tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

    def _build_total_frame(self):
        frm = tb.Frame(self)
        frm.pack(fill=X, padx=10, pady=(0,10))

        tk.Label(frm, text="Total:", font=("Segoe UI", 12), fg="white", bg=frm.cget("background")).grid(
            row=0, column=0, sticky=E, padx=5
        )
        self.total_var = tk.StringVar(value="0.00")
        tk.Label(frm, textvariable=self.total_var, font=("Segoe UI", 12, "bold"),
                 fg="white", bg=frm.cget("background")).grid(row=0, column=1, sticky=W)

        tb.Button(frm, text="Finalizar Venta", bootstyle="success", command=self._finish_sale).grid(
            row=1, column=0, columnspan=2, sticky=EW, pady=8
        )

    def _add_to_cart(self):
        name = self.prod_combo.get()
        qty_str = self.qty_entry.get()
        if not name or not qty_str.isdigit():
            tb.Messagebox.show_error("Error", "Seleccione producto y cantidad válida")
            return
        qty = int(qty_str)
        pid = self.product_map[name]
        row = self.db.fetchone("SELECT precio, cantidad FROM productos WHERE id=?", (pid,))
        if qty > row["cantidad"]:
            tb.Messagebox.show_error("Error", "Stock insuficiente")
            return

        price = row["precio"]
        subtotal = qty * price
        self.cart.append({"id": pid, "name": name, "qty": qty, "price": price, "subtotal": subtotal})
        self.tree.insert("", "end", values=(name, qty, f"{price:.2f}", f"{subtotal:.2f}"))
        total = sum(item["subtotal"] for item in self.cart)
        self.total_var.set(f"{total:.2f}")
        self.qty_entry.clear()

    def _finish_sale(self):
        if not self.cart:
            tb.Messagebox.show_error("Error", "Carrito vacío")
            return

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total = float(self.total_var.get())
        # Por simplicidad: usuario_id = 1
        self.db.execute("INSERT INTO ventas (fecha, usuario_id, total) VALUES (?, ?, ?)",
                        (fecha, 1, total))
        vid = self.db.cursor.lastrowid

        for item in self.cart:
            self.db.execute(
                "INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, subtotal) VALUES (?, ?, ?, ?)",
                (vid, item["id"], item["qty"], item["subtotal"])
            )
            self.db.execute(
                "UPDATE productos SET cantidad = cantidad - ? WHERE id = ?",
                (item["qty"], item["id"])
            )

        tb.Messagebox.show_info("Éxito", f"Venta registrada (ID: {vid})")
        self.destroy()
