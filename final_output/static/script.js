// Initialize the map
const map = L.map('map').setView([20, 0], 2); // Default center and zoom level

// Add a tile layer (OpenStreetMap)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Add a marker with a popup
let marker = null;

map.on('click', (e) => {
    const { lat, lng } = e.latlng;

    // Remove the previous marker if it exists
    if (marker) {
        map.removeLayer(marker);
    }

    // Add a new marker at the clicked location
    marker = L.marker([lat, lng]).addTo(map)
        .bindPopup(`Latitude: ${lat.toFixed(4)}, Longitude: ${lng.toFixed(4)}`)
        .openPopup();

    // Update the longitude and latitude input fields
    document.getElementById('latitude').value = lat.toFixed(4);
    document.getElementById('longitude').value = lng.toFixed(4);
});

// Theme Toggle
const themeSwitcher = document.getElementById('theme-switcher');
const body = document.body;

themeSwitcher.addEventListener('click', () => {
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    body.setAttribute('data-theme', newTheme);
    themeSwitcher.textContent = newTheme === 'dark' ? '🌓 Toggle Theme' : '🌞 Toggle Theme';
});