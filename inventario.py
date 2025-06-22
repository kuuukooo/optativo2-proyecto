# inventario.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from manager import DBManager

class InventarioApp(tb.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Inventario")
        self.geometry("800x500")
        self.db = DBManager()
        self.selected_id = None  # Para rastrear el ID del producto seleccionado
        
        cols = ("ID","Nombre","Descripción","Categoría","Precio","Cantidad","Proveedor")
        self.tree = tb.Treeview(self, columns=cols, show="headings", bootstyle="dark")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=100, anchor=CENTER)
        
        # Bind para selección de elementos
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        
        self.tree.pack(fill=BOTH, expand=True, pady=10, padx=10)
        self._load_data()
        self._build_form()
    
    def _load_data(self):
        for row in self.db.fetchall("SELECT * FROM productos"):
            vals = (
                row["id"], row["nombre"], row["descripcion"],
                row["categoria"], row["precio"], row["cantidad"], row["proveedor_id"]
            )
            self.tree.insert("", "end", values=vals)
    
    def _build_form(self):
        frm = tb.Frame(self, padding=10)
        frm.pack(fill=X)
        
        labels = ["Nombre","Descripción","Categoría","Precio","Cantidad","Proveedor ID"]
        self.entries = {}
        
        for i, lbl in enumerate(labels):
            tb.Label(frm, text=lbl).grid(row=i, column=0, sticky=E, padx=5, pady=4)
            ent = tb.Entry(frm, bootstyle="dark")
            ent.grid(row=i, column=1, padx=5, pady=4, sticky=EW)
            self.entries[lbl.lower().replace(" ", "_")] = ent  # Normalizar nombres de keys
        
        frm.columnconfigure(1, weight=1)
        
        # Botones
        btn_frame = tb.Frame(frm)
        btn_frame.grid(row=len(labels), column=0, columnspan=2, pady=10, sticky=EW)
        
        tb.Button(btn_frame, text="Guardar", bootstyle="success", command=self._save).pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="Nuevo", bootstyle="info", command=self._clear_form).pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="Eliminar", bootstyle="danger", command=self._delete).pack(side=LEFT, padx=5)
    
    def _on_select(self, event):
        """Manejar selección de elemento en el treeview"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            # Guardar el ID seleccionado
            self.selected_id = values[0]
            
            # Llenar el formulario con los datos seleccionados
            self.entries["nombre"].delete(0, END)
            self.entries["nombre"].insert(0, values[1])
            
            self.entries["descripción"].delete(0, END)
            self.entries["descripción"].insert(0, values[2])
            
            self.entries["categoría"].delete(0, END)
            self.entries["categoría"].insert(0, values[3])
            
            self.entries["precio"].delete(0, END)
            self.entries["precio"].insert(0, values[4])
            
            self.entries["cantidad"].delete(0, END)
            self.entries["cantidad"].insert(0, values[5])
            
            self.entries["proveedor_id"].delete(0, END)
            self.entries["proveedor_id"].insert(0, values[6] if values[6] else "")
    
    def _clear_form(self):
        """Limpiar formulario para nuevo producto"""
        self.selected_id = None
        for entry in self.entries.values():
            entry.delete(0, END)
        # Deseleccionar en el treeview
        self.tree.selection_remove(self.tree.selection())
    
    def _save(self):
        try:
            # Obtener valores del formulario
            v = {k: e.get().strip() for k, e in self.entries.items()}
            
            # Validaciones básicas
            if not v["nombre"] or not v["precio"] or not v["cantidad"]:
                Messagebox.show_error("Error", "Los campos Nombre, Precio y Cantidad son obligatorios")
                return
            
            # Convertir tipos de datos
            try:
                precio = float(v["precio"])
                cantidad = int(v["cantidad"])
                proveedor_id = int(v["proveedor_id"]) if v["proveedor_id"] else None
            except ValueError:
                Messagebox.show_error("Error", "Precio debe ser un número decimal y Cantidad debe ser un número entero")
                return
            
            params = (
                v["nombre"], v["descripción"], v["categoría"],
                precio, cantidad, proveedor_id
            )
            
            # Ejecutar operación de base de datos
            if self.selected_id:  # Actualizar producto existente
                self.db.execute(
                    "UPDATE productos SET nombre=?,descripcion=?,categoria=?,precio=?,cantidad=?,proveedor_id=? WHERE id=?",
                    (*params, self.selected_id)
                )
                print("Producto actualizado correctamente")  # Debug temporal
            else:  # Insertar nuevo producto
                self.db.execute(
                    "INSERT INTO productos (nombre,descripcion,categoria,precio,cantidad,proveedor_id) VALUES (?,?,?,?,?,?)",
                    params
                )
                print("Producto agregado correctamente")  # Debug temporal
            
            # Recargar datos y limpiar formulario
            self._refresh_data()
            self._clear_form()
            
            # Mostrar mensaje de éxito al final
            if self.selected_id:
                Messagebox.show_info("Éxito", "Producto actualizado correctamente")
            else:
                Messagebox.show_info("Éxito", "Producto agregado correctamente")
            
        except Exception as e:
            print(f"Error completo en _save: {e}")  # Debug
            Messagebox.show_error("Error", f"Error al guardar producto: {str(e)}")
    
    def _delete(self):
        """Eliminar producto seleccionado"""
        try:
            if not self.selected_id:
                Messagebox.show_warning("Advertencia", "Selecciona un producto para eliminar")
                return
            
            # Confirmar eliminación
            result = Messagebox.show_question("Confirmar", "¿Estás seguro de eliminar este producto?")
            if result == "Yes":
                self.db.execute("DELETE FROM productos WHERE id=?", (self.selected_id,))
                print("Producto eliminado correctamente")  # Debug
                self._refresh_data()
                self._clear_form()
                Messagebox.show_info("Éxito", "Producto eliminado correctamente")
                
        except Exception as e:
            print(f"Error en _delete: {e}")  # Debug
            Messagebox.show_error("Error", f"Error al eliminar producto: {str(e)}")
    
    def _refresh_data(self):
        """Actualizar datos del treeview"""
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Recargar datos
        self._load_data()