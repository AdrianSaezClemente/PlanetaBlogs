$(document).ready(function(){
	$("#nuevohilo").hide()
	$("#butagregarhilo").click(function() {
		$("#nuevohilo").toggle("slide", 1000 );
	});
	
	$( "#tags" ).autocomplete({
		source: asignaturas
	});
});


function Agregar(idasignatura,titulo,descripcion){
	$('#agregar'+idasignatura).hide();
	var html = '<button title="Hilo añadido" type="button" class="btn-xs btn-success pull-right">Añadido<span class="glyphicon glyphicon-ok"></span></button>'
	$('#botonagregar'+idasignatura).html(html);
	//$('#'+idasignatura).hide();
	$.ajax({
		data: {'id':idasignatura},
		url: '/planetablogs/agregarasignaturaprofesor/',
		type: 'GET',
		success: function(datos){
			//console.log("añadido: "+datos)
		},
	});
	$("#nohayent").hide()
	$("#clase_lista_asignaturas").prepend("<li id='eliminar"+idasignatura+"' class='list-group-item nuevo'><div style='word-wrap:break-word;'><h6 class='list-group-item-heading'><div class='row'><div class='col-sm-9'><span><strong>Título: </strong>"+titulo+"</span></br><span><strong>Descripción: </strong>"+descripcion+"</span></div><div class='col-sm-3'><button type='button' class='btn-xs btn-warning pull-right boton' onclick=window.open('/planetablogs/tutores/hilo/"+idasignatura+"','_self')><span class='glyphicon glyphicon-camera'></span> Visitar</button><button onclick=EliminarHilo('"+idasignatura+"','"+titulo+"','"+descripcion+"'); id='botoneliminar"+idasignatura+"' title='Eliminar hilo' type='button' class='btn-xs btn-danger pull-right boton'><span class='glyphicon glyphicon-remove'></span> Eliminar</button></div></div></h6></div></li></br>");
	$("li#"+idasignatura).hide("highlight", 2000 );
}


function EliminarHilo(idasignatura,titulo,descripcion){
	console.log(titulo)
	var title = "Eliminar "+titulo;
	var mensaje = "¿Estás seguro de que quieres eliminar "+titulo+"?";
	BootstrapDialog.show({
		type: BootstrapDialog.TYPE_DANGER,
		title: title,
		message: mensaje,
		buttons: [{
			label: 'Cancelar',
			action: function(dialog) {
				dialog.close();
			}
		}, {
			icon: 'glyphicon glyphicon-remove',
			cssClass: 'btn-danger',
			label: 'Eliminar',
			action: function(dialog) {
				Eliminar(idasignatura,titulo,descripcion);
				dialog.close();
			}
		}]
	});
}

function Eliminar(idasignatura,titulo,descripcion){
	console.log(idasignatura)
	$('#eliminar'+idasignatura).hide(1500);
	$('#botoneliminar'+idasignatura).hide();
	$.ajax({
		data: {'id':idasignatura},
		url: '/planetablogs/eliminarasignaturaprofesor/',
		type: 'GET',
		success: function(datos){
			
		},
	});
	var html = "<div class='list-group'><li id="+idasignatura+" class='list-group-item'><div style='word-wrap:break-word;'>";
	html += "<h6  class='list-group-item-heading'><div class='row'><div class='col-sm-9'><span><strong>Título: </strong>"+titulo+"</span></br><span><strong>Descripción: </strong>"+descripcion+"</span>";
	html += "</div><div id='botonagregar"+idasignatura+"' class='col-sm-3'><button onclick=Agregar('"+idasignatura+"','"+titulo+"','"+descripcion+"'); id='agregar"+idasignatura+"' title='Añadir hilo' type='button' class='btn-xs btn-primary pull-right boton'><span class='glyphicon glyphicon-plus'></span>Añadir</button>";
	html += "</div></div></h6></div></li></div>";
	$("#clase_no_lista_asignaturas").prepend(html);
}