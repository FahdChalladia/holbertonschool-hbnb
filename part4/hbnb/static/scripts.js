document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch('/api/v1/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/`;
                    window.location.href = '/places';
                } else {
                    alert('Login failed: Invalid email or password');
                }
            } catch (error) {
                alert('Login failed: Network error');
                console.error(error);
            }
        });
    }

    if (document.getElementById('place-details')) {
        initPlaceDetailsPage();
    }
    if (document.getElementById('places-list')) {
        checkAuthentication();
        document.getElementById('price-filter').addEventListener('change', handlePriceFilter);
    }
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function initPlaceDetailsPage() {
    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        alert('Place ID missing in URL');
        return;
    }

    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');
    if (token) {
        if (addReviewSection) addReviewSection.style.display = 'block';
        fetchPlaceDetails(token, placeId);
    } else {
        if (addReviewSection) addReviewSection.style.display = 'none';
        fetchPlaceDetails(null, placeId);
    }

    if (addReviewSection) {
        const reviewForm = document.getElementById('review-form');
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            await submitReview(token, placeId);
        });
    }
}

function getPlaceIdFromURL() {
    const pathParts = window.location.pathname.split('/');
    return pathParts[pathParts.length - 1];
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        const response = await fetch(`/api/v1/places/${placeId}`, { headers });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
            displayReviews(place.reviews || []);
        } else {
            alert('Failed to load place details');
            console.error('Error:', response.statusText);
        }
    } catch (error) {
        alert('Network error while fetching place details');
        console.error(error);
    }
}

async function displayPlaceDetails(place) {
    const detailsSection = document.getElementById('place-details');
    detailsSection.innerHTML = '';

    const title = document.createElement('h1');
    title.textContent = place.name || place.title || 'No Title';
    console.log(place)
    if (place.owner) {
    try {
        const response = await fetch(`/api/v1/users/${place.owner}`);

        if (response.ok) {
            const owner = await response.json();
            const fullName = `${owner.first_name || 'N/A'} ${owner.last_name || ''}`.trim();

            const host = document.createElement('p');
            host.textContent = `Host: ${fullName}`;
            detailsSection.appendChild(host);
            console.log('Host full name:', fullName);
        } else {
            const host = document.createElement('p');
            host.textContent = 'Host: Unknown';
            detailsSection.appendChild(host);
        }
    } catch (err) {
        const host = document.createElement('p');
        host.textContent = 'Host: Error loading host info';
        detailsSection.appendChild(host);
        console.error('Failed to fetch owner:', err);
    }       
}

    const description = document.createElement('p');
    description.textContent = place.description || 'No description available';

    const price = document.createElement('p');
    price.textContent = `Price: $${place.price_per_night || place.price || 'N/A'}/night`;

    // Amenities
    const amenities = document.createElement('div');
    amenities.innerHTML = '<h3>Amenities:</h3>';
    const ulAmenities = document.createElement('ul');
    if (place.amenities && place.amenities.length > 0) {
        place.amenities.forEach(amenity => {
            const li = document.createElement('li');
            li.textContent = amenity.name || amenity;
            ulAmenities.appendChild(li);
        });
    } else {
        ulAmenities.textContent = 'No amenities listed.';
    }
    amenities.appendChild(ulAmenities);
    detailsSection.appendChild(amenities);
}

async function displayReviews(reviews) {
    const reviewsSection = document.getElementById('reviews');
    reviewsSection.innerHTML = '<h3>Reviews:</h3>';

    if (reviews.length === 0) {
        reviewsSection.innerHTML += '<p>No reviews yet.</p>';
        return;
    }

    for (const review of reviews) {
        const reviewDiv = document.createElement('div');
        reviewDiv.className = 'review';

        let fullName = '';

        if (review.user_id) {
            try {
                const response = await fetch(`/api/v1/users/${review.user_id}`);
                if (response.ok) {
                    const user = await response.json();
                    fullName = `${user.first_name || ''} ${user.last_name || ''}`.trim();
                } else {
                    console.error(`User not found for ID: ${review.user_id}`);
                }
            } catch (err) {
                console.error('Failed to fetch user:', err);
            }
        }

        // Full name
        const reviewer = document.createElement('strong');
        reviewer.textContent = fullName;
        reviewDiv.appendChild(reviewer);

        // Rating
        if (review.rating !== undefined) {
            const rating = document.createElement('p');
            rating.textContent = `Rating: ${review.rating}`;
            reviewDiv.appendChild(rating);
        }

        // Review text
        const reviewText = document.createElement('p');
        reviewText.textContent = review.text || '';
        reviewDiv.appendChild(reviewText);

        reviewsSection.appendChild(reviewDiv);
    }
}

async function submitReview(token,placeId) {
  const rating= parseInt(document.getElementById('rating').value);
  const text = document.getElementById('review-text').value.trim();

  const response = await fetch("http://127.0.0.1:5000/api/v1/reviews", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({
      place_id: placeId,
      rating: rating,
      text: text
    })
  });

  if (!response.ok) {
    const error = await response.text();
    console.error('Error:', error);
  } else {
    const result = await response.json();
    console.log("Review posted successfully:", result);
  }
}
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.querySelector('a[href="/login"]');

    if (!token) {
        if (loginLink) loginLink.style.display = 'inline-block';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

async function fetchPlaces(token) {
    try {
        const response = await fetch('/api/v1/places', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            const data = await response.json();
            displayPlaces(data);
        } else {
            console.error('Failed to fetch places:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.setAttribute('data-price', place.price_per_night);

        placeCard.innerHTML = `
            <h2>${place.title || place.name}</h2>
            <p>Price: $${place.price_per_night || place.price}/night</p>
            <p>${place.description || ''}</p>
            <button class="details-button" onclick="window.location.href='/place/${place.id}'">View Details</button>

        `;

        placesList.appendChild(placeCard);
    });

}

function handlePriceFilter() {
    const selectedValue = document.getElementById('price-filter').value;
    const placeCards = document.querySelectorAll('.place-card');

    placeCards.forEach(card => {
        const price = parseFloat(card.getAttribute('data-price'));
        card.style.display = (selectedValue === 'all' || price <= parseFloat(selectedValue)) ? 'block' : 'none';
    });
}
