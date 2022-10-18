const color_palette  = [
"#824638",
"#CE9587" ,
"#A86758" ,
"#6B2D1F" ,
"#491509" ,
"#825F38" ,
"#CEAD87" ,
"#A88258" ,
"#6B471F" ,
"#492B09" ,
"#254552" ,
"#577582" ,
"#3A5B6A" ,
"#163644" ,
"#08222E" ,
"#285E3E" ,
"#619476" ,
"#3F7857" ,
"#164D2C" ,
"#073419"]


const ctx = document.getElementById('station-chart');
const myChart = new Chart(ctx, {

    type: 'line',
    data: {
      datasets: [
        {% for name, data in stations.items() %}
          { label: "{{name}}",
            data: [{% for entry in data %}{x:'{{entry[1]}}', y:{{entry[2]}}},{% endfor %}],
            borderColor: color_palette.shift(),
            backgroundColor: "#ffffff",
          },
      {% endfor %}
    ]
  },
    options: {
      responsive: true,
      maintainAspectRatio: true
  }
});
