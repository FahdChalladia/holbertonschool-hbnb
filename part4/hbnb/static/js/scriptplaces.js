if (document.getElementById('places-list')) 
{
    document.addEventListener('DOMContentLoaded', () => 
    {
        checkAuthentication();
        document.getElementById('price-filter').addEventListener('change', handlePriceFilter);
    });
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.querySelector('a[href="/login"]');

    if (!token) {
        if (loginLink) loginLink.style.display = 'inline-block';
    } else {
        if (loginLink) loginLink.style.display = 'none';
    }

    fetchPlaces(token);
}

async function fetchPlaces(token) {
    try {
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch('/api/v1/places', {
            method: 'GET',
            headers: headers
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
        placeCard.setAttribute('data-price', place.price);

        placeCard.innerHTML = `
            <h2>${place.title || place.name}</h2>
            <p>Price: $${place.price_per_night || place.price}/night</p>
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
