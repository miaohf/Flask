from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin
from sqlalchemy import event
from sqlalchemy import DDL



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# def _get_date():
#     return datetime.datetime.now()

# class Posts(Base):
#     #...
#     created_at = Column(Date, default=_get_date)
#     updated_at = Column(Date, onupdate=_get_date)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    last_login = db.Column(db.DateTime, default=datetime.now)
    login_ip = db.Column(db.String(60), nullable=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"




class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"



class Garden(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    coordinate = db.Column(db.Text, nullable=False)
    note = db.Column(db.String(200))
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now)
    

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"



class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    landlord_id = db.Column(db.Integer,  nullable=False)
    garden_id = db.Column(db.Integer,  nullable=False)
    address = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer,  nullable=False)
    pictures = db.Column(db.String(200),  nullable=False)
    area1 = db.Column(db.NUMERIC(8,2),  nullable=False)
    area2 = db.Column(db.NUMERIC(8,2),  nullable=False)
    cardid = db.Column(db.String(200), unique=True, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    note = db.Column(db.String(200))
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now)
    
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"



class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), unique=True, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    resource_id = db.Column(db.String(200),  nullable=False)
    area = db.Column(db.String(200),  nullable=False)
    pictures = db.Column(db.String(200), nullable=False)
    note = db.Column(db.String(200))
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now)
    

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"



class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    phone = db.Column(db.String(200), nullable=False)
    cardid = db.Column(db.String(200),  unique=True, nullable=False)
    pictures = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), unique=True, nullable=False)
    postcode = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(200))
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now)
    

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Landlord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    phone = db.Column(db.String(200), nullable=False)
    cardid = db.Column(db.String(200),  unique=True, nullable=False)
    pictures = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    note = db.Column(db.String(200))
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now)
    

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    bill_status = db.Column(db.Integer, nullable=False, default=0)
    customer_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    is_xuzu = db.Column(db.Integer, nullable=False, default=0)
    auction_date = db.Column(db.DateTime)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    house_id = db.Column(db.String(200), nullable=False)
    useof = db.Column(db.String(200), nullable=False)
    security_deposit = db.Column(db.Integer, nullable=False)
    annual_rent = db.Column(db.Integer, nullable=False)
    contract_pics = db.Column(db.String(200), nullable=False)
    approval_pics = db.Column(db.String(200), nullable=False)
    auction_announcement = db.Column(db.String(200), nullable=False)
    auction_confirmation = db.Column(db.String(200), nullable=False)
    origin_contract_id = db.Column(db.Integer, unique=True)
    note = db.Column(db.String(200))
    reason = db.Column(db.String(200))
    user_id = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now)
    

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"



class Contractype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    note = db.Column(db.String(200))
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now)
    

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Maintenanceunit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    phone = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    note = db.Column(db.String(200))
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now)
    

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Maintenancerec(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, nullable=False)
    maintenanceunit_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    note = db.Column(db.String(200))
    maintenance_note = db.Column(db.String(200))
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now)
    

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Contractbill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, nullable=False)
    contract_type = db.Column(db.Integer, nullable=False)
    contract_create = db.Column(db.DateTime, nullable=False)
    bill_sequence = db.Column(db.Integer, nullable=False)
    bill_date = db.Column(db.DateTime)
    bill_amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    opid = db.Column(db.Integer, nullable=False, default=0)
    note = db.Column(db.String(200))
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now)
    

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

event.listen(
    User.__table__, 
    "after_create", 
    DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 80100001;").execute_if(dialect=('postgresql', 'mysql'))
) 

event.listen(
    Post.__table__, 
    "after_create", 
    DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 80200001;").execute_if(dialect=('postgresql', 'mysql'))
) 

event.listen(
    Garden.__table__, 
    "after_create", 
    DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 80300001;").execute_if(dialect=('postgresql', 'mysql'))
) 

event.listen(
    Resource.__table__, 
    "after_create", 
    DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 80400001;").execute_if(dialect=('postgresql', 'mysql'))
) 

event.listen(
    House.__table__, 
    "after_create", 
    DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 80500001;").execute_if(dialect=('postgresql', 'mysql'))
) 

event.listen(
    Customer.__table__, 
    "after_create", 
    DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 80600001;").execute_if(dialect=('postgresql', 'mysql'))
) 

event.listen(
    Contract.__table__, 
    "after_create", 
    DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 80700001;").execute_if(dialect=('postgresql', 'mysql'))
) 

event.listen(
    Contractype.__table__, 
    "after_create", 
    DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 80800001;").execute_if(dialect=('postgresql', 'mysql'))
) 

event.listen(
    Maintenanceunit.__table__, 
    "after_create", 
    DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 80900001;").execute_if(dialect=('postgresql', 'mysql'))
) 

event.listen(
    Contractbill.__table__, 
    "after_create", 
    DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 81000001;").execute_if(dialect=('postgresql', 'mysql'))
) 

event.listen(
    Maintenancerec.__table__, 
    "after_create", 
    DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 81100001;").execute_if(dialect=('postgresql', 'mysql'))
) 
