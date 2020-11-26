$(document).ready(function () {
  var t = 4;
  $("#add").click(function () {
    var a =
      '<div class="form-group row" id="flow-' +
      t +
      '">\n\t\t\t\t\t\t\t<div class="col-11">\n\t\t\t\t\t\t\t\t<div class="input-group mb-2">\n\t\t\t\t\t\t\t\t\t<div class="input-group-prepend">\n\t\t\t\t\t\t\t\t\t\t<span class="input-group-text year">Síntoma ' +
      t +
      ':</span>\n\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t\t<input type="text" step="any" class="form-control" id="fc' +
      t +
      '" placeholder="Ingresa un síntoma de la enfermedad congénita">\n\t\t\t\t\t\t\t\t\t<div class="input-group-append">\n\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t<div class="col-1 mt-2 p-0">\n\t\t\t\t\t\t\t\t<i class="fas fa-backspace remove"></i>\n\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t</div>';
    $("#flow").append(a), t++;
  });
  $("#flow").on("click", ".remove", function () {
    var a = $(this).parents(".form-group").attr("id");
    $("#" + a).remove(), (a = parseFloat(a.split("-")[1])), (new_id = a);
    for (var n = a + 1; n < t; n++)
      $("#flow")
        .children("#flow-" + n)
        .find(".year")
        .html("Síntoma " + new_id + ":"),
        $("#flow")
          .children("#flow-" + n)
          .find("#fc" + n)
          .attr("id", "fc" + new_id),
        $("#flow")
          .children("#flow-" + n)
          .attr("id", "flow-" + new_id),
        new_id++;
    t--;
  });
});
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

function readDisease(rac_r, nam_r, sym_r, ans_r) {
  $("#rac_r").val(rac_r);
  $("#nam_r").val(nam_r);
  $("#sym_r").val(sym_r);
  $("#ans_r").val(ans_r);
}

function updateDisease(id_u, rac_u, nam_u, sym_u, ans_u) {
  $("#id_u").val(id_u);
  $("#rac_u").val(rac_u);
  $("#nam_u").val(nam_u);
  $("#sym_u").val(sym_u);
  $("#ans_u").val(ans_u);
}
