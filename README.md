# event_manager

Este proyecto es una aplicación web para gestionar eventos, tipos de entradas e inscripciones, desarrollada con **Django** y **Django REST Framework**.  
Permite a los usuarios registrarse, visualizar eventos, inscribirse, recibir un código QR, cancelar inscripciones, y a los administradores gestionar todo desde el panel.

---
# AVISO
AÚN NO TENGO HECHO EL FRONTEND Y NO SE PUEDE PROBAR COMO TAL EN WEB

# Requisitos

- Python 3.10 o superior
- pip
- Virtualenv 
- PostgreSQL o SQLite

---

# Instalación

1. **Clona el repositorio**

git clone https://github.com/adrian-estebanez/event_manager.git
cd event_manager

2. **Activa el entorno**
python -m venv env
source env/bin/activate

3. **Intala las dependencias**
   pip install -r requirements.txt

4. **Haz las migraciones**
   python manage.py makemigrations
   python manage.py migrate

5. **Crea un superusuario**
   python manage.py createsuperuser
   
6. **Inicia el server**
   python manage.py runserver
   
