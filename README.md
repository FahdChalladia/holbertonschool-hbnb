HBnB Project
📌 Overview
HBnB is a full-stack booking platform inspired by Airbnb.

Backend: RESTful API managing users, places, reviews, amenities with secure JWT authentication and admin control.

Frontend: React-based client interface for browsing, booking, and managing listings.

Backend API (Parts 2 & 3)
Features
User authentication & authorization with JWT

Admin role with elevated privileges

CRUD operations on Users, Places, Reviews, Amenities

SQLAlchemy ORM models with well-defined relationships

SQLite database with schema setup and initial data

Comprehensive API endpoints with input validation and error handling

Backend Architecture
Models and Relationships
User: UUID, first_name, last_name, email (unique), hashed password, is_admin

Place: UUID, title, description, price, coordinates, owner (User)

Review: UUID, text, rating (1-5), user (author), place (target)

Amenity: UUID, unique name

PlaceAmenity: Association table linking places and amenities (many-to-many)

Relationships
User → Places (one-to-many)

User → Reviews (one-to-many)

Place → Reviews (one-to-many)

Place → Amenities (many-to-many via PlaceAmenity)

Authentication & Admin Control
JWT tokens issued at login, containing user id and admin status

Protected routes require Authorization: Bearer <token>

Admin-only endpoints for managing users, amenities, and viewing all data

Passwords stored hashed using bcrypt

Admin user creation example provided with password hashing snippet

Database Setup
SQL scripts to create tables and insert initial data (create_schema.sql, insert_initial_data.sql)

Run using sqlite3 CLI

UUID generation utility provided for unique IDs

API Endpoints
User registration and login

Place listing, creation, update, deletion

Review management linked to users and places

Amenity management (admin only)

Query filters and pagination for listings

ER Diagram
mermaid

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
Frontend Application (Part 4)
Overview
The frontend is a React-based single page application that interfaces with the HBnB backend API to provide a rich user experience:

User registration and login with JWT authentication

Browse, filter, and search listings of places

View place details, amenities, and reviews

Submit reviews and manage bookings

Admin dashboard for managing users, places, amenities, and reviews

Responsive design and client-side routing

Features
Authentication: Login form stores JWT, protects routes client-side

Listings Page: Display places with filtering by price, amenities, location

Place Details: Detailed info with reviews and amenities

Review Submission: Authenticated users can add/edit/delete reviews

Admin Panel: Manage users, places, and amenities with elevated rights

State Management: Uses React Context or Redux for global state

Error Handling: User-friendly error messages on failed requests

Testing: Frontend unit tests for components and integration with backend mocks

Tech Stack
React + React Router for SPA routing

Axios or Fetch API for HTTP requests to backend

JWT stored in localStorage or secure HTTP-only cookies

CSS Modules / Styled Components / Tailwind CSS for styling (depending on implementation)

Running the Frontend
Install dependencies: npm install or yarn

Configure backend API URL in environment variables

Start development server: npm start

Build for production: npm run build

Getting Started
Setup Backend

Run SQL scripts to create schema and insert data.

Install Python dependencies (flask, sqlalchemy, bcrypt, pyjwt, etc.).

Run backend server.

Setup Frontend

Install frontend dependencies.

Set backend API URL.

Run frontend server.

Useful Commands
Backend
bash

sqlite3 hbnb.db
.read db_scripts/create_schema.sql
.read db_scripts/insert_initial_data.sql
python run.py  # or equivalent command to start backend
Frontend
bash

npm install
npm start
Additional Resources
Password Hashing Example

python

import bcrypt
password = b"admin1234"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed.decode())
UUID Generation

python

import uuid
print(str(uuid.uuid4()))