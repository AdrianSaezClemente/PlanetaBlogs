
$(document).ready(function() {

	idopcion = $('select').val();
	$('select').on('change',Dameidopcion);

	function Dameidopcion() {
		idopcion = $(this).val();
		alert(idopcion)
	}

	$("#buscar").click(function(){
			var texto = $("#texto").val();
			alert(texto)
			$.ajax({
				data: {'idopcion':idopcion, 'texto':texto},
				url: '/planetablogs/buscarNickUsuario/',
				type: 'GET',
				success: function(datos){
					alert( "Se guardaron los datos: " + datos);
				},
			});
		}
	);

});