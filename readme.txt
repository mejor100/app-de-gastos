# 💸 Aplicación de Registro de Gastos

Esta es una aplicación creada con **Streamlit** y **MySQL** que permite registrar, visualizar y filtrar gastos por fecha o categoría. La base de datos se gestiona localmente usando **XAMPP**.

[📽️ Ver video demo en Google Drive](https://drive.google.com/drive/folders/1bl9mjytAVUgjcE1H9l8lg9ZOaSy8C5Fk)

---

## 🗃️ Configuración de la Base de Datos (usando XAMPP)

1. Asegurate de tener [XAMPP](https://www.apachefriends.org/index.html) instalado y que el servicio de **MySQL** esté corriendo.
2. Abrí **phpMyAdmin** desde "http://localhost/phpmyadmin".
3. Creá una base de datos nueva llamada "datos" (o dejá que el archivo SQL lo haga por vos).
4. Importá el archivo SQL:
   - Entrá a la pestaña **Importar**
   - Seleccioná el archivo "datos.sql" (o donde lo hayas puesto)
   - Hacé clic en **Continuar**

Después de esto vas a tener dos tablas:

- "usuarios": para gestionar los usuarios registrados
- "gastos": para registrar los gastos asociados a cada usuario

