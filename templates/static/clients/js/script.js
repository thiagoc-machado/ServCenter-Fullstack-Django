const btn_del = document.querySelectorAll('.delete');
btn_del.forEach(function (botao) {
    botao.addEventListener("click", function (e) {
      if (!confirm("Tem certeza que deseja apagar esse registro?")) {
        console.log('não apagou');
        e.preventDefault();
      }
  });
});