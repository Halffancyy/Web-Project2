import unittest
from app import create_app, db
from config import TestConfig
from models import User, Comment

class BasicTests(unittest.TestCase):

    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        
        self.add_test_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def add_test_data(self):
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

    def test_user_registration(self):
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')

    def test_password_hashing(self):
        user = User.query.filter_by(username='testuser').first()
        self.assertTrue(user.check_password('testpassword'))
        self.assertFalse(user.check_password('wrongpassword'))

    def test_add_comment(self):
        user = User.query.filter_by(username='testuser').first()
        comment = Comment(content='This is a test comment', user_id=user.id, request_id=1)
        db.session.add(comment)
        db.session.commit()
        saved_comment = Comment.query.filter_by(user_id=user.id).first()
        self.assertIsNotNone(saved_comment)
        self.assertEqual(saved_comment.content, 'This is a test comment')

if __name__ == '__main__':
    unittest.main()
