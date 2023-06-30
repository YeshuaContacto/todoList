from tkinter import *
import sqlite3

root = Tk()
root.title("Todo list - YeshuaContacto")
root.geometry("+0+0")
root.configure(background="#404554")
root.iconbitmap(r"C:\Users\Lenovo\Desktop\todoList\juego.ico")
root.grid_rowconfigure(1, weight=1)  # Expandir la segunda fila verticalmente
root.grid_columnconfigure(0, weight=1)  # Expandir la primera columna horizontalmente



labelColor = "#f2f2f2"
rootColor = "#404554"


conn = sqlite3.connect("todo.db")

c = conn.cursor()

c.execute("""
    CREATE TABLE if not exists todo(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL
    );
""")

conn.commit()

def remove(id):
    def _remove():
        c.execute("DELETE FROM todo WHERE id = ?", (id, ))
        conn.commit()
        render_todos()

    return _remove

def complete(id):
    def _complete():
        todo = c.execute("SELECT * FROM todo WHERE id = ?", (id, )).fetchone()
        c.execute("UPDATE todo SET completed = ? WHERE id  = ?", (not todo[3], id))
        conn.commit()
        render_todos()

    return _complete

def render_todos():
    rows = c.execute("SELECT * FROM todo").fetchall()

    for widget in frame.winfo_children():
        widget.destroy()

    for i in range(0, len(rows)):
        id = rows[i][0]
        completed = rows[i][3]
        description = rows[i][2]
        todoColor = "#5d647a" if completed else "#f2f2f2" #color claro
        l = Checkbutton(frame, text=description, fg=todoColor, bg=rootColor, selectcolor=todoColor, width=42, anchor="w", command=complete(id), wraplength=200)
        l.grid(row=i, column=0, sticky="w", padx=5, pady=5)
        btn = Button(frame, text="Eliminar", bg="#9b2722", fg="#f2f2f2", command=remove(id))
        btn.grid(row=i, column=1, padx=5, pady=5)
        l.select() if completed else l.deselect()

def addTodo():
    todo = e.get()
    if todo:
        c.execute("""
                    INSERT INTO todo (description, completed) VALUES (?, ?)
                    """, (todo, False))
        conn.commit()
        e.delete(0, END)
        render_todos()
        e.focus()
    else:
        pass

def closeWindow(event):
    root.destroy()

container = Frame(root, bg=rootColor)
container.grid(row=0, column=0, padx=10, pady=10)
container.grid_columnconfigure(1, weight=1)


l = Label(container, text="Tarea", fg=labelColor, bg=rootColor)
l.grid(row=0, column=0)

e = Entry(container, bg=rootColor, fg="#f2f2f2")
e.grid(row=0, column=1, padx=5)
e.bind("<Return>", lambda event: addTodo())

btn = Button(container, text="Agregar", bg="#2bbf72", fg="#f2f2f2", command=addTodo)
btn.grid(row=0, column=2)
btn.bind("<Return>", lambda event: addTodo())

frame = LabelFrame(root, text="Mis tareas", fg=labelColor, bg=rootColor)
frame.grid(row=1, column=0, columnspan=3, sticky="nswe", padx=5)
frame.configure(background="#404554")


e.focus()

root.bind("<Return>", lambda x: addTodo)
root.bind("<KeyPress-Escape>", closeWindow)

render_todos()

root.mainloop()