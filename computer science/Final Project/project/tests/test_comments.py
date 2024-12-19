import unittest
from app import app, db
from flask import url_for
from app.models import User, Role, Event, Comment 
from werkzeug.security import generate_password_hash
from app.helpers import make_login
from datetime import datetime
from flask_login import login_user

class CommentsTests(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
        self.app.config['SERVER_NAME'] = 'localhost'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            
            from app.models import Category
            if not Category.query.first():
                category = Category(name='general')
                db.session.add(category)

                category = Category(name='football')
                db.session.add(category)

                db.session.commit()
            

            if not Role.query.first():
                viewer_role = Role(name='viewer')
                db.session.add(viewer_role)

                journalist_role = Role(name='journalist')
                db.session.add(journalist_role)

                administrator_role = Role(name='administrator')
                db.session.add(administrator_role)
                db.session.commit()

                # Crear user for test
                default_role = Role.query.filter_by(name='administrator').first()
                hashed_password = generate_password_hash('hashedpassword')
                self.user = User(name='testuser', email='test@example.com', password=hashed_password, id_role=default_role.id)
                db.session.add(self.user)
                db.session.commit()
                assert self.user.id is not None

                # Create category for test
                self.category = Category(name='Test Category')
                db.session.add(self.category)
                db.session.commit()

                # Create event for test
                self.event = Event(name='Test Event', header='Test Header', description='Test Description',
                date=datetime.now(),
                id_category=self.category.id,
                id_user_creator=self.user.id)
                db.session.add(self.event)
                db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_create_comment(self):
        with self.app.app_context():
            response = make_login(self, 'testuser', 'hashedpassword')

            event_id = Event.query.first().id
            response = self.client.get(url_for('event.view_event', event_id=event_id))
            csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]
        
            event_data = {
                'csrf_token':csrf_token,
                'text': 'Comment 1'
            }

            response = self.client.post(url_for('comment.create_comment', event_id=event_id), data=event_data, follow_redirects=True)

            self.assertEqual(response.status_code, 200) 
            self.assertIn('Comment created successfully'.encode('utf-8'), response.data) 

            with self.app.app_context():
                comment = Comment.query.first()
                self.assertIsNotNone(comment) 
                self.assertEqual(comment.text, 'Comment 1') 
    
    
    def test_delete_comment(self):
         with self.app.app_context():
            response = make_login(self, 'testuser', 'hashedpassword')

            
            event = Event.query.first()
            print(event)
            print(event.id)
            print(event.name)
            event_id = event.id 
            response = self.client.get(url_for('event.view_event', event_id=event_id))
            csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]
        
            event_data = {
                'csrf_token':csrf_token,
                'text': 'Comment 1'
            }

            response = self.client.post(url_for('comment.create_comment', event_id=event_id), data=event_data, follow_redirects=True)

            self.assertEqual(response.status_code, 200)


            comment = Comment.query.filter_by(text='Comment 1').first()
            comment_id = comment.id

            event_data = {
                'csrf_token':csrf_token
            }

            response = self.client.post(url_for('comment.delete_comment', event_id=event_id, comment_id=comment_id), data=event_data)
            self.assertEqual(response.status_code, 302) 
            self.assertNotIn('Comment successfully deleted'.encode('utf-8'), response.data)

if __name__ == '__main__':
    unittest.main()