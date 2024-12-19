import unittest
from app import app, db
from flask import url_for
from app.models import User, Role, Category, Event  
from werkzeug.security import generate_password_hash
from app.helpers import make_login
from datetime import datetime
from flask_login import login_user

class EventsTests(unittest.TestCase):

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

                default_role = Role.query.filter_by(name='administrator').first()
                hashed_password = generate_password_hash('hashedpassword')
                self.user = User(name='testuser', email='test@example.com', password=hashed_password, id_role=default_role.id)
                db.session.add(self.user)
                db.session.commit()
                assert self.user.id is not None

                self.category = Category(name='Test Category')
                db.session.add(self.category)
                db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all() 
    
    def test_create_category(self):
        with self.app.app_context():
            response = make_login(self, 'testuser', 'hashedpassword')

            response = self.client.get(url_for('event.create_category'))
            csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]
        
            event_data = {
                'csrf_token':csrf_token,
                'name': 'Category'
            }

            response = self.client.post(url_for('event.create_category'), data=event_data, follow_redirects=True)

            self.assertEqual(response.status_code, 200) 
            self.assertIn('Category created successfully'.encode('utf-8'), response.data)

            with self.app.app_context():
                category = Category.query.filter_by(name='Category').first()
                self.assertIsNotNone(category)
                self.assertEqual(category.name, 'Category')
    
    def test_delete_category(self):
        with self.app.app_context():
            response = make_login(self, 'testuser', 'hashedpassword')

            response = self.client.get(url_for('event.create_category'))
            csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]
        
            event_data = {
                'csrf_token':csrf_token,
                'name': 'Category delete'
            }

            response = self.client.post(url_for('event.create_category'), data=event_data, follow_redirects=True)
            
            category = Category.query.filter_by(name='Category delete').first()
            category_id = category.id
            category_name = category.name
        
            event_data = {
                'csrf_token':csrf_token
            }
            response = self.client.post(f'/delete_category/{category_id}', data=event_data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            response = self.client.get('/events')
            self.assertNotIn(('%s'%category_name).encode('utf-8'), response.data) 

    def test_create_event(self):
        with self.app.app_context():
            response = make_login(self, 'testuser', 'hashedpassword')
            
            
            response = self.client.get(url_for('event.create_event'))
            csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]

            cat = Category.query.first()

            event_data = {
                'csrf_token': csrf_token,
                'name': 'Test Event',
                'header': 'Test Header',
                'description': 'Test Description',
                'date': '2024-09-15 13:42:46',  
                'category': cat.id,
                'save_and_view': False  
            }

            
            response = self.client.post(url_for('event.create_event'), data=event_data, follow_redirects=True)

            self.assertEqual(response.status_code, 200)  
            self.assertIn(b'Event created successfully.', response.data)  

            with self.app.app_context():
                event = Event.query.filter_by(name='Test Event').first()
                self.assertIsNotNone(event)  
                self.assertEqual(event.header, 'Test Header') 
    
    def test_get_events(self):
        with self.app.app_context():
            response = make_login(self, 'testuser', 'hashedpassword')
            
            response = self.client.get(url_for('event.create_event'))
            csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]

            cat = Category.query.first()

            event_data = {
                'csrf_token': csrf_token,
                'name': 'Test List Event',
                'header': 'Test List Header',
                'description': 'Test List Description',
                'date': '2024-09-15 13:42:46',
                'category': cat.id,
                'save_and_view': False 
            }
            
            response = self.client.post(url_for('event.create_event'), data=event_data, follow_redirects=True)

            response = self.client.get('/events')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test List Event', response.data)
    
    def test_update_event(self):
        with self.app.app_context():
            response = make_login(self, 'testuser', 'hashedpassword')
            
            response = self.client.get(url_for('event.create_event'))
            csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]

            cat = Category.query.first()

            event_data = {
                'csrf_token': csrf_token,
                'name': 'Test Update Event',
                'header': 'Test Update Header',
                'description': 'Test Update Description',
                'date': '2024-09-15 13:42:46',
                'category': cat.id,
                'save_and_view': False 
            }

            response = self.client.post(url_for('event.create_event'), data=event_data, follow_redirects=True)
        
            event_id = Event.query.filter_by(name='Test Update Event').first().id
            
            response = self.client.get(url_for('event.edit_event', event_id=event_id))
            csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]
            
            update_event_data = {
                'csrf_token': csrf_token,
                'name': 'Change Update Name',
                'header': 'Change Update Header',
                'description': 'Change Update Description',
                'date': '2024-09-15 13:42:46',
                'category': cat.id,
                'save_and_view': False
            }

            response = self.client.post(url_for('event.edit_event', event_id=event_id), data=update_event_data, follow_redirects=True)
            self.assertEqual(response.status_code, 200) 
            self.assertIn(b'Event updated successfully', response.data) 
            
            updated_item = self.client.get(url_for('event.list_events'))
            self.assertIn(b'Change Update Name', updated_item.data)
    

    def test_delete_event(self):
        with self.app.app_context():
            response = make_login(self, 'testuser', 'hashedpassword')

            response = self.client.get(url_for('event.create_event'))
            csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]
        
            cat = Category.query.first()

            event_data = {
                'csrf_token': csrf_token,
                'name': 'Test Delete Event',
                'header': 'Test Delete Header',
                'description': 'Test Delete Description',
                'date': '2024-09-15 13:42:46',
                'category': cat.id,
                'save_and_view': False
            }

            response = self.client.post(url_for('event.create_event'), data=event_data, follow_redirects=True)
            
            event = Event.query.filter_by(name='Test Delete Event').first()
            event_id = event.id
            event_name = event.name
        
            event_data = {
                'csrf_token':csrf_token
            }
            response = self.client.post(f'/delete_event/{event_id}', data=event_data, follow_redirects=True)
            self.assertEqual(response.status_code, 200) 
            response = self.client.get('/events')
            self.assertNotIn(('%s'%event_name).encode('utf-8'), response.data)
    

if __name__ == '__main__':
    unittest.main()