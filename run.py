#this goes to __ini__.py and grabs the app variable, and db, and ?runs throug the rest of file?
from app_folder import app, db

#This creates the db models
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()