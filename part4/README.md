Part 4 - Simple Web Client
Overview
This part of the project focuses on building a front-end web client that interacts with your back-end API. Using HTML5, CSS3, and JavaScript ES6, you will develop an interactive, user-friendly interface for managing places and reviews.

The web client features include:

User authentication with JWT token management

Displaying a list of places with client-side filtering

Viewing detailed information of a place including reviews

Adding new reviews (authenticated users only)

Seamless interaction with back-end API using Fetch API

Features
1. Login Page
Allows users to log in with email and password.

Sends credentials to the API via POST request.

Stores the returned JWT token in cookies for session management.

Redirects authenticated users to the main page.

Displays errors for failed login attempts.

2. List of Places (Main Page)
Fetches the list of places from the API.

Displays places as cards including name, price, and a “View Details” button.

Implements client-side filtering by price range.

Shows or hides login link based on user authentication status.

3. Place Details Page
Fetches and displays detailed information for a selected place.

Shows amenities, host info, description, price, and reviews.

Displays a form to add a new review for authenticated users.

4. Add Review Page
Allows authenticated users to submit reviews for a place.

Redirects unauthenticated users to the main page.

Sends review data to the API and handles success/error feedback.

Technologies Used
HTML5: Semantic page structure for accessibility and SEO.

CSS3: Styling with responsive design principles.

JavaScript (ES6): Client-side scripting for API interaction and dynamic UI updates.

Fetch API: AJAX requests to communicate with back-end API.

Cookies: JWT token storage for session management.

Setup & Usage
Prerequisites
A running back-end API (from previous parts of the project) that supports:

User login (returns JWT token)

Fetching places list and details

Submitting reviews

Web server or simple HTTP server to serve static HTML/CSS/JS files.

Installation
Clone the repository or download the part4 directory.

Place the files in your web server’s root directory (e.g., htdocs or public folder).

Ensure the API URL is correctly set in your JavaScript code (scripts.js) for AJAX requests.

Running the Application
Open login.html in your browser to sign in.

After login, you will be redirected to index.html where you can browse places.

Click “View Details” on a place card to see more information.

If logged in, you can add reviews on the place details page.

Project Structure
part4/
│
├── index.html          # Main page listing places
├── login.html          # User login page
├── place.html          # Place details page
├── add_review.html     # Form to add a review
├── styles.css          # CSS styles
├── scripts.js          # JavaScript for API calls and UI logic
├── logo.png            # Application logo
└── icon.png            # Favicon
Important Notes
The client handles CORS by ensuring the API allows requests from the client origin.

JWT token is stored in a cookie with path / for session persistence.

All forms use client-side validation for better UX.

The design follows provided specifications with semantic HTML and accessibility in mind.

Resources
HTML5 Documentation

CSS3 Documentation

JavaScript ES6 Features

Fetch API
