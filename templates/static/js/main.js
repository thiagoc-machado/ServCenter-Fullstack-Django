const charts = document.querySelectorAll(".chart");
charts.forEach(function (chart) {
  var ctx = chart.getContext("2d");
  var myChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["8 hrs", "9 hrs", "10 hrs", "11 hrs", "12 hrs", "13 hrs", "14 hrs", "15 hrs", "16 hrs", "17 hrs", "18 hrs"],
      datasets: [
        {
          label: "Entradas por hora",
          data: [values_by_hour[0], values_by_hour[1], values_by_hour[2], values_by_hour[3], values_by_hour[4], values_by_hour[5], values_by_hour[6], values_by_hour[7], values_by_hour[8], values_by_hour[9], values_by_hour[10], values_by_hour[11]],
          backgroundColor: [
            "rgba(38, 143, 99, 0.435)",
          ],
          borderColor: [
            "rgba(38, 143, 99, 1)",       
          ],
          borderWidth: 1,
        },
        {
          label: "Saídas por hora",
          data: [output_by_hour[0], output_by_hour[1], output_by_hour[2], output_by_hour[3], output_by_hour[4], output_by_hour[5], output_by_hour[6], output_by_hour[7], output_by_hour[8], output_by_hour[9], output_by_hour[10], output_by_hour[11]],
          backgroundColor: "rgba(255, 0, 0, 0.6)",
          borderColor: "rgba(255, 0, 0, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
});


$(document).ready(function () {
  $(".data-table").each(function (_, table) {
    $(table).DataTable();
  });
});


var spinner = document.getElementById("spinner");
// Exibe o spinner quando a página estiver carregando
window.addEventListener("beforeunload", function(event) {
  spinner.classList.remove("d-none");
  document.title = "ServCenter - Carregando...";
  event.preventDefault();
});

// Oculta o spinner quando a página estiver carregada
window.addEventListener("load", function(event) {
  spinner.classList.add("d-none");
  document.title = "ServCenter"; // Altere para o título correto da sua página
});