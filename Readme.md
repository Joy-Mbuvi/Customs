PROJECT NAME : CUSTOMS

## Description

This project involves a web application that allows customers to create an account, authenticate using Google, and receive a JWT token for secure access to the platform. The application integrates with the Africa's Talking API in a test environment (sandbox mode) for processing orders. The project uses PostgreSQL as the database to manage customer data and orders.

The app's Continuous Integration (CI) is managed using GitHub Pages, while Continuous Deployment (CD) is handled through AWS Elastic Beanstalk. The customer ordering system allows users to place orders for products, and the backend is structured to support scalability and security with JWT authentication.

## Features

- **Customer Registration & Authentication**: Customers can create an account through a dedicated template at `http://localhost/custos/create`. After registering, they are redirected to Google for OAuth authentication. Upon successful login, the user is redirected to a page displaying their JWT token for secure communication with the backend.
  
- **Google Authentication**: OAuth authentication is integrated, allowing customers to sign in via Google. This is part of a seamless customer experience, ensuring secure and authenticated access to the platform.

- **JWT Token Generation**: After a successful Google sign-in, a JWT token is generated and provided to the customer. This token is used to authenticate API requests and ensure secure interactions with the backend.

- **Africa's Talking Integration**: For SMS and other communications, the platform integrates with the Africa's Talking API in a test sandbox environment. This ensures that development and testing can be performed without affecting live data.

- **PostgreSQL Database**: The application uses PostgreSQL to store customer information and order data, ensuring reliable and scalable storage for all platform activities.

- **Ordering System**: Customers can place orders for any available products. The order processing is integrated with the backend, allowing for seamless management of customer requests.

- **Testing**: Automated tests are created to ensure the reliability and performance of the customer authentication process and ordering system.

## Technologies Used

- **GitHub Pages**: Continuous Integration (CI) for building and deploying the application.
- **AWS Elastic Beanstalk**: Continuous Deployment (CD) for automatically deploying the application to the cloud.
- **Google OAuth**: User authentication using Google login.
- **Africa’s Talking API**: For communication (SMS, voice) in the sandbox environment.
- **PostgreSQL**: Database used to store customer data and orders.
- **JWT**: For secure token-based authentication.

## Setup Instructions

### Local Development

1. Clone this repository:
   git clone https://github.com/Joy-Mbuvi/Customs.git

2. create an enviroments:
python3 venv env


3. Install the requirements
 pip install -r requirements.txt

 4. Run the application
 python3 manage.py runserver

5. Navigate to `http://localhost/customs/create` to create a new customer. Follow the prompts to authenticate via Google, and obtain your JWT token after a successful login.

### Continuous Integration & Deployment

- **CI (GitHub Pages)**: The project is set up with GitHub Pages for automated CI workflows. Every change pushed to the repository triggers the build process and updates the GitHub Pages site.

- **CD (Elastic Beanstalk)**: The project is deployed using pythonanywhere

## API Endpoints

- `POST /customs/create`: Create a new customer and redirect to Google for authentication.
- `GET /auth/google`: Redirect to Google OAuth for login.
- `POST /customs/orders/new/`: Allow customers to place an order for any available product.
- 'GET/customs/orders/<int:customer_id>/': Get all orders associated with the customer.
-'GET/customs/customers/: fetches all the customers

## Testing

Automated tests are written to ensure that customer registration, Google OAuth authentication, and order placements work correctly. These tests are run automatically as part of the CI pipeline.

## License

This project is licensed under the MIT License 


