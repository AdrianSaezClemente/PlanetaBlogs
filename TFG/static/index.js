$.noConflict();
$(document).ready(function() {
	$(".oculto").hide();
	$("#subir").hide();
	
	//Darle el alto y ancho
	$("#popup").css('width', 300 + 'px');
	$("#popup").css('height', 150 + 'px');
	
   
	$(".usuario").mouseover(function() {
		SacarPosicion(this);
		var id = $(this).attr("id");
		InformacionUsuario(id);
	});
	$(".usuario").mouseout(function() {
		var id = $(this).attr("id");
		$("#popup").fadeOut(200);
		$("#popup").html("");
	});
	
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

function SacarPosicion(elemento){
	var posicion = $(elemento).position();
	var x = posicion.left + 250;
	var y = posicion.top + 250;
	$("#popup").css("left",x + "px");
	$("#popup").css("top",y + "px");
}

function InformacionUsuario(id){
	for (i=0;i<usuarios.length;i++){
		if (usuarios[i].pk == id){
			for (k=0;k<alumnos.length;k++){
				if (id == alumnos[k].fields.alumno){
					idalumno = alumnos[k].pk
					break;
				}
			}
			for (j=0;j<valoraciones.length;j++){
				if (valoraciones[j].fields.alumno == idalumno){
					var html = "<div class='panel-heading'><div class='panel-title'>Información de usuario</div></div>";
					html += "<div class='panel-body'><span class='pull-left'>Nombre: "+usuarios[i].fields.first_name+"</span></br>";
					html += "<span class='pull-left'>Apellidos: "+usuarios[i].fields.last_name+"</span></br>";
					html += "<span class='pull-left'>Puntos: "+valoraciones[j].fields.puntos+"</span></br>";
					html += "<span class='pull-left'>Nivel: "+valoraciones[j].fields.nivel+"</span></div>";
					$("#popup").append(html);
					$("#popup").fadeIn();
					break;
				}
			}
		}
	}
}

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

function Up(identrada,idusuario,idasignatura,up,down){
	var up1 = parseInt(up) + parseInt(1)
	$.ajax({
		data: {'identrada':identrada,'idusuario':idusuario,'idasignatura':idasignatura,'up':up},
		url: '/planetablogs/up/',
		type: 'GET',
		success: function(datos){
			var html = "<div class='btn-group'><button type='button' disabled='disabled' class='btn btn-success btn-xs'><span class='badge'>"+up1+"</span></button></div> <div class='btn-group'><button type='button' disabled='disabled' class='btn btn-danger btn-xs'><span class='badge'>"+down+"</span></button></div>"
			$("#updown"+identrada).html(html);
		},
	});
}

function Down(identrada,idusuario,idasignatura,up,down){
	var down1 = parseInt(down) + parseInt(1)
	$.ajax({
		data: {'identrada':identrada,'idusuario':idusuario,'idasignatura':idasignatura,'down':down},
		url: '/planetablogs/down/',
		type: 'GET',
		success: function(datos){
			var html = "<div class='btn-group'><button type='button' disabled='disabled' class='btn btn-success btn-xs'><span class='badge'>"+up+"</span></button></div> <div class='btn-group'><button type='button' disabled='disabled' class='btn btn-danger btn-xs'><span class='badge'>"+down1+"</span></button></div>"
			$("#updown"+identrada).html(html);
		},
	});
}

function AgregarComentario(identrada,idasignatura,iduser){
	var descripcion = $("#descripcion_comentario").val();
	$.ajax({
		data: {'identrada':identrada,'idasignatura':idasignatura,'iduser':iduser,'descripcion':descripcion},
		url: '/planetablogs/agregarcomentario/',
		type: 'GET',
		success: function(datos){
			console.log("exitoso")
			if (descripcion==""){
				console.log("nada")
				$("#entrada").append("<h5 style='color:red;text-align:center;font-style:oblique;font-size:10px;'>Escribe tu comentario antes de enviar.</h5>"); 
			}
			else{
				$("#descripcion_comentario").val("")
				BorrarInfo();
				var html = "<div id='comentario"+datos.comentario[0].pk+"' class='panel panel-warning'>";
				html += "<div id='titulopanel' class='panel-heading'><div class='panel-title'>Comentario publicado por "+datos.usuario[0].fields.username+"<span class='pull-right'>"+datos.comentario[0].fields.fecha+"</span></div></div>";
				html += "<div style='word-wrap:break-word;' class='panel-body'>"+datos.comentario[0].fields.descripcion+"<button id='"+datos.comentario[0].pk+"' onclick='EliminarComentario("+datos.comentario[0].pk+","+datos.comentario[0].fields.asignatura+")' type='button' class='btn btn-danger btn-xs pull-right'>Eliminar comentario</button></div></div>";
				html += "<div id='infocomentario"+datos.comentario[0].pk+"' class='info oculto'><div class='alert alert-success alert-dismissable'><button type='button' class='close' data-dismiss='alert'>&times;</button><strong>¡Comentario borrado!</strong> Vuelve a comentar cuando lo desees.</div></div>";
				$("#entrada").append(html);
				$("#infocomentario"+datos.comentario[0].pk).hide();
			}
		},
	});
}

function EliminarComentario(idcomentario,idasignatura){
	$('#comentario'+idcomentario).hide("slow");
	$('#infocomentario'+idcomentario).show("slow");
	$.ajax({
		data: {'idcomentario':idcomentario,'idasignatura':idasignatura},
		url: '/planetablogs/eliminarcomentario/',
		type: 'GET',
		success: function(datos){
			setTimeout(BorrarComentario(idcomentario),2000)
		},
	});
}

function BorrarComentario(idcomentario){
	$('#comentario'+idcomentario).remove();
}

function CalcularPlanetsEntrada(id,up,down){
	$("#total"+id).html("")
	var total = up*3-down*1
	$("#total"+id).html(total)
}

function BorrarInfo(){
	$(".info").remove();
}