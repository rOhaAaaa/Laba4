# ☁️ Laba 1: Хмарне розгортання Flask API

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

☁️ Laba 2: Контейнеризація та автоматичне масштабування REST API
🧩 Опис

У межах лабораторної роботи створено контейнеризований REST API-сервіс, розгорнутий у хмарному середовищі AWS ECS (Fargate).
Система реалізує автоматичне масштабування контейнерів залежно від навантаження CPU, а також використовує окремий контейнер-генератор навантаження (k6) для тестування продуктивності.

🔧 Реалізовано

Створено Docker-образ Flask REST API на основі попередньої лабораторної роботи.

Завантажено образ у Amazon ECR і розгорнуто контейнер як ECS Fargate service.

Налаштовано автоматичне масштабування (Target Tracking Policy за метрикою CPUUtilization).

Реалізовано endpoint /heavy з режимами CPU та memory для імітації навантаження.

Створено окремий контейнер-навантажувач (load generator) з Grafana k6, який автоматично генерує запити до API.

Проведено моніторинг через Amazon CloudWatch (CPUUtilization, Scaling Activities, ECS events).

Після виконання тесту контейнери loadgen-сервісу автоматично завершують роботу.

🧰 Використані технології

Python 3.12, Flask, Flask-RESTx

Docker + Amazon ECR / ECS (Fargate)

AWS CloudWatch — моніторинг і тригери масштабування

AWS Application Auto Scaling — Target Tracking Policy

Grafana k6 — генератор навантаження (VUs, Duration, Target)

IAM Roles, CloudWatch Logs — доступи та логування ECS taskів

⚙️ Основні елементи

/heavy?seconds=3&mode=cpu — endpoint для створення CPU-навантаження

ECS Task Definition: параметри CPU=512, Memory=1024, autoscaling 1→2 контейнери

Load Generator (k6): 20 VUs, 5 хв тривалість, TARGET=http://<API>:8080/heavy

CloudWatch Graphs: CPUUtilization, Scaling Activities Logs

✅ Висновок

У результаті роботи створено повноцінну інфраструктуру контейнеризованого застосунку:
API-сервіс Flask автоматично масштабується під час підвищеного навантаження, а після зменшення — кількість контейнерів зменшується.
Використано AWS ECS Fargate, ECR, CloudWatch та генератор навантаження k6 для повного циклу тестування та моніторингу масштабування.
