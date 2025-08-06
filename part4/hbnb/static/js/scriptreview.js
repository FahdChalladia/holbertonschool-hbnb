document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('place-details')) {
        initPlaceDetailsPage();
    }
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function getPlaceIdFromURL() {
    const pathParts = window.location.pathname.split('/');
    return pathParts[pathParts.length - 1];
}

function initPlaceDetailsPage() {
    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        alert('Place ID missing in URL');
        return;
    }

    const token = getCookie('token');
    const loginLink = document.querySelector('a[href="/login"]');
    const addReviewSection = document.getElementById('add-review');

    if (token) {
        if (addReviewSection) addReviewSection.style.display = 'block';
        if (loginLink) loginLink.style.display = 'none';
        fetchPlaceDetails(token, placeId);
    } else {
        if (loginLink) loginLink.style.display = 'inline-block';
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
    detailsSection.appendChild(title);

    if (place.owner) {
        try {
            const response = await fetch(`/api/v1/users/${place.owner}`);
            const host = document.createElement('p');

            if (response.ok) {
                const owner = await response.json();
                const fullName = `${owner.first_name || 'N/A'} ${owner.last_name || ''}`.trim();
                host.textContent = `Host: ${fullName}`;
            } else {
                host.textContent = 'Host: Unknown';
            }
            detailsSection.appendChild(host);
        } catch (err) {
            const host = document.createElement('p');
            host.textContent = 'Host: Error loading host info';
            detailsSection.appendChild(host);
            console.error('Failed to fetch owner:', err);
        }
    }

    const description = document.createElement('p');
    description.textContent = place.description || 'No description available';
    detailsSection.appendChild(description);

    const price = document.createElement('p');
    price.textContent = `Price: $${place.price_per_night || place.price || 'N/A'}/night`;
    detailsSection.appendChild(price);

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

        const reviewer = document.createElement('strong');
        reviewer.textContent = fullName;
        reviewDiv.appendChild(reviewer);

        if (review.rating !== undefined) {
            const rating = document.createElement('p');
            rating.textContent = `Rating: ${review.rating}`;
            reviewDiv.appendChild(rating);
        }

        const reviewText = document.createElement('p');
        reviewText.textContent = review.text || '';
        reviewDiv.appendChild(reviewText);

        reviewsSection.appendChild(reviewDiv);
    }
}

async function submitReview(token, placeId) {
    const rating = parseInt(document.getElementById('rating').value);
    const text = document.getElementById('review-text').value.trim();

    try {
        const response = await fetch('/api/v1/reviews', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ place_id: placeId, rating, text })
        });

        const contentType = response.headers.get('Content-Type');

        if (!response.ok) {
            let errorMessage = 'Unknown error occurred';

            if (contentType && contentType.includes('application/json')) {
                const errorData = await response.json();
                errorMessage = errorData.error || JSON.stringify(errorData);
            } else {
                errorMessage = await response.text();
            }

            alert(`Error ${response.status}: ${errorMessage}`);
            console.error('Error:', errorMessage);
        } else {
            const result = await response.json();
            alert('Review posted successfully!');
            location.reload();
        }
    } catch (error) {
        console.error('Network error while posting review:', error);
        alert('Network error while posting review');
    }
}
