// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

let dataViajes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
let dataCO2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

function getViajesTotales() {

  fetch("http://localhost:5000/viajes-anuales", {
      method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
      if (data.status == 'ok') {

        dataViajes = data.viajes;

        // Area Chart Example
        var ctx = document.getElementById("myAreaChart");
        var myLineChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sept", "Oct", "Nov", "Dic"],
            datasets: [{
              label: "Viajes",
              lineTension: 0.3,
              backgroundColor: "rgba(2,117,216,0.2)",
              borderColor: "rgba(2,117,216,1)",
              pointRadius: 5,
              pointBackgroundColor: "rgba(2,117,216,1)",
              pointBorderColor: "rgba(255,255,255,0.8)",
              pointHoverRadius: 5,
              pointHoverBackgroundColor: "rgba(2,117,216,1)",
              pointHitRadius: 50,
              pointBorderWidth: 2,
              data: dataViajes,
            }],
          },
          options: {
            legend: {
              display: true
            }
          }
        });
      } else {
        toastr.error(data.message);
      }
    });

}

function getCO2Totales() {

  fetch("http://localhost:5000/co2-anuales", {
      method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
      if (data.status == 'ok') {

        dataCO2 = data.co2;

        // Area Chart Example
        var co2 = document.getElementById("myAreaChartCo2");
        var myLineChartCO2 = new Chart(co2, {
          type: 'line',
          data: {
            labels: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sept", "Oct", "Nov", "Dic"],
            datasets: [{
              label: "Emisiones CO2",
              lineTension: 0.3,
              backgroundColor: "rgba(60, 179, 113,0.2)",
              borderColor: "rgba(60, 179, 113,1)",
              pointRadius: 5,
              pointBackgroundColor: "rgba(60, 179, 113,1)",
              pointBorderColor: "rgba(255,255,255,0.8)",
              pointHoverRadius: 5,
              pointHoverBackgroundColor: "rgba(2,117,216,1)",
              pointHitRadius: 50,
              pointBorderWidth: 2,
              data: dataCO2,
            }],
          },
          options: {
            legend: {
              display: true
            }
          }
        });
      } else {
        toastr.error(data.message);
      }
    });

}

getViajesTotales();
getCO2Totales();