import unittest
from app import app, db
from flask import url_for
from app.models import User, Role 
from werkzeug.security import generate_password_hash
from app.helpers import make_login

class AuthTests(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
        self.app.config['SERVER_NAME'] = 'localhost'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all() 

            if not Role.query.first():
                viewer_role = Role(name='viewer')
                db.session.add(viewer_role)

                journalist_role = Role(name='journalist')
                db.session.add(journalist_role)

                administrator_role = Role(name='administrator')
                db.session.add(administrator_role)
                db.session.commit()

            # Create user for test
            default_role = Role.query.first()
            hashed_password = generate_password_hash('hashedpassword')
            self.user = User(name='testuser', email='test@example.com', password=hashed_password, id_role=default_role.id)
            db.session.add(self.user)
            db.session.commit()
            assert self.user.id is not None

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all() 

    def test_login_success(self):
        with self.app.app_context():
            response = make_login(self, 'testuser', 'hashedpassword')

            self.assertEqual(response.status_code, 200)  
            self.assertIn('Successful login'.encode('utf-8'), response.data) 

    def test_login_failure(self):
        with self.app.app_context():
            response = make_login(self, 'wronguser', 'wrongpassword')

            self.assertEqual(response.status_code, 200) 
            self.assertIn('Incorrect email or password'.encode('utf-8'), response.data) 
            

    def test_logout(self):
        with self.app.app_context():
            response = make_login(self, 'testuser', 'hashedpassword')

            response = self.client.get('/logout', follow_redirects=True)

            self.assertEqual(response.status_code, 200) 
            self.assertIn('You have successfully logged out'.encode('utf-8'), response.data)
            
    def test_register_success(self):
        with self.app.app_context():
            response = self.client.get(url_for('user.register'))
            csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]
        
            response = self.client.post('/register', data={
                'csrf_token': csrf_token,
                'name': 'newuser',
                'email': 'newuser@example.com',
                'password': 'newpassword',
                'confirmation': 'newpassword'
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200) 
            self.assertIn('Successful registration'.encode('utf-8'), response.data)

    def test_register_failure_email_taken(self):
        with self.app.app_context():
            response = self.client.get(url_for('user.register'))
            csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]
        
            response = self.client.post('/register', data={
                'csrf_token': csrf_token,
                'name': 'testuser',  
                'email': 'test@example.com',
                'password': 'newpassword',
                'confirmation': 'newpassword'
            }, follow_redirects=True)
            
            self.assertEqual(response.status_code, 200) 
            self.assertIn('The email is already registered'.encode('utf-8'), response.data) 

if __name__ == '__main__':
    unittest.main()