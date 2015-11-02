$(document).ready(function(){
	$( "#tags" ).autocomplete({
		source: asignaturas
	});
	$(".oculto").hide();
	
	$("#subir").hide();
	$(function () {
		$(window).scroll(function () {
			if ($(this).scrollTop() > 200) {
				$('#subir').fadeIn();
			} else {
				$('#subir').fadeOut();
			}
		});
		$('#subir a').click(function () {
			$('body,html').animate({
				scrollTop: 0
			}, 800);
			return false;
		});
	});
});

function EliminarHilo(idasignatura,titulo,descripcion){
	console.log(titulo)
	var title = "¡CUIDADO! Vas a eliminar "+titulo;
	var mensaje = "<p>¿Estás seguro de que quieres eliminar "+titulo+" de tus hilos?</p><span>Se perderá toda tu información dentro de este hilo:</span><ul><li>Tus entradas imprimidas.</li><li>Los comentarios que hayas realizado en tus entradas.</li><li>Valoraciones positivas y negativas.</li><li>Tu puntuación obtenida hasta este momento.</li></ul>";
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
	$('#eliminar'+idasignatura).hide(2000);
	$('#botoneliminar'+idasignatura).hide();
	$.ajax({
		data: {'id':idasignatura},
		url: '/planetablogs/eliminarasignaturaalumno/',
		type: 'GET',
		success: function(datos){
			
		},
	});
}