console.log("ok");

var preco = document.querySelector("input[name='preco']");
var desconto = document.querySelector("input[name='desconto']");
var acrescimo = document.querySelector("input[name='acressimo']");
var total = document.querySelector("input[name='total']");


preco.oninput = function() {
    total.value = accounting.formatMoney(parseFloat(preco.value) - parseFloat(desconto.value) + parseFloat(acrescimo.value), "R$ ", 2, ".", ",");
}
desconto.oninput = function() {
  total.value = accounting.formatMoney(parseFloat(preco.value) - parseFloat(desconto.value) + parseFloat(acrescimo.value), "R$ ", 2, ".", ",");
}
acrescimo.oninput = function() {
  total.value =accounting.formatMoney(parseFloat(preco.value) - parseFloat(desconto.value) + parseFloat(acrescimo.value), "R$ ", 2, ".", ",");
}
