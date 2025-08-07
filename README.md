# 🏠 HBnB Evolution

An AirBnB-like web application built with a layered architecture. HBnB allows users to register, list places, leave reviews, and manage amenities in a clean, scalable system.

## 🔧 Tech Stack
- Python (OOP, SOLID Principles)
- FlowChart for UML

## 📐 Architecture
- **Presentation Layer**: RESTful API endpoints for user interaction.
- **Business Logic Layer**: Core models and logic (User, Place, Review, Amenity).
- **Persistence Layer**: Data repositories and DB abstraction.

## 📄 Features
- ✅ User registration and profile management
- ✅ Place creation with geolocation
- ✅ Review system with ratings
- ✅ Amenity listing and association
- ✅ Modular, scalable architecture

## Project Structure

hbnb/
├── app/
│ ├── init.py # Flask app factory
│ ├── api/ # API endpoint modules (organized by version)
│ ├── models/ # Business entities (User, Place, Review, Amenity)
│ ├── services/ # Facade pattern implementation
│ ├── persistence/ # In-memory repository implementation
├── run.py # Application entry point
├── config.py # Configuration for different environments
├── requirements.txt # Python dependencies
├── README.md # Project documentation

## Business Logic Layer

This layer defines core entities and their relationships in the HBnB application:

### Entities
- `User`: Represents system users with fields like `first_name`, `email`, and `is_admin`.
- `Place`: Represents properties listed by users. Includes `title`, `description`, `price`, location, and relationships to reviews and amenities.
- `Review`: Users can leave reviews for places with `text`, `rating`, and references to the place and user.
- `Amenity`: Features like "Wi-Fi", "Pool", etc.

### Common Features
- All classes inherit from `BaseModel`, which includes:
  - `id`: UUID
  - `created_at` and `updated_at` timestamps
  - `save()` to update `updated_at`
  - `update(data_dict)` to apply multiple updates at once

### Relationships
- A `User` can own multiple `Places`
- A `Place` can have many `Reviews` and `Amenities`
- A `Review` is linked to a single `Place` and `User`

### Example Usage
```python
user = User("Jane", "Doe", "jane@example.com")
place = Place("Seaside House", "Lovely ocean view", 150, 36.0, -120.0, user)
amenity = Amenity("Hot Tub")
place.add_amenity(amenity)
review = Review("Perfect getaway!", 5, place, user)
place.add_review(review)
```
### Project Vision and Scope

Implement the Presentation Layer using Flask and flask-restx to create RESTful API endpoints.

Develop the Business Logic Layer with core classes and relationships.

Use the Facade pattern to simplify interaction between layers.

Implement CRUD operations for Users, Places, Reviews, and Amenities (with some limitations on DELETE).

Handle data serialization to include related object attributes (e.g., owner details in Place responses).

Focus on core functionality only; authentication and role-based access control will be added in Part 3.

###Objectives

Project Setup: Organize a modular project structure for Presentation, Business Logic, and Persistence layers.

Business Logic Implementation: Create classes for User, Place, Review, and Amenity with attributes, methods, and relationships.

API Development: Build RESTful endpoints for core entities using Flask-restx, including input validation and response formatting.

Testing & Validation: Ensure endpoints handle expected and edge cases correctly using cURL, Postman, and automated tests.

Documentation: Leverage Flask-restx to auto-generate Swagger UI documentation.

###Tasks Summary

0. Project Setup and Package Initialization
Set up modular folders and packages for Presentation, Business Logic, and Persistence.

Implement an in-memory repository to simulate data storage

Prepare for Facade pattern integration.

1. Core Business Logic Classes
Implement core entities: User, Place, Review, Amenity.

Define attributes, methods, and entity relationships.

Support data validation and integrity.

2. User Endpoints
Implement POST (create), GET (list and by ID), and PUT (update) for users.

Exclude password from responses.

No DELETE operation yet.

3. Amenity Endpoints
Implement POST, GET, and PUT endpoints for amenities.

No DELETE operation yet.

Follow patterns established in User endpoints.

4. Place Endpoints
Implement POST, GET, and PUT endpoints for places.

Handle relationships with User (owner) and Amenity.

Validate attributes such as price, latitude, longitude.

No DELETE operation yet.

5. Review Endpoints
Implement full CRUD operations including DELETE.

Associate reviews with both User and Place.

Update Place endpoints to include reviews.

6. Testing and Validation
Add validation for input data on all endpoints.

Perform manual testing with cURL and Swagger UI.

Create and run automated tests with unittest or pytest.

Document test results, including edge cases.

###Technologies & Tools

Python 3

Flask

Flask-RESTx (for API and Swagger documentation)

UUID (for unique identifiers)

cURL/Postman (for API testing)

unittest/pytest (for automated testing)




## Authors :black_nib:
* **Fahd Challadia** <[FahdChalladia](https://github.com/FahdChalladia)>
* **Yassine khouzemi** <[yaskho](https://github.com/yaskho)>   
