import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import bcrypt
import sys

def encriptar_contraseña(contraseña):
    return bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())


credenciales_validas = {
    'Sistemas1': encriptar_contraseña('jjlex2024'),
    'Sistemas2': encriptar_contraseña('jjlex2025')
}


def solicitar_credenciales_para_info(callback):
    def verificar_credenciales(event=None):  
        username = entrada_usuario_popup.get()
        password = entrada_password_popup.get()
        if username in credenciales_validas and bcrypt.checkpw(password.encode('utf-8'), credenciales_validas[username]):
            popup.destroy()
            callback()
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")

   
    popup = tk.Toplevel(root)
    popup.title("Credenciales requeridas")
    popup.geometry("300x200")
    popup.resizable(False, False)
    popup.iconbitmap(icon_path)

    tk.Label(popup, text="Usuario:").pack(pady=5)
    entrada_usuario_popup = tk.Entry(popup, width=30)
    entrada_usuario_popup.pack(pady=5)

    tk.Label(popup, text="Contraseña:").pack(pady=5)
    entrada_password_popup = tk.Entry(popup, show="*", width=30)
    entrada_password_popup.pack(pady=5)

    tk.Button(popup, text="Verificar", command=verificar_credenciales).pack(pady=10)

    popup.bind('<Return>', verificar_credenciales)
    popup.transient(root)
    popup.grab_set()
    root.wait_window(popup)


def mostrar_registro():
    print("Acceso autorizado a la pestaña de Registro.")    
    mostrar_datos_usuarios() 

root = tk.Tk()
root.title("Directorio Lexcom")
root.geometry("900x600")

icon_path = r"C:\Users\Soporte 2\Documents\Phyton\Directorio_lex\Logo.ico"
root.iconbitmap(icon_path)

label_titulo = tk.Label(root, text="Directorio Lexcom", font=("Arial", 20))
label_titulo.place(x=5, y=5)

nb = ttk.Notebook(root)
nb.place(x=10, y=50, width=880, height=540)

pl = ttk.Frame(nb)
nb.add(pl, text='Directorio')

p2 = ttk.Frame(nb)
nb.add(p2, text='Registro')


label_nombre = tk.Label(pl, text="Cartera", font=("Arial", 16))
label_nombre.place(x=50, y=50)

carteras_disponibles = ["VANA", "BAM ", "GYT", "PROAMERICA", "BAC", "BAM ADMIN", "BI", "EMBARGOS", "ADMINISTACION"]
combobox_nivel = ttk.Combobox(pl, values=carteras_disponibles, state="readonly", width=45)
combobox_nivel.place(x=150, y=50) 


def manejar_cambio_pestana(event):
    if nb.index("current") == 0:   
        mostrar_datos_usuarios() 

nb.bind("<<NotebookTabChanged>>", manejar_cambio_pestana)  

def mostrar_datos_usuarios():
    try:
       
        print("Conectando a la base de datos...")
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="Usuario",
            port=3306 
        )
        print("Conexión exitosa a la base de datos.")

        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios;")
        resultados = cursor.fetchall()

        if not resultados:
            print("No hay datos en la base de datos.")
        else:
            print("Datos encontrados: ", resultados) 

        tree = ttk.Treeview(pl, columns=("codigo", "area", "puesto", "nombre", "extencion"), show="headings")
        tree.place(x=50, y=100, width=800, height=300)  

     
        tree.heading("codigo", text="Código")
        tree.heading("area", text="Área")
        tree.heading("puesto", text="Puesto")
        tree.heading("nombre", text="Nombre")
        tree.heading("extencion", text="Extensión")

        for fila in resultados:
            tree.insert("", "end", values=fila)

    except mysql.connector.Error as err:
        print(f"Error al conectar o al consultar la base de datos: {err}")
        messagebox.showerror("Error en la conexión", f"Error al conectar a la base de datos: {err}")
    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")
        messagebox.showerror("Error inesperado", f"Ha ocurrido un error inesperado: {e}")
    finally:
        try:
            cursor.close()
            conexion.close()
        except:
            pass


def on_closing():
    print("Cerrando la aplicación.")
    root.quit()


root.protocol("WM_DELETE_WINDOW", on_closing)


try:
    root.mainloop()
except Exception as e:
    print(f"Error al iniciar la interfaz gráfica: {e}")
    messagebox.showerror("Error en la interfaz gráfica", f"Error al iniciar la interfaz gráfica: {e}")
