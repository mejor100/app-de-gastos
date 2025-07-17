# 💸 Aplicación de Registro de Gastos

Esta es una aplicación creada con **Streamlit** y **MySQL** que permite registrar, visualizar y filtrar gastos por fecha o categoría. La base de datos se gestiona localmente usando **XAMPP**.

[📽️ Ver video demo en Google Drive](https://drive.google.com/file/d/1ofrwXIfzZ8d3FB_crt7_ApReKV1UXRMF/view?usp=sharing)

---

Para trabajar con este proyecto localmente, seguí estos pasos para configurar la base de datos MySQL utilizando XAMPP y HeidiSQL:
✅ Requisitos previos

    XAMPP instalado y funcionando

    HeidiSQL (o cliente similar como DBeaver o MySQL Workbench)

🛠 Pasos

    -Iniciá MySQL desde el panel de control de XAMPP (botón "Start").

    -Abrí HeidiSQL y creá una nueva conexión:

        Hostname/IP: 127.0.0.1 o localhost

        Usuario: root

        Contraseña: (dejar en blanco, a menos que la hayas cambiado)

        Puerto: 3306 (por defecto)

    -Conectate al servidor.

    -Tenés dos opciones:

        Crear manualmente una base de datos llamada datos

        O simplemente importar el archivo .sql, que ya la crea y configura

    -Para importar:

        Clic derecho sobre el servidor > "Run SQL file..."

        Seleccioná el archivo datos.sql

        Ejecutá

Después de esto vas a tener dos tablas:

- "usuarios": para gestionar los usuarios registrados
- "gastos": para registrar los gastos asociados a cada usuario

