# InforcePythonTask
task received 13.09.24 12:00

**ACTUAL TASK:**

A company needs internal service for its 'employees which helps them to make a decision at the lunch place. Each restaurant will be uploading menus
using the system every day over API.
Employees will vote for the menu before leaving for lunch on a mobile app for whom the backend has to be implemented. There are users who did not
update the app to the latest version and the backend has to support both versions. The mobile app always sends the build version in headers

**API FUNCTIONALITY:**

- Authentication
- Creating restaurant
- Uploading menu for restaurant (There should be a menu for each day)
- Creating employee
- Getting current day menu
- Getting results for the current day

**REQUIREMENTS:**

- Only Back End (no needs to add UI);
- REST architecture;
- Tech stack: Django + DRF, JWT, PostgreSQL, Docker(docker-compose),
PyTests;
- Added at least a few different tests;
- README.md with a description of how to run the system;
- Will be a + to add flake8 or smth similar

# Restaurant Menu Voting System

This is a Django-based backend system that allows users to create restaurants, upload menus, and vote on them. The system also supports authentication and versioning, ensuring compatibility with both current and outdated versions of mobile apps.

## Table of Contents
- [Installation](#installation)
- [Running the System](#running-the-system)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)

## Installation

### Prerequisites
- Python 3.8+
- Django 4.0+
- Docker (for containerized setup)

### Steps

1. **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. **Install Dependencies**
    Use `pip` to install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up the Database**
    Run migrations to set up your database:
   along the path *mealvote/mealvote/settings.py*
   change data about the database to your own, then
    ```bash
    python manage.py migrate
    ```

5. **Create a Superuser**
    Create an admin account for accessing the Django Admin Panel:
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the Development Server**
    Start the Django development server:
    ```bash
    python manage.py runserver
    ```

7. **Run with Docker (optional)**
    You can also use Docker to run the system. Build and start the containers using Docker Compose:
    ```bash
    docker-compose up --build
    ```

## Running the System

Once the server is running, you can access the following endpoints to interact with the system.

## API Endpoints

### 1. **Authentication Endpoints**
   These endpoints allow users to register and authenticate.

   - **User Registration**  
     Endpoint: `/users/register/`  
     Method: `POST`  
     Description: Allows a user to register an account.  
     Payload:
     ```json
     {
         "first_name": "user123",
         "last_name": "123user",
         "email": "user@example.com",
         "password": "password",
         "password2": "password",
         "phone_number": "+123456789"
     }
     ```

   - **User Login**  
     Endpoint: `/users/login/`  
     Method: `POST`  
     Description: Authenticates a user and returns a JWT token.  
     Payload:
     ```json
     {
         "email": "user@example.com",
         "password": "password"
     }
     ```

   - **User token refresh**  
     Endpoint: `/users/token/refresh/`  
     Method: `POST`  
     Description: Refreshes a users JWT token.  
     Payload:
     ```json
     {
         "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
     }
     ```

### 2. **Restaurant Endpoints**
   These endpoints are responsible for restaurant management, including creation, retrieval, and listing of restaurants.

   - **Create Restaurant**  
     Endpoint: `/restaurants/create/`  
     Method: `POST`  
     Description: Creates a new restaurant.  
     Payload:
     ```json
     {
         "name": "Restaurant Name",
         "address": "123 Street Name",
         "phone_number": "1234567890"
     }
     ```
   
   - **List All Restaurants**  
     Endpoint: `/restaurants/all/`  
     Method: `GET`  
     Description: Retrieves a list of all registered restaurants.

### 3. **Menu Endpoints**
   These endpoints are used to manage restaurant menus.

   - **Upload Menu**  
     Endpoint: `/restaurants/menu/upload/`  
     Method: `POST`  
     Description: Creates a menu for a restaurant on a specific date. You cannot create menus for past dates.  
     Payload:
     ```json
     {
         "restaurant": 1,
         "date": "2024-09-15",
         "items": "Sushi, Pizza, Burger"
     }
     ```

     Response on success:
     ```json
     {
         "id": 1,
         "restaurant": 1,
         "restaurant_name": "Restaurant Name",
         "date": "2024-09-15",
         "items": "Sushi, Pizza, Burger"
     }
     ```

     **Note:** If you try to create a menu for a past date, the system will return:
     ```json
     {
         "date": "Cannot set a menu for a past date. Please select today or a future date."
     }
     ```

   - **Today's Menu**  
     Endpoint: `/restaurants/menu/today/`  
     Method: `GET`  
     Description: Retrieves all menus available for the current day.

### 4. **Voting Endpoints**
   These endpoints allow users to vote for a particular restaurant based on their daily menu and view the voting results.

  - **Today's Menu**  
     Endpoint: `/voting/menu/today/`  
     Method: `GET`  
     Description: Retrieves all menus available for the current day.
    
  - **Today's Menu**  
     Endpoint: `/voting/vote/`  
     Method: `POST`  
     Description: There is a vote for the restaurant
    
  - **Today's Menu**  
     Endpoint: `/voting/results/`  
     Method: `GET`  
     Description: Gets the menu with the most votes for the current day.


## Running Tests

To ensure everything works as expected, you can run the system's tests:

1. **Run Unit Tests**
    ```bash
    python manage.py test
    ```

2. **Run Tests in Docker (if using Docker)**
    ```bash
    docker-compose exec web python manage.py test
    ```

## Future Improvements
- Improve voting logic.
- Implement a dual role for the user so that it is possible to choose
whether he is a worker or a restaurant representative and, depending on the role, grant access to certain endpoints.
- Implement role-based permissions for managing restaurants and menus.
- Add pagination for the restaurant list and menu list endpoints.
- The mobile app always sends the build version in headers. 


## License

This project is open source and available for anyone to use, modify, or improve. There is no specific license attached to it, and contributions are welcome.

