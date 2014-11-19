
$(document).ready(function() {
	
					
	idopcion = $('select').val();
	$('select').on('change',Dameidopcion);

	function Dameidopcion() {
		idopcion = $(this).val();
	}

	$("#buscar").click(function(){
			var texto = $("#texto").val();
			$.ajax({
				data: {'idopcion':idopcion, 'texto':texto},
				url: '/planetablogs/buscarNickUsuario/',
				type: 'GET',
				success: function(datos){
					console.log(datos)
					/*
					for(i=0;i<entradas.length;i++){
						//$("#resultado").append("<h2>"+datos.entradas[i].fields.titulo+"</h2>");
					}*/
				},
			});
		}
	);

});