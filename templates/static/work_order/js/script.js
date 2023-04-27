console.log('ok');

// Função para formatar o valor do campo preço
var preco = document.querySelector("input[name='preco']");
var desconto = document.querySelector("input[name='desconto']");
var acrescimo = document.querySelector("input[name='acressimo']");
var total = document.querySelector("input[name='total']");

preco.oninput = function () {
  total.value = accounting.formatMoney(
    parseFloat(preco.value) -
      parseFloat(desconto.value) +
      parseFloat(acrescimo.value),
    'R$ ',
    2,
    '.',
    ','
  );
};
desconto.oninput = function () {
  total.value = accounting.formatMoney(
    parseFloat(preco.value) -
      parseFloat(desconto.value) +
      parseFloat(acrescimo.value),
    'R$ ',
    2,
    '.',
    ','
  );
};
acrescimo.oninput = function () {
  total.value = accounting.formatMoney(
    parseFloat(preco.value) -
      parseFloat(desconto.value) +
      parseFloat(acrescimo.value),
    'R$ ',
    2,
    '.',
    ','
  );
};

function getSelectedValue() {
  var selectedOption = document.querySelector(
    "#list_clients option[value='" +
      document.querySelector("input[list='list_clients']").value +
      "']"
  );
  var selectedClient = selectedOption.getAttribute('data-cod_cli');
  document.querySelector('#cod_cli').value = selectedClient;
  var selectedWhatsapp = selectedOption.getAttribute('data-whatsapp');
  document.querySelector('#whatsapp').value = selectedWhatsapp;
}


