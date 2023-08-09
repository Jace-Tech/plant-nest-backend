# Plant Nest Backend / API

Contains the API for the frontend and also the views to the admin management portal

## Installation

- Create a virtual enviroment

  ```shell
    # In Windows 
    py -m venv venv

    # In Unix (Mac | Linux)
    python3 -m venv venv
  ```

- Install the packages from the `requirements.txt` by running `pip install -r requirements.txt`

- Create a new `.env` file in the root of your directory, and then add in all the variables from the `.env.examples` with the appropriate values

- Finally, run the app with `gunicorn --workers=2 'app:create_app()'`
