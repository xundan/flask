from models import db, Record
db.create_all()
# admin = User('admin1', 'admin1@example.com')
# guest = User('guest', 'guest@example.com')
# db.session.add(admin)
# db.session.add(guest)
# db.session.commit()
records = Record.query.all()
one = Record.query.filter_by(id=1).first()
print one