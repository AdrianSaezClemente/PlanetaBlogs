

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
	$.ajax({
		data: {'id':identrada},
		url: '/planetablogs/up/',
		type: 'GET',
		success: function(datos){
			alert( "Se guardaron los datos: " + datos);
		},
		/*success: function(data){
			for (var i=0;i<entrada.length;i++){
				var ent = entrada[i]
				if (ent.pk == identrada){
					ent.fields.up += 1
					ent.save()
					break;
				}
			}*/
		
	});
	/*for (var i=0;i<usuario.length;i++){
		var usu = usuario[i]
		if (usu.pk == idusuario){
			usu.fields.puntuaciontotal += 3
			usu.save()
			break;
		}
	}
	for (var i=0;i<entrada.length;i++){
		var ent = entrada[i]
		if (ent.pk == identrada){
			ent.fields.up += 1
			ent.save()
			break;
		}
	}*/
	//$("#up").append("<a href="+url_blog+">"+nombre+"</a>");
}

function Down(identrada){
	$.ajax({
		data: {'id':identrada},
		url: '/planetablogs/down/',
		type: 'GET',
		success: function(datos){
			alert( "Se guardaron los datos: " + datos);
		},
		/*success: function(data){
			for (var i=0;i<entrada.length;i++){
				var ent = entrada[i]
				if (ent.pk == identrada){
					ent.fields.up += 1
					ent.save()
					break;
				}
			}*/
		
	});
}

$.noConflict();
$(document).ready(function() {
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