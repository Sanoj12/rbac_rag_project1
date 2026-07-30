from application.database import db
from application.auth.hashing import hashing_password



admin_email = "admin5@gmail.com"
admin_password = "admin5"

existing_admin = db.query(User).filter(User.email == admin_email).first()

if existing_admin:
    print("admin already exists")

else:
    admin = User(
        email = admin_email,
        password = hashing_password(admin_password),
        department = "admin"
    )


    db.add(admin)
    db.commit()

    print("admin added successfully")
