HBnB Backend API PART 3 - Project Documentation:

📌 Overview

HBnB is a RESTful backend API that powers a booking platform similar to Airbnb. It provides functionality for managing users, places, reviews, and amenities. This documentation covers core backend logic, including user authentication using JWT, admin-level access control, SQLAlchemy model relationships, and database schema visualization.

🔐 JWT Authentication

The application uses JWT (JSON Web Token) for secure authentication.

✅ Features:

Token-based login

Authenticated routes

Admin-only access for certain endpoints

🔧 Implementation:

JWT is generated upon login.

Authorization: Bearer <token> must be included in headers for protected routes.

Token includes user ID and is_admin claims.

🧑‍💻 Admin Privileges

Admin users have elevated access rights:

🔐 Admin-Only Actions:

Create/update/delete any user

Add/update amenities

Access all places and reviews, regardless of ownership

🔑 Creating an Admin:

Use hashed password and SQL insert manually or via script:

INSERT INTO user (id, first_name, last_name, email, password, is_admin)
VALUES (
  '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
  'Admin',
  'HBnB',
  'admin@hbnb.io',
  '$2b$12$tWDbV1D7Z7J7FSD8IwW/OuTTzA9gxvljmncX8msTZaC7n6R7Z8CuS',
  TRUE
);

To generate the hash:

import bcrypt
password = b"admin1234"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed.decode())

🗃️ Entities and SQLAlchemy Models

The following entities are defined with SQLAlchemy:

User

id (UUID, PK)

first_name (String)

last_name (String)

email (String, unique)

password (String, hashed)

is_admin (Boolean)

Place

id (UUID, PK)

title (String)

description (Text)

price (Float)

latitude (Float)

longitude (Float)

owner_id (FK → User)

Review

id (UUID, PK)

text (Text)

rating (Integer: 1-5)

user_id (FK → User)

place_id (FK → Place)

Amenity

id (UUID, PK)

name (String, unique)

PlaceAmenity

place_id (FK → Place)

amenity_id (FK → Amenity)

Composite PK: (place_id, amenity_id)

🔗 Mapping Relationships Between Entities (SQLAlchemy)

Relationships Overview

User → Places: One-to-Many

User → Reviews: One-to-Many

Place → Reviews: One-to-Many

Place → Amenities: Many-to-Many

Review → Place/User: Many-to-One

Example: User Model

class User(Base):
    __tablename__ = 'user'
    id = Column(String(36), primary_key=True)
    ...
    places = relationship("Place", back_populates="owner", cascade="all, delete")
    reviews = relationship("Review", back_populates="user", cascade="all, delete")

Place Model

class Place(Base):
    __tablename__ = 'place'
    id = Column(String(36), primary_key=True)
    ...
    owner_id = Column(String(36), ForeignKey('user.id'))
    owner = relationship("User", back_populates="places")
    reviews = relationship("Review", back_populates="place", cascade="all, delete")
    amenities = relationship("Amenity", secondary="place_amenity", back_populates="places")

Review Model

class Review(Base):
    __tablename__ = 'review'
    id = Column(String(36), primary_key=True)
    ...
    user_id = Column(String(36), ForeignKey('user.id'))
    place_id = Column(String(36), ForeignKey('place.id'))
    user = relationship("User", back_populates="reviews")
    place = relationship("Place", back_populates="reviews")

Amenity Model

class Amenity(Base):
    __tablename__ = 'amenity'
    id = Column(String(36), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    places = relationship("Place", secondary="place_amenity", back_populates="amenities")

Join Table

class PlaceAmenity(Base):
    __tablename__ = 'place_amenity'
    place_id = Column(String(36), ForeignKey('place.id'), primary_key=True)
    amenity_id = Column(String(36), ForeignKey('amenity.id'), primary_key=True)

🗄️ Database SQL Scripts

SQL files were used to:

Create tables with constraints

Insert initial admin and amenity data

Files:

create_schema.sql

insert_initial_data.sql

To execute:

sqlite3 hbnb.db
.read db_scripts/create_schema.sql
.read db_scripts/insert_initial_data.sql

🧪 Testing SQL Scripts

sqlite3 hbnb.db
sqlite> .read db_scripts/create_schema.sql
sqlite> .read db_scripts/insert_initial_data.sql

Verify table creation using .tables and PRAGMA table_info(table_name);

Run CRUD operations with SELECT, INSERT, etc.

🆔 UUID Generation

To generate UUIDs:

import uuid
print(str(uuid.uuid4()))

📈 ER Diagram (Mermaid.js)

erDiagram
    USER {
        CHAR id PK
        VARCHAR first_name
        VARCHAR last_name
        VARCHAR email
        VARCHAR password
        boolean is_admin
    }

    PLACE {
        CHAR id PK
        VARCHAR title
        TEXT description
        DECIMAL price
        FLOAT latitude
        FLOAT longitude
        CHAR owner_id FK
    }

    REVIEW {
        CHAR id PK
        TEXT text
        INT rating
        CHAR user_id FK
        CHAR place_id FK
    }

    AMENITY {
        CHAR id PK
        VARCHAR name
    }

    PLACE_AMENITY {
        CHAR place_id FK
        CHAR amenity_id FK
    }

    USER ||--o{ PLACE : owns
    USER ||--o{ REVIEW : writes
    PLACE ||--o{ REVIEW : receives
    PLACE ||--o{ PLACE_AMENITY : has
    AMENITY ||--o{ PLACE_AMENITY : includes


✅ Conclusion

This documentation covers key backend features of the HBnB project: JWT authentication, admin access, SQLAlchemy models with relationships, raw SQL scripts for schema setup, and an ER diagram. Together, they define all a robust backend system.