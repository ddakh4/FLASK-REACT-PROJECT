from exts import db

#reservation model
"""
class Reservation:
     id: int primary key
     customer_name: str
     date: date
     time: time
     table_id: int foreign key

"""

class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String(30), nullable = False)
    time = db.Column(db.String(30), nullable = False)
    guests = db.Column(db.Integer, nullable = False)
    occasion = db.Column(db.String(30), nullable = False)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id', name='reservation_table_fk'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='reservation_table_fk'))

    def __repr__(self):
        return f"<Reservation {self.id} >"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
         reservations = db.session.query(
         Reservation.id, Reservation.date, Reservation.time, 
         Reservation.guests, Reservation.occasion, Reservation.table_id,
         User.fullname.label('user_name'), User.phone.label('phone')
         ).join(User).all()
         return [{'id': r.id, 'date': r.date, 'time': r.time, 
             'guests': r.guests, 'occasion': r.occasion, 
             'table_id': r.table_id, 'user_name': r.user_name, 'phone': r.phone} for r in reservations]


#table model
"""
class Table:
     id: int primary key
     capacity: int
     availability: boolean
"""

class Table(db.Model):
    __tablename__ = 'table'
    id = db.Column(db.Integer, primary_key = True)
    capacity = db.Column(db.Integer, nullable = False)
    availability = db.Column(db.Boolean, nullable = False, default=True)
    reservations = db.relationship('Reservation', backref='table')

    def __repr__(self):
        return f"<Table {self.id} >"

    @staticmethod
    def get_available_tables(date, time, guests):
        # get all tables that are available at the given date and time
        available_tables = Table.query.filter(Table.availability == True).filter(~Table.reservations.any(
            (Reservation.date == date) &
            (Reservation.time == time)
        )).filter(Table.capacity >= guests).all()

        return available_tables


#user model
"""
class User:
id: integer,
username: string,
email: string,
password: string,
fist_name: string,
last_name: string
"""

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(25), nullable = False)
    username = db.Column(db.String(25), nullable = False, unique = True)
    phone = db.Column(db.String(20), nullable = False)
    password = db.Column(db.Text(), nullable = False)
    reservations = db.relationship('Reservation', backref='user')

    def __init__(self, fullname, username, phone, password):
        self.fullname = fullname
        self.username = username
        self.phone = phone
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"

    def save(self):
        db.session.add(self)
        db.session.commit()