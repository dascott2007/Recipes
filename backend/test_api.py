import unittest
from main import create_app
from config import TestConfig
from exts import db


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app=create_app(TestConfig)
        self.client=self.app.test_client(self) #takes in the parent app

        with self.app.app_context():
            # db.init_app(self.app)
            db.create_all()
    
    def test_hello_world(self):
        hello_response=self.client.get('/recipe/hello')

        json=hello_response.json
        # print(json)
        self.assertEqual(json, {"message": "Hello World"})

    def test_signup(self):
        signup_response=self.client.post(
            '/auth/signup',
            json={
                "username":"testuser", 
                "email":"testuser@test.com", 
                "password":"password"
                }
        )
        status_code=signup_response.status_code
        # print("Signup "f'{status_code}')

        self.assertEqual(status_code, 200)

    def test_login(self):
        signup_response=self.client.post(
            '/auth/signup',
            json={
                "username":"testuser", 
                "email":"testuser@test.com", 
                "password":"password"
                }
        )
        login_response=self.client.post(
            'auth/login',
            json={
                "username":"testuser", 
                "password":"password"
            }
        )
        status_code=login_response.status_code
        # print("Login "f'{status_code}')
        
        # Will give us access and refresh token
        # json=login_response.json
        # print(json) 

        self.assertEqual(status_code, 200)

    def test_get_all_recipes(self):
        """Test Getting all recipes"""
        response=self.client.get('/recipe/recipes')
        
        # json = response.json
        # print(response.json)

        status_code=response.status_code
        # print("Test get all recipes "f'{status_code}')
        self.assertEqual(status_code, 200)


    def test_get_one_recipe(self):
        """Test Getting one recipe"""
        id=1
        response=self.client.get(f'/recipe/recipe/{id}')
        # print(response)
        status_code=response.status_code

        self.assertEqual(status_code, 200)
        # self.assertEqual(status_code, 404) # 404 because there are no recipes yet
        # print("Test get one recipe "f'{status_code}')

    def test_create_recipe(self):
        signup_response=self.client.post(
            '/auth/signup',
            json={
                "username":"testuser", 
                "email":"testuser@test.com", 
                "password":"password"
                },
            content_type='application/json' # I don't know if we need this
        )
        login_response=self.client.post(
            'auth/login',
            json={
                "username":"testuser", 
                "password":"password"
            },
            content_type='application/json' # I don't know if we need this
        )
        access_token=login_response.json["access_token"]

        create_recipe_response=self.client.post(
            '/recipe/recipes',

            json={
                "title": "Test Cookie",
                "description": "test description"
            },
            headers={
                "Authorization":f"Bearer {access_token}"
            }, 
          
        )
        status_code=create_recipe_response.status_code
        # view the recipe getting created
        # print(create_recipe_response.json)
        self.assertEqual(status_code, 201)

# pretty much all the code below is not running, not sure why yet

    def update_recipe(self):
        signup_response=self.client.post(
            '/auth/signup',
            json={
                "username":"testuser", 
                "email":"testuser@test.com", 
                "password":"password"
                }
        )
        login_response=self.client.post(
            'auth/login',
            json={
                "username":"testuser", 
                "password":"password"
            }
        )
        access_token=login_response.json["access_token"]
        

        create_recipe_response=self.client.put(
            '/recipe/recipes',

            json={
                "title": "Test Cookie",
                "description": "test description"
            },
            headers={
                "Authorization":f"Bearer {access_token}"
            }
        )

        status_code=create_recipe_response.status_code # I don't think we need this
        
        id=1
        update_response=self.client.put(
            f'/recipe/recipe/{id}',
            json={
                "title":"Test Cookie",
                "description":"test description1"
            },
            headers={
                "Authorization":f"Bearer {access_token}"
                }
        )
        # print(update_response)
        status_code=update_response.status_code
        print("Update get one recipe "f'{status_code}')
        self.assertEqual(status_code, 200)

    def delete_recipe(self):
        signup_response=self.client.post(
            '/auth/signup',
            json={
                "username":"testuser", 
                "email":"testuser@test.com", 
                "password":"password"
                }
        )
        login_response=self.client.post(
            'auth/login',
            json={
                "username":"testuser", 
                "password":"password"
            }
        )
        access_token=login_response.json["access_token"]

        create_recipe_response=self.client.post(
            '/recipe/recipes',

            json={
                "title": "Test Cookie",
                "description": "test description"
            },
            headers={
                "Authorization":f"Bearer {access_token}"
            }
        )
        id=1
        delete_response=self.client.delete(
            f'/recipe/recipe/{id}',
            headers={
                "Authorization":f"Bearer {access_token}"
                }

        )
        status_code=delete_response.status_code
        print(delete_response.json)
        self.assertEqual(status_code, 200)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all

if __name__=="__main__":
    unittest.main()
