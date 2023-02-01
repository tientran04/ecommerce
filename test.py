from app import create_app, db
from app.models import Product, User
from app.config import Config
import unittest


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = "abc"


class ProductModelCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_get_price(self):
        for i in range(1,6):
            name = "product " + str(i)
            description = "description " + str(i)
            gender = "gender " + str(i)
            size = i
            color = "color " + str(i)
            price = i

            product = Product(name=name, description=description, gender=gender, 
                              size=size, color=color, price=price)
            db.session.add(product)
        db.session.commit()

        for i in range(1,6):
            product = Product.query.filter_by(id=i).first()
            self.assertEqual(product.get_price(), i)
        
    def test_update_price(self):
        for i in range(1,6):
            name = "product " + str(i)
            description = "description " + str(i)
            gender = "gender " + str(i)
            size = i
            color = "color " + str(i)
            price = i

            product = Product(name=name, description=description, gender=gender, 
                              size=size, color=color, price=price)
            db.session.add(product)
        db.session.commit()

        for i in range(1,6):
            product = Product.query.filter_by(id=i).first()
            product.update_price(i + 1)
            db.session.commit()
        
        for i in range(1,6):
            product = Product.query.filter_by(id=i).first()
            self.assertEqual(product.get_price(), i + 1)
        

class UserModelCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        user = User(first_name="a", last_name="b", status=False)
        user.set_password("123")
        self.assertTrue(user.verify_password("123"))   

    def test_activate(self):
        user = User(first_name="a", last_name="b")
        user.activate()
        self.assertTrue(user.status)
        
    def test_get_activation_code(self):
        user = User(first_name="a", last_name="b", email="abc@gmail.com")
        user.set_password("abc")
        db.session.add(user)
        db.session.commit()
        token = user.get_token()
        self.assertEqual(User.verify_token(token), user.email)


if __name__ == '__main__':
    unittest.main(verbosity=2)
