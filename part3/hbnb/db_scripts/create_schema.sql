DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS review;
DROP TABLE IF EXISTS place;
DROP TABLE IF EXISTS amenity;
DROP TABLE IF EXISTS user;

-- Table: user
CREATE TABLE user (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- Table: place
CREATE TABLE place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36),
    FOREIGN KEY (owner_id) REFERENCES user(id) ON DELETE CASCADE
);

-- Table: review
CREATE TABLE review (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    user_id CHAR(36),
    place_id CHAR(36),
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES place(id) ON DELETE CASCADE,
    UNIQUE (user_id, place_id)
);

-- Table: amenity
CREATE TABLE amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- Table: place_amenity (association table)
CREATE TABLE place_amenity (
    place_id CHAR(36),
    amenity_id CHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES place(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenity(id) ON DELETE CASCADE
);
