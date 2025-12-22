from app import create_app  # Import the create_app function from the wm278_coursework module

run = create_app()  # Create an instance of the Flask application using the create_app function

if __name__ == '__main__':
    run.run(debug=True)  # Run the Flask application in debug mode if the script is executed directly
