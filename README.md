# PlantNest E-commerce Platform [Backend / API]

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [API Reference](#api-reference)
- [Contributing](#contributing)

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
   git clone https://github.com/Jace-Tech/plant-nest-backend.git
   ```

2. Navigate to the project directory:

   ```bash
   cd plant-nest-backend
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

## API Reference

- The PlantNest API provides endpoints for user registration, authentication, product management, shopping cart, and order handling. See [API Documentation](https://documenter.getpostman.com/view/18481947/2s9Xy5LVM2#77ee463f-d2a9-414f-a832-286d792b0bc9) for detailed information.

## Contributing

- Fork the repository and create a new branch for your contributions.
- Make your changes and submit a pull request.
- Follow the project's coding style and guidelines.