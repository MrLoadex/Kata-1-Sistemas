import sqlite3

def connect_db():
    conn=sqlite3.connect("users.db")
    try:
        conn.execute("""create table users (
                                user_id integer primary key autoincrement,
                                useruserName text,
                                password text
                            )""")
        print("se creo la tabla users")                        
    except sqlite3.OperationalError:
        print("La tabla users ya existe")                    
    conn.close()



def add_user(userName, password):
    userName = userName
    conn = sqlite3.connect("users.db")
    conn.execute("""
        INSERT INTO users (userName, password)
        VALUES (:userName, :password)
    """, {'userName': userName, 'password': password})
    conn.commit()
    conn.close()

#devuelve una lista de users
def show_users():
    users = []
    conn=sqlite3.connect("users.db")
    cursor=conn.execute("select user_id, userName, password from users")
    
    for fila in cursor:
        users.append(fila)
    conn.close()
    return users

#devuelve los datos del user seleccionado 0=userName, 1=, 2=password
def get_user(userName, password):
    conn=sqlite3.connect("users.db")
    cursor = conn.execute("SELECT userName, password FROM users WHERE userName = ? AND password = ?", (userName, password))
    
    fila=cursor.fetchone()
    conn.close()   
    
    if fila!=None:
        return(fila)
    else:
        print("ERROR: El user no existe")
        return 0
    
def del_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Eliminar el alumno de la tabla
    cursor.execute("""
        DELETE FROM users
        WHERE user_id = ?
    """, (user_id,))
    conn.commit()
    conn.close()  


#necesita si o si la id
def update_user(userName = 0, password = 0, user_id = 0):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    #copia en memoria los datos de la base de datos
    user_data = get_user(user_id)
    #Si la id era invalida finaliza (el error lo mostrara get_user)
    if user_data == 0:
        return 0
    
    #Reemplaza los valores no modificados por los valores viejos
    userName = user_data[0] if userName == 0 or userName =="" else userName.capitalize()
    password = user_data[2] if password == 0 or password=="" else password 
    
    # Actualizar los datos del user en la tabla
    cursor.execute("""
        UPDATE users
        SET userName = ?, password = ?
        WHERE user_id = ?
    """, (userName, password, user_id))

    conn.commit()
    conn.close()    

#Si se ejecuta el modulo solo
if __name__ == "__main__":
    connect_db()
    #add_user("admin","admin")
    print(show_users())
    print(get_user("admin","admin"))