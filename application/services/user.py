from application.database.db import Session, User
from application.auth.hashing import (
    hashing_password,
    verify_password
)

from sqlalchemy.exc import IntegrityError


# =========================================================
# ADD USER
# =========================================================

def add_user(
    name,
    email,
    password,
    department
):

    session = Session()

    try:

        # -------------------------------------------------
        # Check whether email already exists
        # -------------------------------------------------

        existing_user = session.query(User).filter(
            User.email == email
        ).first()

        if existing_user:

            return {
                "error": "Email already exists"
            }

        # -------------------------------------------------
        # Hash password
        # -------------------------------------------------

        hashed_password = hashing_password(
            password
        )

        # -------------------------------------------------
        # Create user
        # -------------------------------------------------

        user = User(
            name=name,
            email=email,
            password=hashed_password,
            department=department
        )

        session.add(user)

        session.commit()

        session.refresh(user)

        print(
            "USER ADDED:",
            user.email,
            user.department
        )

        return {
            "message": "User created successfully",
            "name": user.name,
            "email": user.email,
            "department": user.department
        }

    except IntegrityError as e:

        session.rollback()

        print(
            "DATABASE ERROR:",
            repr(e)
        )

        return {
            "error": "Email already exists"
        }

    except Exception as e:

        session.rollback()

        print(
            "ADD USER ERROR:",
            repr(e)
        )

        return {
            "error": str(e)
        }

    finally:

        session.close()


# =========================================================
# LOGIN
# =========================================================

def login(
    email,
    password
):

    session = Session()

    try:

        # -------------------------------------------------
        # Find user
        # -------------------------------------------------

        user = session.query(User).filter(
            User.email == email
        ).first()

        # -------------------------------------------------
        # User doesn't exist
        # -------------------------------------------------

        if not user:

            print(
                "USER DOES NOT EXIST"
            )

            return None

        # -------------------------------------------------
        # Verify password
        # -------------------------------------------------

        if verify_password(
            password,
            user.password
        ):

            print(
                "LOGIN SUCCESS:",
                user.email,
                user.department
            )

            return user

        # -------------------------------------------------
        # Wrong password
        # -------------------------------------------------

        print(
            "INVALID PASSWORD"
        )

        return None

    except Exception as e:

        print(
            "LOGIN ERROR:",
            repr(e)
        )

        return None

    finally:

        session.close()