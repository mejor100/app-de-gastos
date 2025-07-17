import streamlit as st 
import mysql.connector
import datetime
import hashlib

def hashear_contraseña(contraseña):
    return hashlib.sha256(contraseña.encode()).hexdigest()


def conectar_db():
        db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database= "datos"
    )
        return db

def pagInicio():
    col1, col2 = st.columns([2, 9])
    with col1:
        if st.button("Iniciar sesión"):
            st.session_state['pagina'] = 'login'
            return st.session_state['pagina']
    with col2:    
        if st.button("Registrarse"):
            st.session_state['pagina'] = 'registro'
            return st.session_state['pagina']
    with st.container():
        st.title("Seguidor de Gastos")
        st.markdown("""
        ¡Hola! 👋  
        Esta aplicación te ayudará a **registrar**, **organizar** y **visualizar tus gastos diarios** para que tengas un mejor control de tus finanzas personales.

        ### ¿Qué podés hacer?
        - Agregar tus gastos con fecha, monto y categoría
        - Filtrar y revisar gastos por mes o categoría

        > Empezá registrandote o iniciando sesion.  
        ¡Tus finanzas están a punto de mejorar! 📊
        """)

def pagRegistro():
    with st.container():
        if st.button("Inicio"):
            st.session_state['pagina'] = 'inicio'
            st.rerun()
        st.title("Registro")
        email = st.text_input("Email")
        nombreUsuario = st.text_input("Nombre de usuario")
        contraseña = st.text_input("Contraseña", type="password")
        if st.button("aceptar"):
            if not email or not nombreUsuario or not contraseña:
                st.warning("Por favor, completá todos los campos.")
            elif "@" not in email:
                st.error("El email no parece válido.")
            else:
                    # Conexión a la base de datos
                    conn = conectar_db()
                    cursor = conn.cursor()

                    # Verificar si ya existe ese nombre de usuario
                    cursor.execute("SELECT * FROM usuarios WHERE nombreUsuario = %s", (nombreUsuario,))
                    usuarioExistente = cursor.fetchone()
                    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
                    emailExistente = cursor.fetchone()

                    if usuarioExistente:
                        st.warning("El nombre de usuario ya existe. Elegí otro.")
                    elif emailExistente:
                        st.warning("Ese email ya esta siendo usado.")
                    else:
                        # Insertar usuario
                        contraseña_hash = hashear_contraseña(contraseña)
                        cursor.execute("INSERT INTO usuarios (email, nombreUsuario, contraseña) VALUES (%s, %s, %s)",
                            (email, nombreUsuario, contraseña_hash))
                        conn.commit()
                        st.success("Usuario registrado con éxito ✅")
                        st.session_state['pagina'] = 'inicio'
                        st.rerun()

               

                
                    cursor.close()
                    conn.close()   


def pagLogin():
    with st.container():
        if st.button("Inicio"):
            st.session_state['pagina'] = 'inicio'
            st.rerun()
        st.title("Inicio de sesion")
        nombreUsuario = st.text_input("Nombre de usuario")
        contraseña = st.text_input("Contraseña", type="password")
        if st.button("aceptar"):
            if not nombreUsuario or not contraseña:
                st.warning("Por favor, completá todos los campos.")
            else:
                    # Conexión a la base de datos
                    conn = conectar_db()
                    cursor = conn.cursor()
                    contraseña_hash = hashear_contraseña(contraseña)
                    cursor.execute("SELECT * FROM usuarios WHERE nombreUsuario = %s AND contraseña = %s",
                                   (nombreUsuario, contraseña_hash))
                    resultado = cursor.fetchone()

                    if resultado:
                        st.success("Inicio de sesión exitoso ✅")
                        st.session_state['pagina'] = "Sesion iniciada"
                        #guardo la id del usuario asi la puedo referenciar en la base de datos
                        cursor.execute("SELECT id_usuario FROM usuarios where nombreUsuario = %s",
                                       (nombreUsuario,))
                        resultadoId = cursor.fetchone()
                        st.session_state['id'] = resultadoId[0] #resultadoId[0] en vez de resultadoId porque cursor.fetchone() devuelve una tupla

                        st.rerun()
                    else:
                        st.error("Usuario o contraseña incorrectos")
                    
                    cursor.close()
                    conn.close()

def sesionIniciada():
    conn = conectar_db()
    cursor = conn.cursor()
    with st.container():
        if st.button("Cerrar Sesion"):
            st.session_state['pagina'] = 'inicio'
            st.session_state['id'] = ""
            st.rerun()
    pestañas = st.tabs(["Agregar gastos", "Tabla Entera", "Tabla con filtros"])
    with pestañas[0]:
            st.title("Agregue sus gastos")
            monto = st.number_input("Gasto")
            opciones = ["Alimentos", "Transporte", "Entretenimiento", "Salud"]
            categoria = st.selectbox("Seleccioná una categoría:", opciones)
            fecha = st.date_input("Fecha")
            #conecto a base de datos
            try: 
                if st.button("Aceptar"):
                    if not monto or not categoria or not fecha:
                        st.warning("Por favor, ingrese todos los datos")
                    else:
                        cursor.execute("INSERT INTO gastos(fecha, monto, categoria, usuario_id) VALUES (%s, %s, %s, %s)",
                                    (fecha, monto, categoria, st.session_state['id']))
                        conn.commit()
                        st.success("Sus datos han sido ingresados exitosamente")

                        
                                
            except:
                st.error(f"Error en la base de datos")



    with pestañas[1]: 
            st.title("Todos los gastos")
            cursor.execute("SELECT id_gastos, fecha, monto, categoria from gastos WHERE usuario_id = %s",
                        (st.session_state['id'],))
            resultados = cursor.fetchall()
            tabla = [] #lista
            for i in resultados:
                tabla.append({"id": i[0], "Fecha": str(i[1]), "Monto": float(i[2]), "Categoria": str(i[3])})
            st.dataframe(tabla)
            
            #total de los gastos
            cursor.execute("SELECT SUM(monto) from gastos where usuario_id = %s",
                        (st.session_state['id'],)) 
            totalGastos = cursor.fetchall()
            for i in totalGastos:
                if i[0] is not None:
                    st.write(f"Total de los gastos: ${float(i[0])}")
                else:
                    None

            filaSeleccionada = st.selectbox("Elija qué fila quiere borrar", (tabla))
            if st.button("Borrar"):
                cursor.execute("DELETE FROM gastos WHERE id_gastos = %s", (filaSeleccionada["id"],))
                conn.commit()
                st.success("Se ha borrado lo que seleccionó.")
                st.rerun()

    with pestañas[2]:
            st.title("Filtre su busqueda")
            filtroAño = st.selectbox("Seleccione su año", (2025, 2026, 2027, 2028, 2029, 2030))
            meses = {"Enero": 1,"Febrero": 2,"Marzo": 3,"Abril": 4,"Mayo": 5,"Junio": 6,"Julio": 7,"Agosto": 8,"Septiembre": 9,"Octubre": 10,"Noviembre": 11,"Diciembre": 12,}
            filtroMes = st.selectbox("Seleccione un Mes", (meses.keys()))
            opciones = ["Todo", "Alimentos", "Transporte", "Entretenimiento", "Salud"]
            filtroCategoria = st.selectbox("Seleccione una Categoria", (opciones))
            if filtroCategoria != "Todo":
                cursor.execute("SELECT fecha, monto, categoria FROM gastos WHERE YEAR(fecha) = %s AND MONTH(fecha) = %s AND categoria = %s AND usuario_id = %s",
                                        (filtroAño, meses[filtroMes], filtroCategoria, st.session_state['id']))
                resultados = cursor.fetchall()
                tabla = []
                for i in resultados:
                    tabla.append({"Fecha": str(i[0]), "Monto": float(i[1]), "Categoria": str(i[2])})
                st.dataframe(tabla)

                cursor.execute("SELECT SUM(monto) FROM gastos WHERE YEAR(fecha) = %s AND MONTH(fecha) = %s AND categoria = %s AND usuario_id = %s",
                                        (filtroAño, meses[filtroMes], filtroCategoria, st.session_state['id']))
                totalFiltroGastos = cursor.fetchone()
                if totalFiltroGastos[0] is not None:
                    for i in totalFiltroGastos:
                        st.write(f"Total de los gastos: ${float(i)}")
                else:
                    st.write("Total de los gastos: $0.00")
            else:
                cursor.execute("SELECT fecha, monto, categoria FROM gastos WHERE YEAR(fecha) = %s AND MONTH(fecha) = %s  AND usuario_id = %s",
                                        (filtroAño, meses[filtroMes], st.session_state['id']))
                resultados = cursor.fetchall()
                tabla = []
                for i in resultados:
                    tabla.append({"Fecha": str(i[0]), "Monto": float(i[1]), "Categoria": str(i[2])})
                st.dataframe(tabla)
                cursor.execute("SELECT SUM(monto) FROM gastos WHERE YEAR(fecha) = %s AND MONTH(fecha) = %s  AND usuario_id = %s",
                                        (filtroAño, meses[filtroMes], st.session_state['id']))
                totalFiltroGastos = cursor.fetchone()
                if totalFiltroGastos[0] is not None:
                    for i in totalFiltroGastos:
                        st.write(f"Total de los gastos: ${float(i)}")
                else:
                    st.write("Total de los gastos: $0.00")


            
    cursor.close()
    conn.close()



