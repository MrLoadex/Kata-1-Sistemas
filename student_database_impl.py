import sqlite3

def connect_db():
    conn=sqlite3.connect("students.db")
    try:
        conn.execute("""create table students (
                                student_id integer primary key autoincrement,
                                name text,
                                DNI integer,
                                career text
                            )""")
        print("se creo la tabla students")                        
    except sqlite3.OperationalError:
        print("La tabla students ya existe")                    
    conn.close()



def add_student(name, DNI, career):
    name = name.capitalize()
    conn = sqlite3.connect("students.db")
    conn.execute("""
        INSERT INTO students (name, DNI, career)
        VALUES (:name, :dni, :career)
    """, {'name': name, 'dni': DNI, 'career': career})
    conn.commit()
    conn.close()

#devuelve una lista de estudiantes
def show_students():
    students = []
    conn=sqlite3.connect("students.db")
    cursor=conn.execute("select student_id, name, DNI, career from students")
     
    for fila in cursor:
        students.append(fila)
    conn.close()
    return students

#devuelve los datos del estudiante seleccionado 0=name, 1=dni, 2=career
def get_student(student_id):
    conn=sqlite3.connect("students.db")
    cursor=conn.execute("SELECT name, DNI, career from students where student_id=?", (student_id, ))
    
    fila=cursor.fetchone()
    conn.close()   
    
    if fila!=None:
        return(fila)
    else:
        print("ERROR: El estudiante no existe")
        return 0
    
def del_student(student_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    # Eliminar el alumno de la tabla
    cursor.execute("""
        DELETE FROM students
        WHERE student_id = ?
    """, (student_id,))
    conn.commit()
    conn.close()  


#necesita si o si la id
def update_student(name = 0, DNI = 0, career = 0, student_id = 0):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    #copia en memoria los datos de la base de datos
    student_data = get_student(student_id)
    #Si la id era invalida finaliza (el error lo mostrara get_student)
    if student_data == 0:
        return 0
    
    #Reemplaza los valores no modificados por los valores viejos
    name = student_data[0] if name == 0 or name =="" else name.capitalize()
    DNI = student_data[1] if DNI == 0 or DNI=="" else DNI
    career = student_data[2] if career == 0 or career=="" else career 
    
    # Actualizar los datos del estudiante en la tabla
    cursor.execute("""
        UPDATE students
        SET name = ?, DNI = ?, career = ?
        WHERE student_id = ?
    """, (name, DNI, career, student_id))

    conn.commit()
    conn.close()    

#Si se ejecuta el modulo solo
if __name__ == "__main__":
    connect_db()
    print(show_students())