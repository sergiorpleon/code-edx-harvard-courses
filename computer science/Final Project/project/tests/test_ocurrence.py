import unittest
from app import app, db
from flask import url_for
from app.models import User, Role, EventOccurrence, Event, OcurrenceTypeEnum, SurveyResponse, SurveyOption 
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
    

    def test_get_ocurrences(self):
        with self.app.app_context():
            response = make_login(self, 'testuser', 'hashedpassword')

            event = Event.query.first()

            response = self.client.get(url_for('ocurrence.create_ocurrence', event_id=event.id))
            csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]

            
            options_data = [
                {'option': 'Option 1'},
                {'option': 'Option 2'},
                {'option': 'Option 3'},
                {'option': 'Option 4'},
                {'option': 'Option 5'},
            ]

            ocurrence_data = {
                'csrf_token':csrf_token,
                'text': 'Ocurrence text',
                'ocurrence_type': OcurrenceTypeEnum.NARRATION.name,
                #'options': options_data
                'options-0-option': 'Option 1',
                'options-1-option': 'Option 2',
                'options-2-option': 'Option 3',
                'options-3-option': 'Option 4',
                'options-4-option': 'Option 5' 
            }

            response = self.client.post(url_for('ocurrence.create_ocurrence', event_id=event.id), data=ocurrence_data, follow_redirects=True)


            response = self.client.get(url_for('event.view_event', event_id=event.id))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Ocurrence text', response.data)

    def test_create_survey(self):
        with self.app.app_context():
            response = make_login(self, 'testuser', 'hashedpassword')

            event = Event.query.first()

            response = self.client.get(url_for('ocurrence.create_ocurrence', event_id=event.id))
            csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]

            
            options_data = [
                {'option': 'Option 1'},
                {'option': 'Option 2'},
                {'option': 'Option 3'},
                {'option': 'Option 4'},
                {'option': 'Option 5'},
            ]

            ocurrence_data = {
                'csrf_token':csrf_token,
                'text': 'Ocurrence text',
                'ocurrence_type': OcurrenceTypeEnum.SURVEY.name,
                #'options': options_data 
                'options-0-option': 'Option 1',
                'options-1-option': 'Option 2',
                'options-2-option': 'Option 3',
                'options-3-option': 'Option 4',
                'options-4-option': 'Option 5'
            }

            response = self.client.post(url_for('ocurrence.create_ocurrence', event_id=event.id), data=ocurrence_data, follow_redirects=True)

            self.assertEqual(response.status_code, 200) 
            self.assertIn('Event ocurrence created successfully'.encode('utf-8'), response.data)  
            
            self.assertEqual(len(SurveyOption.query.all()), 5)
            self.assertIn('Option 1'.encode('utf-8'), response.data)  
            
            with self.app.app_context():
                ocurrence = EventOccurrence.query.first()
                self.assertIsNotNone(ocurrence)  
                self.assertEqual(ocurrence.text, 'Ocurrence text')

    def test_vote_survey(self):
        with self.app.app_context():
            response = make_login(self, 'testuser', 'hashedpassword')

            event = Event.query.first()

            response = self.client.get(url_for('ocurrence.create_ocurrence', event_id=event.id))
            csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]

            
            options_data = [
                {'option': 'Option 1'},
                {'option': 'Option 2'},
                {'option': 'Option 3'},
                {'option': 'Option 4'},
                {'option': 'Option 5'},
            ]

            ocurrence_data = {
                'csrf_token':csrf_token,
                'text': 'Ocurrence text',
                'ocurrence_type': OcurrenceTypeEnum.SURVEY.name,
                #'options': options_data 
                'options-0-option': 'Option 1',
                'options-1-option': 'Option 2',
                'options-2-option': 'Option 3',
                'options-3-option': '',
                'options-4-option': ''
            }

            response = self.client.post(url_for('ocurrence.create_ocurrence', event_id=event.id), data=ocurrence_data, follow_redirects=True)

            self.assertEqual(response.status_code, 200)  
            self.assertIn('Event ocurrence created successfully'.encode('utf-8'), response.data)  
            
            self.assertEqual(len(SurveyOption.query.all()), 3)
            self.assertIn('Option 1'.encode('utf-8'), response.data)  
            
            ocurrence = EventOccurrence.query.first()
            response = self.client.get(url_for('ocurrence.vote_ocurrence', event_id=event.id, ocurrence_id=ocurrence.id), follow_redirects=True)
            csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]

            ocurrence_data = {
                'csrf_token':csrf_token,
            }
            option = SurveyOption.query.filter_by(option="Option 1").first()
            response = self.client.post(url_for('ocurrence.vote', event_id=event.id, ocurrence_id=ocurrence.id, option_id=option.id), data=ocurrence_data, follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)  
            self.assertEqual(len(SurveyResponse.query.all()), 1)
            
            # Not can vote more of one time. SurveyResponse == 1
            response = self.client.post(url_for('ocurrence.vote', event_id=event.id, ocurrence_id=ocurrence.id, option_id=option.id), data=ocurrence_data, follow_redirects=True)
            
            self.assertEqual(response.status_code, 200) 
            self.assertEqual(len(SurveyResponse.query.all()), 1)

    def test_update_ocurrence(self):
        with self.app.app_context():
            response = make_login(self, 'testuser', 'hashedpassword')

            event = Event.query.first()

            response = self.client.get(url_for('ocurrence.create_ocurrence', event_id=event.id))
            csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]

            
            options_data = [
                {'option': 'Option 1'},
                {'option': 'Option 2'},
                {'option': 'Option 3'},
                {'option': 'Option 4'},
                {'option': 'Option 5'},
            ]

            ocurrence_data = {
                'csrf_token':csrf_token,
                'text': 'Ocurrence text',
                'ocurrence_type': OcurrenceTypeEnum.NARRATION.name,
                'options': options_data 
            }

            response = self.client.post(url_for('ocurrence.create_ocurrence', event_id=event.id), data=ocurrence_data, follow_redirects=True)

            self.assertEqual(response.status_code, 200) 
            self.assertIn('Event ocurrence created successfully'.encode('utf-8'), response.data)  
        
            ocurrence_id = EventOccurrence.query.filter_by(text='Ocurrence text').first().id
            
            
            response = self.client.get(url_for('ocurrence.edit_ocurrence', event_id=event.id, ocurrence_id=ocurrence_id))
            csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]
            
            update_ocurrence_data = {
                'csrf_token':csrf_token,
                'text': 'Ocurrence text change',
                'ocurrence_type': OcurrenceTypeEnum.NARRATION.name,
                'options': options_data 
            }

            response = self.client.post(url_for('ocurrence.edit_ocurrence', event_id=event.id, ocurrence_id=ocurrence_id), data=update_ocurrence_data, follow_redirects=True)
            self.assertEqual(response.status_code, 200) 
            self.assertIn(b'Event Ocurrence updated successfully', response.data)  
            
            updated_item = self.client.get(url_for('event.view_event', event_id=event.id))
            self.assertIn(b'Ocurrence text change', updated_item.data)
    

    def test_delete_ocurrence(self):
        with self.app.app_context():
            response = make_login(self, 'testuser', 'hashedpassword')

            event = Event.query.first()

            response = self.client.get(url_for('ocurrence.create_ocurrence', event_id=event.id))
            csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]

            
            options_data = [
                {'option': 'Option 1'},
                {'option': 'Option 2'},
                {'option': 'Option 3'},
                {'option': 'Option 4'},
                {'option': 'Option 5'},
            ]

            ocurrence_data = {
                'csrf_token':csrf_token,
                'text': 'Ocurrence text',
                'ocurrence_type': OcurrenceTypeEnum.NARRATION.name,
                'options': options_data 
            }

            response = self.client.post(url_for('ocurrence.create_ocurrence', event_id=event.id), data=ocurrence_data, follow_redirects=True)

            ocurrence = EventOccurrence.query.filter_by(text='Ocurrence text').first()
            ocurrence_id = ocurrence.id
            ocurrence_name = ocurrence.text
        
            event_data = {
                'csrf_token':csrf_token
            }
            
            response = self.client.post(url_for('ocurrence.delete_ocurrence', event_id=event.id, ocurrence_id=ocurrence_id), data=event_data, follow_redirects=True)
            self.assertEqual(response.status_code, 200) 
            self.assertIn(b'Event Ocurrence successfully deleted', response.data) 
            
            response = self.client.get(url_for('event.view_event', event_id=event.id))
            self.assertNotIn(('%s'%ocurrence_name).encode('utf-8'), response.data)  
    
    
    

if __name__ == '__main__':
    unittest.main()