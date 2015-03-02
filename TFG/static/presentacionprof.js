$(document).ready(function(){
	$( "#tags" ).autocomplete({
		source: asignaturas
	});
	
});



function Agregar(idasignatura,titulo,descripcion){
	$('#agregar'+idasignatura).hide();
	var html = '<button title="Hilo añadido" type="button" class="btn-xs btn-success pull-right">Añadido<span class="glyphicon glyphicon-ok"></span></button>'
	$('li#'+idasignatura+' h6').append(html);
	//$('#'+idasignatura).hide();
	$.ajax({
		data: {'id':idasignatura},
		url: '/planetablogs/agregarasignaturaprofesor/',
		type: 'GET',
		success: function(datos){
			//console.log("añadido: "+datos)
			//$("#clase_lista_asignaturas").append("<a id='idasignatura' href='javascript:void(0)' class='list-group-item'>"+titulo+" - <span>"+descripcion+" </span><button onclick='Eliminar("+idasignatura+","+titulo+","+descripcion+");' id='eliminar"+idasignatura+"' title='Eliminar hilo' type='button' class='btn-xs btn-danger pull-right'><span class='glyphicon glyphicon-minus'></span></button></a>");
		},
	});
}


function Eliminar(idasignatura,titulo,descripcion){
	console.log(idasignatura)
	$('#eliminar'+idasignatura).hide(2000);
	$('#botoneliminar'+idasignatura).hide();
	var html = '<button title="Hilo eliminado" type="button" class="btn-xs btn-danger pull-right">Eliminado<span class="glyphicon glyphicon-ok"></span></button>'
	$('a#eliminar'+idasignatura).append(html);
	$.ajax({
		data: {'id':idasignatura},
		url: '/planetablogs/eliminarasignaturaprofesor/',
		type: 'GET',
		success: function(datos){
			
		},
	});
}