# 🧠 Sistema Experto para la Gestión de Proyectos con Scrum

Este proyecto es un sistema experto desarrollado en Python para asistir en la gestión de proyectos basados en la metodología **Scrum**. Utiliza un motor de inferencia y una base de datos relacional para brindar recomendaciones automatizadas y facilitar la toma de decisiones durante el ciclo de vida de los proyectos.

---

## 📋 Requisitos

- Python 3.8 o superior
- Git
- Entorno virtual con `venv`
- MariaDB (para la base de datos)

---

## ⚙️ Tecnologías utilizadas

- **Python**
- **Flask** – framework para la interfaz web
- **Experta** – motor de inferencia basado en reglas
- **SQLAlchemy** – ORM para la conexión con base de datos
- **MariaDB** – motor de base de datos relacional

---

## 🚀 Pasos para la instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/EliasO23/Sistema_Experto_SCRUM.git
```
```bash
cd Sistema_Experto_SCRUM
```

### 2. Crear y activar un entorno virtual

```bash
python -m venv venv
```
```bash
venv\Scripts\activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos

1. Crear una base de datos en MariaDB.
2. Configurar las credenciales de la base de datos en el archivo `app.py` colocando usuario y contraseña.

### 5. Ejecutar la aplicación

```bash
python main.py
```

### 6. Acceder a la aplicación

Abrir un navegador web y dirigirse a `http://127.0.0.1:5000`.

---

## 🔄 Reapertura del proyecto

Cada vez que se cierre o salga del proyecto, asegúrate de realizar los siguientes pasos para reactivarlo:

1. Activar el entorno virtual:

    ```bash
    venv\Scripts\activate
    ```

2. Ejecutar la aplicación:

    ```bash
    python main.py
    ```
