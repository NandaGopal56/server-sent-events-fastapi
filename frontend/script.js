const coordinatesElement = document.getElementById('coordinates');
let coords;

// Create EventSource for SSE endpoint
const eventSource = new EventSource('http://127.0.0.1:8000/get-waypoints');

eventSource.onopen = () => {
    console.log('EventSource connected')
    //Everytime the connection gets extablished clearing the previous data from UI
    coordinatesElement.innerText = ''
}

//eventSource can have event listeners based on the type of event.
//Bydefault for message type of event it have the onmessage method which can be used directly or this same can be achieved through explicit eventlisteners
eventSource.addEventListener('locationUpdate', function (event) {
    coords = JSON.parse(event.data);
    console.log('LocationUpdate', coords);
    updateCoordinates(coords)
});

//In case of any error, if eventSource is not closed explicitely then client will retry the connection a new call to backend will happen and the cycle will go on.
eventSource.onerror = (error) => {
    console.error('EventSource failed', error)
    // eventSource.close()
}

// Function to update and display coordinates
function updateCoordinates(coordinates) {
    // Create a new paragraph element for each coordinate and append it
    const paragraph = document.createElement('p');
    paragraph.textContent = `Latitude: ${coordinates.lat}, Longitude: ${coordinates.lng}`;
    coordinatesElement.appendChild(paragraph);
}