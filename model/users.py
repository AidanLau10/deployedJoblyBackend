'''
users.py provied by teacher but I added a status column to distinguish users from freelancers and employers
'''

import json
from .jobs import Job
from .jobuser import JobUser
from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'  


    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _status = db.Column(db.String(20), unique=False, nullable=False)

    users = db.relationship('JobUser', backref='users', uselist=True, lazy='dynamic')
    jobpostees = db.relationship('Job', backref='users', uselist=True, lazy='dynamic')
    applications = db.relationship('Application', backref='users', uselist=True, lazy='dynamic')
   
    # constructor to initialize the data when the user object is being made with proper attributes/parameters
    def __init__(self, name, uid, password="123qwerty", status="unknown"):
        self._name = name    # variables with self prefix become part of the object, 
        self._uid = uid
        self.set_password(password)
        self._status = status

    # method that gets the name from the object
    @property
    def name(self):
        return self._name
    
    # setter function that allows the name to be updated 
    @name.setter
    def name(self, name):
        self._name = name
    
    # method that gets the status from the object
    @property
    def status(self):
        return self._status
    
    # setter function that allows the status to be updated
    @status.setter
    def status(self, status):
        self._status = status
    
    # method that gets the uid from the object
    @property
    def uid(self):
        return self._uid
    
    # setter function that allows the uid to be updated
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # checks if uid matches the user object uid
    def is_uid(self, uid):
        return self._uid == uid
    
    # method that gets the password from the object
    @property
    def password(self):
        return self._password[0:10] + "..." 

    # update password, this is conventional setter
    def set_password(self, password):
        """Create a hashed password."""
        self._password = generate_password_hash(password, "pbkdf2:sha256", salt_length=10)

    # check password parameter versus stored/encrypted password
    def is_password(self, password):
        """Check against hashed password."""
        result = check_password_hash(self._password, password)
        return result
    
    # output the content for API responses in JSON form which humans can read
    def __str__(self):
        return json.dumps(self.read())
    
    # function/method to create the user object
    def create(self):
        try:
            db.session.add(self) 
            db.session.commit()  
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # function/method that returns the details of the user object in a dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
            "status": self.status,
        }

    # functio/method to update the details of the user object
    def update(self, name="", uid="", password=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(password) > 0:
            self.set_password(password)
        db.session.commit()
        return self

    # function/method to delete the user object
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

# function that initializes test data
def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        users = [
        User(name='The Employer', uid='employer', password='123employer', status="Employer"),
        User(name='The Freelancer', uid='freelancer', password='123freelancer', status="Freelancer"),
        User(name='Another Employer', uid='anotheremployer', password='123anotheremployer', status="Employer"),
        User(name='Another Freelancer', uid='anotherfreelancer', password='123anotherfreelancer', status="Freelancer"),
        User(name='Desperate Freelancer', uid='desperatefreelancer', password='123desperate', status="Freelancer"),
        User(name='Not-so Desperate Freelancer', uid='notdesperatefreelancer', password='123notdesperate', status="Freelancer"),
        User(name='Freelancer1', uid='freelancer1', password='123freelancer1', status='Freelancer'),
        User(name='Freelancer2', uid='freelancer2', password='123freelancer2', status='Freelancer'),
        User(name='Freelancer3', uid='freelancer3', password='123freelancer3', status='Freelancer'),
        User(name='Freelancer4', uid='freelancer4', password='123freelancer4', status='Freelancer'),
        User(name='Freelancer5', uid='freelancer5', password='123freelancer5', status='Freelancer'),
        User(name='Freelancer6', uid='freelancer6', password='123freelancer6', status='Freelancer'),
        User(name='Freelancer7', uid='freelancer7', password='123freelancer7', status='Freelancer'),
        User(name='Freelancer8', uid='freelancer8', password='123freelancer8', status='Freelancer'),
        User(name='Freelancer9', uid='freelancer9', password='123freelancer9', status='Freelancer'),
        User(name='Freelancer10', uid='freelancer10', password='123freelancer10', status='Freelancer'),
        User(name='Freelancer11', uid='freelancer11', password='123freelancer11', status='Freelancer'),
        User(name='Freelancer12', uid='freelancer12', password='123freelancer12', status='Freelancer'),
        User(name='Freelancer13', uid='freelancer13', password='123freelancer13', status='Freelancer'),
        User(name='Freelancer14', uid='freelancer14', password='123freelancer14', status='Freelancer'),
        User(name='Freelancer15', uid='freelancer15', password='123freelancer15', status='Freelancer'),
        User(name='Freelancer16', uid='freelancer16', password='123freelancer16', status='Freelancer'),
        ]


        """Builds sample user/note(s) data"""
        for user in users:
            try:
                
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.uid}")

