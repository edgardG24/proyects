 
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI =  "postgres://tyiuqokgzyrbem:7a906139c3b520dab15e6f603d3ff0c40f7b88d313d1db6cd4f603a04961c0b3@ec2-34-195-115-225.compute-1.amazonaws.com:5432/d3qgi53uaj1knr"  #'sqlite:///site.db' 
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'mypythonwebsv@gmail.com'#os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = '@skarl3t1sent@'#os.environ.get('EMAIL_PASS')