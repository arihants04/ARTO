
console.log("script loaded");

const ctx = document.getElementById('myChart');
var data = {
            value: 100,
            max: 100,
            label: "Sentiment"
        };

        // Chart.js chart's configuration
        // We are using a Doughnut type chart to 
        // get a Gauge format chart 
        // This is approach is fine and actually flexible
        // to get beautiful Gauge charts out of it
        var config = {
            type: 'doughnut',
            data: {
                labels: [data.label],
                datasets: [{
                    data: [data.value, data.max - data.value],
                    backgroundColor: [ data.value>=50 ?'#c3f0ca': '#f25042', '#0f0e17'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutoutPercentage: 85,
                rotation: -90,
                circumference: 180,
                tooltips: {
                    enabled: false
                },
                legend: {
                    display: false
                },
                animation: {
                    animateRotate: true,
                    animateScale: false
                },
                title: {
                    display: true,
                    text: data.label,
                    fontSize: 16
                }
            }
        };

        // Create the chart
        var gaugeChart = new Chart(ctx, config);


// Select the form element
const form = document.getElementById('search');
const url= window.location.href;

// When the form is submitted
form.addEventListener('submit', function (event) {
  // Prevent the default form submit
  event.preventDefault();

  // Create FormData object from the form
  const formData = new FormData(form);
  console.log(formData);
  // Use Fetch API to send the POST request with FormData
  fetch(`/search`, {
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
    document.getElementById("main-content").classList.remove('mt-40');
    document.getElementById("blurb").classList.add('scale-0');
    document.getElementById("blurb").style.marginBottom = `-${blurb.offsetHeight}px`;
    document.getElementById("info").classList.remove('hidden');
    
    setTimeout(()=>{
      document.getElementById("blurb").classList.add("hidden");
    }, 500)
  })
  .catch(error => {
    console.error('There has been a problem with your fetch operation:', error);
  });
});