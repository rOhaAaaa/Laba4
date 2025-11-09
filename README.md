# ☁️ Laba 4–5: Хмарне розгортання Flask API

## 📘 Опис
У межах лабораторної роботи створено та розгорнуто **Flask REST API** на хмарній платформі **AWS EC2**.  
Сервіс реалізує роботу з базою даних компанії (співробітники, обладнання, відділи, офіси тощо)  
і використовує **JWT-авторизацію**, **Swagger-документацію** та **CI/CD** через GitHub Actions.

## 🚀 Реалізовано
1. Розгорнуто Flask API на **AWS EC2**.  
2. Підключено **MySQL (AWS RDS)** для зберігання даних.  
3. Налаштовано **Swagger UI** для перегляду REST-endpoints.  
4. Реалізовано **автоматичний деплой** через GitHub (CI/CD).  
5. Додано **JWT-токен авторизацію** для безпечного доступу.

## 🧰 Використані технології
- Python 3.12 / Flask / Flask-RESTx  
- SQLAlchemy ORM  
- AWS EC2 + RDS  
- Swagger (OpenAPI)  
- GitHub Actions (CI/CD)  

## 🔗 Основні endpoints
- `/auth/login` – авторизація користувача (JWT)
- `/employees`, `/departments`, `/computers`, `/routers`, `/printers`, `/offices` – CRUD-операції
- `/apidocs/` – документація Swagger

## ✅ Висновок
У ході роботи створено та налаштовано **повноцінне хмарне середовище**:  
додаток Flask з JWT, MySQL-базою на RDS, автоматичним деплоєм через GitHub Actions і Swagger-документацією.
