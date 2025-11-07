# EFI Blog Flask

### E.F.I. – Programación Python I  
**Proyecto:** API REST – Flask JWT Roles  
**Integrantes:** Benjamín De Lauro – Esteban Rodríguez  
**Instituto:** ITEC Río Cuarto  
**Carrera:** Técnico Superior en Desarrollo de Software  
**Año:** 2025  

---

## Introducción
El presente trabajo tiene como objetivo desarrollar una **API REST segura** implementada con **Flask** que gestione publicaciones, categorías, comentarios y usuarios, incorporando autenticación mediante **JSON Web Tokens (JWT)** y control de acceso basado en roles.

---

## Objetivo
Aplicar los conceptos de:
- Autenticación y autorización
- Seguridad en APIs
- Arquitectura por capas (service–repository)
- Buenas prácticas de desarrollo con Flask y SQLAlchemy

---

## Arquitectura
El proyecto sigue una estructura modular:
- `/models`: Definición de entidades (User, Post, Comment, Category)  
- `/views`: Controladores basados en clases (MethodView)  
- `/decorators`: Decoradores personalizados para control de roles  
- `/seed_data.py`: Carga de datos iniciales  
- `app.py`: Configuración principal y registro de rutas  

---

## Tecnologías
- **Flask**  
- **Flask-JWT-Extended**  
- **Flask-CORS**  
- **SQLite**  
- **Werkzeug.security**  

---

## Instrucciones de instalación
1. Crear entorno virtual  
   ```bash
   python -m venv venv
   source venv/bin/activate  # en Windows: venv\Scripts\activate
