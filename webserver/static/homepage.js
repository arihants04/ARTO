
console.log("script loaded");

function getColor(value) {
    let color;
    if (value >= 90) {
        color = '#00FF00';
    } else if (value >= 80) {
        color = '#33FF33';
    } else if (value >= 70) {
        color = '#66FF66';
    } else if (value >= 60) {
        color = '#99FF99';
    } else if (value >= 50) {
        color = '#CCFFCC';
    } else if (value >= 40) {
        color = '#FFCCCC';
    } else if (value >= 30) {
        color = '#FF9999';
    } else if (value >= 20) {
        color = '#FF6666';
    } else if (value >= 10) {
        color = '#FF3333';
    } else {
        color = '#FF0000';
    }
    return color;
}


const ctx = document.getElementById('myChart');
var data = {
            value: 50,
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
                    backgroundColor: [ getColor(data.value), '#0f0e17'],
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
                    animateScale: true
                },
                title: {
                    display: false,
                    text: data.label,
                    fontSize: 16
                },
                plugins:{
                  legend: false,
                  title: false,
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

  const val = document.getElementById("default-search").value

  // Use Fetch API to send the POST request with FormData
  fetch(`/search`, {
    method: 'POST',
    body: JSON.stringify({  
        'key' : val
    }),
    headers: {
      "Content-Type": "application/json",
      // 'Content-Type': 'application/x-www-form-urlencoded',
    }
// FormData is automatically set as the body
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
    //console.log('Success:', data);
    document.querySelector("body").classList.remove('overflow-y-hidden');
    document.getElementById("main-content").classList.remove('mt-40');
    document.getElementById("blurb").classList.add('scale-0');
    document.getElementById("blurb").style.marginBottom = `-${blurb.offsetHeight}px`;
    document.getElementById("info").classList.remove('hidden');
    document.getElementById("description").classList.remove('hidden');
    document.getElementById("summary").classList.remove('hidden');
    if (val.toUpperCase() == "NVDA"){
        console.log("NVDA");
        console.log(typeof(data));
        data = JSON.parse(data);

        document.getElementById("description-title").innerHTML = val.toUpperCase();
        document.getElementById("description-text-o").innerHTML = "Opening price: $"+data["stock_info"][0].toFixed(2);
        document.getElementById("description-text-h").innerHTML = "Highest price: $"+data["stock_info"][1].toFixed(2);
        document.getElementById("description-text-l").innerHTML = "Lowest price: $"+data["stock_info"][2].toFixed(2);
        document.getElementById("description-text-c").innerHTML = "Closing price: $"+data["stock_info"][3].toFixed(2);
        
    }
    
    setTimeout(()=>{
      document.getElementById("blurb").classList.add("hidden");
    }, 500)
  })
  .catch(error => {
    console.error('There has been a problem with your fetch operation:', error);
  });
});
