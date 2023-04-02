#This goes to /app_folder/__ini__.py and grabs the app variable which
#represents the web application
from app_folder import app
#This checks to see if the run.py script is being run as the main program if so
#run the flask web application by starting the development servero on default
#port which is 5000 on the local machine (localhost:5000)
if __name__ == "__main__":
    app.run()