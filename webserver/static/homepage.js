// document.addEventListener('DOMContentLoaded', function() {
//   // Get the form by its ID
//   var searchForm = document.getElementById('search');

//   // Add a submit event listener to the form
//   searchForm.addEventListener('submit', function(event) {
//     print();
//     // Prevent the default form submission
//     event.preventDefault();   

//     // Get the search query from the form input with ID 'search'
//     var searchQuery = document.getElementById("default-search").value;

//     // Change the current page location to include the query
//     document.location.href = `/search?s=${encodeURIComponent(searchQuery)}`;

//     // // Send a POST request to the server
//     // fetch('/search', {
//     //   method: 'POST',
//     //   headers: {
//     //     'Content-Type': 'application/x-www-form-urlencoded',
//     //   },
//     //   body: `q=${encodeURIComponent(searchQuery)}`,
//     // })
//     // .then(response => response.json())
//     // .then(data => {
//     //   console.log('Success:', data);
//     //   // Handle the response data
//     // })
//     // .catch((error) => {
//     //   console.error('Error:', error);
//     // });
//   });
// });
