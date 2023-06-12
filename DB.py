import tkinter as tk
import sqlite3

def connect_db():
    connection=sqlite3.connect("students.db")
    try:
        connection.execute("""create table students (
                                id integer primary key autoincrement,
                                name text,
                                DNI integer,
                                career text
                            )""")
        print("se creo la tabla students")                        
    except sqlite3.OperationalError:
        print("La tabla students ya existe")                    
    connection.close()

def add_student(name, DNI, career):
    connection = sqlite3.connect("students.db")
    connection.execute("""
        INSERT INTO students (name, DNI, career)
        VALUES (?, ?, ?)
    """, (name, DNI, career))
    connection.commit()
    connection.close()

def select_students():
    connection=sqlite3.connect("students.db")
    cursor=connection.execute("select id, name, DNI, career from students")
    for fila in cursor:
        print(fila)
    connection.close()

def select_student(id):
    connection=sqlite3.connect("students.db")
    cursor=connection.execute("select name, DNI, career from students where id=?", (id, ))
    fila=cursor.fetchone()
    if fila!=None:
        print(fila)
    else:
        print("NO ESTAAAAAA!!!!!!!!!!.")
    connection.close()   


#connect_db()
#add_student("juaisdhfkjdhn",3932834534845,"sisdfgdfgtemas")
select_student(50)