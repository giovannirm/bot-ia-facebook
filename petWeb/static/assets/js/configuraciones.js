$("#tbldisease").DataTable({
  language: {
    lengthMenu: "Mostrar  _MENU_  entrada",
    zeroRecords: "No se encontraron resultados en su búsqueda",
    info:
      "Mostrando registros de _START_ al _END_ de un total de _TOTAL_ Enfermedades",
    infoEmpty: "No existen registros",
    infoFiltered: "(filtrado de un total de _MAX_ registros)",
    search: "Buscar : ",
    paginate: {
      first: "Primero",
      last: "Ultimo",
      next: "Siguiente",
      previous: "Anterior",
    },
  },
});

function open_modal_update(url) {
  var $ = jQuery.noConflict();
  $("#update").load(url, function () {
    $(this).modal("show");
  });
};

function readDisease(rac_r, nam_r, sym_r, ans_r) {
  $("#rac_r").val(rac_r);
  $("#nam_r").val(nam_r);
  $("#sym_r").val(sym_r);
  $("#ans_r").val(ans_r);
};