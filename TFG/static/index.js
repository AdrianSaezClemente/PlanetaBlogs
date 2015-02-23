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


function Up(identrada,idusuario,idasignatura){
	var up1 = $("#up"+identrada).text();
	var up = parseInt(up1) + parseInt(1)
	$.ajax({
		data: {'identrada':identrada,'idusuario':idusuario,'idasignatura':idasignatura,'up':up},
		url: '/planetablogs/up/',
		type: 'GET',
		success: function(datos){

		},
	});
	$("#up"+identrada).text(parseInt(up));
}

function Down(identrada,idusuario,idasignatura){
	var down1 = $("#down"+identrada).text();
	var down = parseInt(down1) + parseInt(1)
	$.ajax({
		data: {'identrada':identrada,'idusuario':idusuario,'idasignatura':idasignatura,'down':down},
		url: '/planetablogs/down/',
		type: 'GET',
		success: function(datos){
			//datos.entrada[0].fields.down += 1
			//console.log(datos.entrada[0].fields.down)
		},
	});
	$("#down"+identrada).text(parseInt(down));
}

function EliminarComentario(idcomentario,idasignatura){
	$('#comentario'+idcomentario).hide("slow");
	$('#infocomentario'+idcomentario).show("slow");
	$.ajax({
		data: {'idcomentario':idcomentario,'idasignatura':idasignatura},
		url: '/planetablogs/eliminarcomentario/',
		type: 'GET',
		success: function(datos){
			
		},
	});
}

function CalcularPlanetsEntrada(id,up,down){
	var total = up*3-down*1
	$("#total"+id).append(total)
}

$.noConflict();
$(document).ready(function() {
	//CalcularPlanetsEntrada(up,down)
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