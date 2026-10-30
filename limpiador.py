"""Limpiador de carpetas duplicadas.

Busca archivos comprimidos (zip, rar, 7z...) y carpetas con el mismo nombre
en el mismo directorio. Muestra las carpetas a eliminar, pide confirmación y
las elimina todas de golpe.
"""
import os
import shutil
import threading
from dataclasses import dataclass

EXTENSIONES = (".tar.gz", ".tar.bz2", ".tar.xz", ".tgz", ".zip", ".rar",
               ".7z", ".tar", ".gz", ".bz2", ".xz")


@dataclass
class Duplicado:
    carpeta: str
    archivo: str


def nombre_base(nombre):
    """Devuelve el nombre sin extensión de compresión, o None si no es un comprimido."""
    bajo = nombre.lower()
    for ext in EXTENSIONES:
        if bajo.endswith(ext) and len(nombre) > len(ext):
            return nombre[: -len(ext)]
    return None


def buscar_duplicados(raiz, recursivo=True, progreso=None):
    """Encuentra carpetas cuyo nombre coincide con un comprimido en el mismo directorio."""
    resultado = []
    for ruta, carpetas, archivos in os.walk(raiz):
        if progreso:
            progreso(ruta)
        carpetas_por_nombre = {c.lower(): c for c in carpetas}
        for archivo in archivos:
            base = nombre_base(archivo)
            if base and base.lower() in carpetas_por_nombre:
                carpeta = carpetas_por_nombre[base.lower()]
                resultado.append(Duplicado(os.path.join(ruta, carpeta),
                                           os.path.join(ruta, archivo)))
        if not recursivo:
            break
    # Evita duplicados (p. ej. x.zip y x.rar apuntan a la misma carpeta)
    vistos, unicos = set(), []
    for d in resultado:
        clave = os.path.normcase(d.carpeta)
        if clave not in vistos:
            vistos.add(clave)
            unicos.append(d)
    return sorted(unicos, key=lambda d: d.carpeta.lower())


def eliminar(duplicados, papelera=True):
    """Elimina las carpetas. Devuelve (eliminadas, errores)."""
    enviar = None
    if papelera:
        try:
            from send2trash import send2trash as enviar
        except ImportError:
            enviar = None
    eliminadas, errores = 0, []
    for d in duplicados:
        try:
            if enviar:
                enviar(os.path.normpath(d.carpeta))
            else:
                shutil.rmtree(d.carpeta)
            eliminadas += 1
        except Exception as e:  # noqa: BLE001
            errores.append((d.carpeta, str(e)))
    return eliminadas, errores


def main():
    import customtkinter as ctk
    from tkinter import filedialog, messagebox

    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    class App(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("Limpiador de carpetas duplicadas")
            self.geometry("860x620")
            self.minsize(700, 500)
            self.duplicados = []
            self.checks = []

            ctk.CTkLabel(self, text="Limpiador de carpetas duplicadas",
                         font=ctk.CTkFont(size=24, weight="bold")
                         ).pack(anchor="w", padx=24, pady=(20, 0))
            ctk.CTkLabel(self, text="Elimina las carpetas que ya existen comprimidas "
                         "(ej. fichero.zip + carpeta fichero).",
                         text_color=("gray35", "gray65")
                         ).pack(anchor="w", padx=24, pady=(0, 12))

            fila = ctk.CTkFrame(self, corner_radius=12)
            fila.pack(fill="x", padx=24)
            self.ruta = ctk.CTkEntry(fila, placeholder_text="Selecciona una carpeta…",
                                     height=36)
            self.ruta.pack(side="left", fill="x", expand=True, padx=(12, 8), pady=12)
            ctk.CTkButton(fila, text="Examinar", width=100, height=36,
                          command=self.examinar).pack(side="left", padx=(0, 8))
            self.btn_buscar = ctk.CTkButton(fila, text="Buscar", width=100, height=36,
                                            command=self.buscar)
            self.btn_buscar.pack(side="left", padx=(0, 12))

            opc = ctk.CTkFrame(self, fg_color="transparent")
            opc.pack(fill="x", padx=24, pady=8)
            self.recursivo = ctk.CTkSwitch(opc, text="Incluir subcarpetas")
            self.recursivo.select()
            self.recursivo.pack(side="left")
            self.papelera = ctk.CTkSwitch(opc, text="Enviar a la papelera")
            self.papelera.select()
            self.papelera.pack(side="left", padx=24)

            self.lista = ctk.CTkScrollableFrame(self, corner_radius=12)
            self.lista.pack(fill="both", expand=True, padx=24, pady=(0, 8))

            pie = ctk.CTkFrame(self, fg_color="transparent")
            pie.pack(fill="x", padx=24, pady=(0, 16))
            self.estado = ctk.CTkLabel(pie, text="Listo.", anchor="w")
            self.estado.pack(side="left", fill="x", expand=True)
            self.btn_eliminar = ctk.CTkButton(
                pie, text="Eliminar seleccionadas", height=38, state="disabled",
                fg_color="#d13438", hover_color="#a4262c", command=self.confirmar)
            self.btn_eliminar.pack(side="right")

        def examinar(self):
            d = filedialog.askdirectory()
            if d:
                self.ruta.delete(0, "end")
                self.ruta.insert(0, os.path.normpath(d))

        def buscar(self):
            raiz = self.ruta.get().strip()
            if not os.path.isdir(raiz):
                messagebox.showwarning("Carpeta no válida", "Selecciona una carpeta existente.")
                return
            self.btn_buscar.configure(state="disabled")
            self.btn_eliminar.configure(state="disabled")
            self.estado.configure(text="Buscando…")
            rec = bool(self.recursivo.get())

            def tarea():
                res = buscar_duplicados(
                    raiz, rec,
                    lambda p: self.after(0, lambda: self.estado.configure(text=f"Buscando: {p}")))
                self.after(0, lambda: self.mostrar(res))

            threading.Thread(target=tarea, daemon=True).start()

        def mostrar(self, res):
            for w in self.lista.winfo_children():
                w.destroy()
            self.duplicados, self.checks = res, []
            for d in res:
                var = ctk.BooleanVar(value=True)
                self.checks.append(var)
                f = ctk.CTkFrame(self.lista, fg_color="transparent")
                f.pack(fill="x", pady=2)
                ctk.CTkCheckBox(f, text="", variable=var, width=24,
                                command=self.actualizar_boton).pack(side="left")
                txt = ctk.CTkFrame(f, fg_color="transparent")
                txt.pack(side="left", fill="x", expand=True)
                ctk.CTkLabel(txt, text="📁 " + d.carpeta, anchor="w").pack(fill="x")
                ctk.CTkLabel(txt, text="   ↳ " + os.path.basename(d.archivo), anchor="w",
                             text_color=("gray35", "gray65"),
                             font=ctk.CTkFont(size=11)).pack(fill="x")
            self.btn_buscar.configure(state="normal")
            self.estado.configure(
                text=f"{len(res)} carpeta(s) duplicada(s) encontrada(s)." if res
                else "No se encontraron carpetas duplicadas.")
            self.actualizar_boton()

        def seleccionadas(self):
            return [d for d, v in zip(self.duplicados, self.checks) if v.get()]

        def actualizar_boton(self):
            n = len(self.seleccionadas())
            self.btn_eliminar.configure(
                state="normal" if n else "disabled",
                text=f"Eliminar seleccionadas ({n})" if n else "Eliminar seleccionadas")

        def confirmar(self):
            sel = self.seleccionadas()
            if not sel:
                return
            ventana = ctk.CTkToplevel(self)
            ventana.title("Confirmar eliminación")
            ventana.geometry("700x460")
            ventana.transient(self)
            ventana.after(100, ventana.grab_set)
            ctk.CTkLabel(ventana, font=ctk.CTkFont(size=16, weight="bold"),
                         text=f"Se eliminarán {len(sel)} carpeta(s):"
                         ).pack(anchor="w", padx=20, pady=(16, 8))
            caja = ctk.CTkTextbox(ventana)
            caja.pack(fill="both", expand=True, padx=20)
            caja.insert("1.0", "\n".join(d.carpeta for d in sel))
            caja.configure(state="disabled")
            botones = ctk.CTkFrame(ventana, fg_color="transparent")
            botones.pack(fill="x", padx=20, pady=16)

            def aceptar():
                ventana.destroy()
                ok, errs = eliminar(sel, bool(self.papelera.get()))
                msg = f"Se eliminaron {ok} carpeta(s)."
                if errs:
                    msg += f"\n\n{len(errs)} error(es):\n" + "\n".join(
                        f"{c}: {e}" for c, e in errs[:10])
                messagebox.showinfo("Resultado", msg)
                self.buscar()

            ctk.CTkButton(botones, text="Eliminar todas", fg_color="#d13438",
                          hover_color="#a4262c", command=aceptar).pack(side="right")
            ctk.CTkButton(botones, text="Cancelar", fg_color="gray40",
                          hover_color="gray30", command=ventana.destroy
                          ).pack(side="right", padx=8)

    App().mainloop()


if __name__ == "__main__":
    main()
