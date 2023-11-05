
console.log("script loaded");


// Select the form element
const form = document.getElementById('search');
const url= window.location.href;

// When the form is submitted
form.addEventListener('submit', function (event) {
  // Prevent the default form submit
  event.preventDefault();

  // Create FormData object from the form
  const formData = new FormData(form);

  // Use Fetch API to send the POST request with FormData
  fetch(`/${url}/search`, {
    method: 'POST',
    body: formData // FormData is automatically set as the body
    // No need to set 'Content-Type': 'multipart/form-data' header,
    // since the browser sets it automatically with the proper boundary
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok: ' + response.statusText);
    }
    return response.text(); // or response.json() if your server responds with JSON
  })
  .then(data => {
    console.log('Success:', data);
  })
  .catch(error => {
    console.error('There has been a problem with your fetch operation:', error);
  });
});