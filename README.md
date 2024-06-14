## AppIARY
*Bee Smart!*

AppIARY is my portfolio project for the ALX SE course. It is a web application that bee farmers can use to manage apiary operations in a smarter way.

You can use Appiary to manage beehives, perform inspections on beehives and record observations, schedule harvests, record harvests, and add or remove beehives.

### Features
- User authentication using JWT tokens.
- CRUD operations for managing apiaries, beehives, inspections, and harvests.
- Role-based access control (to be implemented).
- API endpoints --some are protect with jwt tokens
- Swagger documentation for API endpoints.
- Responsive web interface with a landing page, key feature sections, and an about section.

### Technologies
- Flask
- SQLAlchemy
- MYSQL
- Jinja
- HTML & CSS
- JWT tokens

### Project Structure
```
Appiary/
  |
  |--decorators.py
  |
  |--requirements.txt
  |
  |--docs/
  |
  |--models/
  |    |
  |    |--engine/ 
  |    |    |--__init__.py, db_storag.py, file_storage.py
  |    |
  |    |--__init__.py basemodel.py, beehive.py, harvest.py, inspection.py, harvest.py
  |
  |--api/
  |   |
  |   |--v1
  |      |
  |      |--app.py
  |      |
  |      |--auth/
  |      |
  |      |--views/
  |
  |
  |--web/
  |   |
  |   |--app.py
  |   |--__init__.py
  |   |
  |   |--templates/
  |   |
  |   |--static/
  |   |
  |   |--views/
    
```
### Installation
#### Prerequisites
- Python 3.8+
- pip
- MySQL


#### Step 1: Setup a virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

#### Step 2: Install the dependencies inside the requirements.txt
`pip install -r requirements.txt`

#### Step 3: Set environment variables
Set these environment variables for API
```
export APPIARY_MYSQL_USER='appiary_db_user'
export APPIARY_MYSQL_PWD='appiary_db_user_pwd'
export APPIARY_MYSQL_HOST='localhost'
export APPIARY_MYSQL_DB='appiary_db'
export APPIARY_ENV='test' #optional if you want to clean the database
export APPIARY_TYPE_STORAGE='db'
export SECRET_KEY='appiary_api'
export APPIARY_API_HOST='0.0.0.0'
export APPIARY_API_PORT='5000'
export DEBUG='True'
```
Set these environment variables for Web App
```
export APPIARY_MYSQL_USER='appiary_db_user'
export APPIARY_MYSQL_PWD='appiary_db_user_pwd'
export APPIARY_MYSQL_HOST='localhost'
export APPIARY_MYSQL_DB='appiary_db'
export APPIARY_ENV='test' <!-- optional if you want to clean the database -->
export APPIARY_TYPE_STORAGE='db'
export SECRET_KEY='appiary_web' <!-- or whatever key you want -->
export API_URL='http://127.0.0.1:5000/api/v1/stats'
export APPIARY_API_HOST='0.0.0.0'
export APPIARY_API_PORT='5050'
export DEBUG_STATUS='True'
```
### Usage
#### 1. Initialize the database
```
cat appiary_db_setup.sql | sudo mysql -uroot -p
```

#### 2. Run the flask application
##### API
`python3 -m api.v1.app`

Access API at: http://127.0.0.1:5000

##### Web
`python3 -m web.app
Access Web APp at: http://127.0.0.1:5050

### Future Enhancements
- Implement role-based access control.
- Add more detailed API documentation.
- Improve the user interface and add more features.

### License
This project is licensed under the MIT License.

### Acknowledgements
- Flask Documentation
- SQLAlchemy Documentation
- Swagger Documentation
- TechWithTim YouTube  Flask Series: [https://www.youtube.com/@TechWithTim](https://www.youtube.com/@TechWithTim)
