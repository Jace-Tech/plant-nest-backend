from app import create_app

if __name__ == '__main__':
    # START APP
    app = create_app()
    app.run(debug=True, port=4000)
