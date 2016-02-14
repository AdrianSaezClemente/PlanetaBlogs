$(document).ready(function(){
	/*( "#tags" ).autocomplete({
		source: asignaturas
	});*/
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
	
	$(function(){
		$(".dropdown-menu").on('click', 'li a', function(){
			$(".btnmenu:first-child").text($(this).text());
			$(".btnmenu:first-child").val($(this).text());
			$(".btnmenu").append(" <span class='caret'></span>")
		});
	});
	
	MostrarEstiloUsuario(usuario);
});


function MostrarEstiloUsuario(usuario) {
	for (i=0;i<disenos.length;i++){
		if (usuario[0].fields.estilo == disenos[i].fields.estilo){
			$("body").prepend("<img id='fondo' src='../../../../../static/imagenes/"+disenos[i].fields.imagen+"'/>");
			//$("body").css("background-image",'url("/static/imagenes/'+disenos[i].fields.imagen+'")');
			//$("body").css("background-attachment",'fixed');
			break;
		}
	}
}

function CambiarEstilo(iddiseno) {
	for (i=0;i<disenos.length;i++){
		if (disenos[i].pk == parseInt(iddiseno)){
			$("#fondo").remove()
			$("body").prepend("<img id='fondo' src='../../../../../static/imagenes/"+disenos[i].fields.imagen+"'/>");
			//$("body").css("background-image",'url("/static/imagenes/'+disenos[i].fields.imagen+'")');
			//$("body").css("background-attachment",'fixed');
			$("#botonlistadisenos").html(disenos[i].fields.estilo+"<span class='pequeña glyphicon glyphicon-list'></span><span class='caret'></span>");
			CambiarEstiloAjax(disenos[i].fields.usuario,disenos[i].fields.estilo)
			break;
		}
	}
}

function CambiarEstiloAjax(idusuario,estilo){
	$.ajax({
		data: {'idusuario':idusuario,'estilo':estilo},
		url: '/planetablogs/cambiarestilo/',
		type: 'GET',
		success: function(datos){
			
		},
	});
}

function EliminarHilo(idasignatura,titulo,descripcion){
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