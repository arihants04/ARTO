
console.log("script loaded");

const ctx = document.getElementById('myChart');
var ctxData = {
            value: 20,
            max: 100,
            label: "Sentiment"
        };

        // Chart.js chart's configuration
        // We are using a Doughnut type chart to 
        // get a Gauge format chart 
        // This is approach is fine and actually flexible
        // to get beautiful Gauge charts out of it
        
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

    console.log('Success:', data);
    document.querySelector("body").classList.remove('overflow-y-hidden');
    document.getElementById("main-content").classList.remove('mt-40');
    document.getElementById("blurb").classList.add('scale-0');
    document.getElementById("blurb").style.marginBottom = `-${blurb.offsetHeight}px`;
    document.getElementById("info").classList.remove('hidden');
    document.getElementById("description").classList.remove('hidden');
    document.getElementById("summary").classList.remove('hidden');
    data = JSON.parse(data);
    document.getElementById("description-title").innerHTML = val.toUpperCase();
    document.getElementById("description-text-o").innerHTML = "Opening price: $"+data["stock_info"][0].toFixed(2);
    document.getElementById("description-text-h").innerHTML = "Highest price: $"+data["stock_info"][1].toFixed(2);
    document.getElementById("description-text-l").innerHTML = "Lowest price: $"+data["stock_info"][2].toFixed(2);
    document.getElementById("description-text-c").innerHTML = "Closing price: $"+data["stock_info"][3].toFixed(2);
    document.getElementById("hist").src = "../static/"+val.toLowerCase() + "Hist.png";
    document.getElementById("big3").src = "../static/"+val.toLowerCase() + "Big3.png";
    document.getElementById("regression").innerHTML = "Predicted Value: "+data["regression_prediction"].toFixed(2);

    ctxData["value"] = data["sentiment"]*50+50;
    document.getElementById("sentiment").innerHTML = (data["sentiment"]*50+50).toFixed(2) +"%";
    var config = {
            type: 'doughnut',
            data: {
                labels: [ctxData.label],
                datasets: [{
                    data: [ctxData.value, ctxData.max - ctxData.value],
                    backgroundColor: [ getColor(ctxData.value), '#0f0e17'],
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
                    text: ctxData.label,
                    fontSize: 16
                },
                plugins:{
                  legend: false,
                  title: false,
                }
            }
        };
    var gaugeChart = new Chart(ctx, config);

    //INTERPRET INSIDER TRADING
    let d = data["insider_trading"]
    let sad = [[],[],[]]
    for(let i = 0; i < d.length; i){
      sad[0].push(d[i++])
      sad[1].push(d[i++])
      sad[2].push(d[i++])
    }

    //create a div to append
    const sadge = document.createElement('div');
    for (let i = 0; i < sad[0].length; i++) {
      let p = document.createElement('p');
      p.textContent = `${sad[0][i]} | ${sad[1][i]} | ${sad[2][i]}`;
      sadge.appendChild(p);
    }
    document.getElementById("IT").appendChild(sadge)



    //request AI response
    setTimeout(()=>{
      let sen = "neutral"
      if(data["sentiment"]> .10){
        sen = "positive"
      } else if (data["sentiment"]< -.10){
        sen = "negative"
      }

      let tot = 0
      for(let i = 0; i < sad[0].length; i++){
        if(sad[2][i] == 'Buy'){
          tot += parseInt(sad[2][i])
        } else {
          tot -= parseInt(sad[2][i])
        }
      }

      res = "buying"
      if (tot > 0){
          res = "buying"
      } else {
          res = "selling"
      }
      reg = data["regression_prediction"] - data["stock_info"][0]

      fetch(`/getai`, {
        method: 'POST',
        body: JSON.stringify({  
            'tick' : val.toUpperCase(),
            'sen' : sen,
            'reg' : reg,
            'close' : data["stock_info"][3],
            'ins' : res
        }),
        headers: {
          "Content-Type": "application/json",
        }
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.text(); // or response.json() if your server responds with JSON
      })
      .then(data => {
          document.getElementById("aigen").textContent = data
        }, 500)
   })
   setTimeout(()=>{
    document.getElementById("blurb").classList.add("hidden");
   }, 1000)
   })
  .catch(error => {
    console.error('There has been a problem with your fetch operation:', error);
  });
    
    
});
