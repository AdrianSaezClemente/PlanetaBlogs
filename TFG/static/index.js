function CompararNick(nick,contra){
	alert(nick+contra)
	for (var i=0;i<usuario.length;i++){
		if ((usuario[i].fields.nick == nick) && (usuario[i].fields.password == contra)){
			var url_blog = usuario[i].fields.url_blog
			var nombre = usuario[i].fields.nombre_apellidos
			$("#sub_nick").append("<a href="+url_blog+">"+nombre+"</a>");
		}
	}
}

function Up(identrada){
	var up = $("#up"+identrada).text();
	$.ajax({
		data: {'id':identrada, 'up':up},
		url: '/planetablogs/up/',
		type: 'GET',
		success: function(datos){

		},
	});
	$("#up"+identrada).text(parseInt(up)+1);
}

function Down(identrada){
	var down = $("#down"+identrada).text();
	$.ajax({
		data: {'id':identrada, 'down':down},
		url: '/planetablogs/down/',
		type: 'GET',
		success: function(datos){
			//datos.entrada[0].fields.down += 1
			//console.log(datos.entrada[0].fields.down)
		},
	});
	$("#down"+identrada).text(parseInt(down)+1);
}

function EliminarComentario(idcomentario,idasignatura){
	console.log(idcomentario)
	$('#comentario'+idcomentario).hide("slow");
	$.ajax({
		data: {'idcomentario':idcomentario,'idasignatura':idasignatura},
		url: '/planetablogs/eliminarcomentario/',
		type: 'GET',
		success: function(datos){
			
		},
	});
}

$.noConflict();
$(document).ready(function() {
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