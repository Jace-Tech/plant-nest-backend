# PlantNest E-commerce Platform [Backend / API]

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [User Authentication](#user-authentication)
  - [Product Catalog](#product-catalog)
  - [Shopping Cart](#shopping-cart)
  - [Order Management](#order-management)
  - [Admin Dashboard](#admin-dashboard)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## Introduction

PlantNest is an e-commerce platform that specializes in providing a wide variety of plants and gardening accessories. This documentation provides an overview of the features, setup instructions, usage guidelines, and API reference for the PlantNest application.

## Features

- User registration and authentication
- Browse and search the product catalog
- Add products to the shopping cart
- Place orders and manage order history
- Admin dashboard for managing products and orders

## Setup

### Prerequisites

- Python 3.x
- Flask web framework
- Flask-JWT-Extended for JWT authentication
- SQLAlchemy for database management
- Flask-CORS for handling CORS issues

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/plantnest.git
   ```

2. Navigate to the project directory:

   ```bash
   cd plantnest
   ```

3. Create a virtual enviroment

  ```shell
    # In Windows 
    py -m venv venv

    # In Unix (Mac | Linux)
    python3 -m venv venv
  ```

4. Install the required packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

5. Create a new `.env` file in the root of your directory, and then add in all the variables from the `.env.examples` with the appropriate values

6. Finally, run the app with `gunicorn --workers=2 'app:create_app()'` or 

  ```bash
  # Windows
  py app.py

  #Unix
  python3 app.py
  ```

## Configuration

1. Open the `config.py` file and configure the following settings:

   - Database connection URL
   - Secret key for JWT authentication
   - CORS settings

2. Set up your database:

   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

## Usage

### Admin Authentication

- Register a new user account
  > Open the `localhost:4000/signup` to 
- Log in using registered credentials
- Obtain JWT token for authentication

### Product Catalog

- Browse and search for plants and accessories
- View detailed information about each product
- Filter products by category or type

### Shopping Cart

- Add products to the shopping cart
- View and adjust cart contents
- Proceed to checkout

### Order Management

- Place orders for selected items
- View order history and details
- Mark orders as completed or canceled

### Admin Dashboard

- Access the admin dashboard using appropriate credentials
- Manage products (add, update, delete)
- Monitor and fulfill orders

## API Reference

- The PlantNest API provides endpoints for user registration, authentication, product management, shopping cart, and order handling. See [API Documentation](api-documentation.md) for detailed information.

## Contributing

- Fork the repository and create a new branch for your contributions.
- Make your changes and submit a pull request.
- Follow the project's coding style and guidelines.

## License

PlantNest is released under the [MIT License](LICENSE).

---

This documentation template provides an outline of the important sections for your PlantNest e-commerce project. Customize the content as needed and add more details specific to your project's implementation.