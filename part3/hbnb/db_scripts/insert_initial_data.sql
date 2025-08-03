-- Admin user
INSERT INTO user (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$tWDbV1D7Z7J7FSD8IwW/OuTTzA9gxvljmncX8msTZaC7n6R7Z8CuS',
    TRUE
);

-- Amenities
INSERT INTO amenity (id, name) VALUES ('8f5b8b01-63b4-47d0-9a8f-a8e1981e2df6', 'WiFi');
INSERT INTO amenity (id, name) VALUES ('77cbe8c6-bc1e-4e38-999b-4c16966b3c45', 'Swimming Pool');
INSERT INTO amenity (id, name) VALUES ('ea91337e-4aef-4892-bf7e-678d1ff53c77', 'Air Conditioning');
