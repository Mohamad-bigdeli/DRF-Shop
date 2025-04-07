<h1> Introduction to the ShopBackend Project </h1>

**A Backend Platform for E-Commerce with Optimized Architecture**

ShopBackend is a powerful and efficient backend system for online stores developed with Django, covering all essential needs of an online shop including product management, shopping cart, secure payments, and user authentication. This project provides a secure and reliable foundation for digital businesses with its optimized architecture and use of modern technologies.

### Key Features and Technologies Used

🔐 **Secure Authentication and User Management**  
- JWT-based authentication for high security  
- Two-factor authentication with OTP (One-Time Password)  
- Simple and efficient user model with two access levels:  
  - Regular user  
  - Admin (full access)  

🛒 **Smart Shopping Cart and Order Processing**  
- Fast shopping cart caching with Redis  
- Asynchronous order processing with Celery + Redis  
- Order tracking system with statuses:  
  - Pending payment  
  - Processing  
  - Completed  
  - Canceled  

💳 **Secure Payments with ZarinPal**  
- Full support for the ZarinPal payment gateway
- Transaction processing is done entirely asynchronously using Celery.

📦 **Advanced Product Management**  
- Smart product search with elastic search
- Review and rating system  
- Automatic final price calculation including discounts  
- Support for multiple images for each product  

📊 **Optimized and Scalable Architecture**  
- Clean and documented APIs with Django REST Framework  
- PostgreSQL database for reliable performance  
- Background processing for heavy operations  
- Easy deployment with Docker  

<h1>db Diagram</h1>

![db Diagram](https://raw.githubusercontent.com/Mohamad-bigdeli/DRF-Shop/main/docs/db_diagram.png)

<h1>Technologies</h1>


![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-005571?style=for-the-badge&logo=elasticsearch&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=json-web-tokens&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=white)
![Ruff](https://img.shields.io/badge/Ruff-000000?style=for-the-badge&logo=black&logoColor=white)

## 🚀 Project Setup

To set up the project, follow the steps below:

### Prerequisites
- **Docker**: If you don't have Docker and Docker Compose installed, follow the [Docker installation guide](https://docs.docker.com/get-docker/) and the [Docker Compose installation guide](https://docs.docker.com/compose/install/).

---

### Setup Steps

1. **Clone the Repository**
  
   Clone the project repository to your local machine:

   ```bash
   git clone https://github.com/Mohamad-bigdeli/DRF-Shop.git

2. **Navigate to the Project Folder**

    Move into the project directory using the cd command:

    ```bash
    cd DRF-Shop
    

3. **Start Docker Compose** 

    Use Docker Compose to start the project services by running the command:

    ```bash
    docker-compose up --build 

4. **Create and Apply Migrations**

    After the services are up, create and apply the database migrations using the following commands:
    ```bash 
    docker-compose exec backend sh -c "python manage.py makemigrations"

    docker-compose exec backend sh -c "python manage.py migrate"

5. **Create a Superuser**

    Create a superuser to access the Django admin panel by running the command:

    ```bash
    docker-compose exec backend sh -c "python manage.py createsuperuser"

6. **Collect Static Files**

    Collect static files for the project using the command:

    ```bash
    docker-compose exec backend sh -c "python manage.py collectstatic --noinput"
    
7. **View the Project**

    Your project is now running on port 8000. Open your browser and navigate to:

   ```bash
    http://localhost:8000.

8. **Access the Admin Panel**

    To access the Django admin panel, go to the following URL and log in with your superuser credentials:

    ```bash
    http://localhost:8000/admin

**Additional Notes**

    If you make changes to the code and need to restart the services, use the docker-compose restart command.
    To stop the services, use the docker-compose down command.

<h3>By following these steps, your project will be fully set up and ready to use. 🎉</h3>
