$.noConflict();
$(document).ready(function() {
	$(".oculto").hide();
	$("#subir").hide();
	
	//Darle el alto y ancho
	$("#popupinfotutor").css('width', 'auto');
	$("#popupinfotutor").css('height', 'auto');
	
	$(".infotutor").mouseover(function() {
		SacarPosicionInfoTutor(this);
		var idasignatura = $(this).attr("id");
		InformacionTutores(idasignatura);
	});
	$(".infotutor").mouseout(function() {
		var id = $(this).attr("id");
		$("#popupinfotutor").fadeOut(200);
		$("#popupinfotutor").html("");
	});
	
	//Darle el alto y ancho
	$("#popup").css('width', 350 + 'px');
	$("#popup").css('height', 200 + 'px');
	
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

function MostrarComentarios(id) {
	if($("#desplieguecomentarios"+id).is(":visible") ){
		$("#despliegueboton"+id).html("<span class='glyphicon glyphicon-arrow-down'></span> Mostrar comentarios");
	}else{
		$("#despliegueboton"+id).html("<span class='glyphicon glyphicon-arrow-up'></span> Ocultar comentarios");
	}
	var str = $("#comentariosentrada"+id).text()
	var cadena = str.replace(/\s/g, '');
	if(cadena == ''){
		$("#comentariosentrada"+id).html("<div id=nohaycomen"+id+"><p style='text-align:center;font-size:9px;font-weight:bold:font-style:oblique;color:red;'>No hay comentarios en esta entrada. !Sé el primero en escribir!</p></div>");
	}
	$("#desplieguecomentarios"+id).toggle("fast","swing");
}

function SacarPosicion(elemento){
	var posicion = $(elemento).position();
	var x = posicion.left + 250;
	var y = posicion.top + 250;
	$("#popup").css("left",x + "px");
	$("#popup").css("top",y + "px");
}

function SacarPosicionInfoTutor(elemento){
	var posicion = $(elemento).position();
	var x = posicion.left;
	var y = posicion.top + 25;
	$("#popupinfotutor").css("left",x + "px");
	$("#popupinfotutor").css("top",y + "px");
}

function InformacionTutores(idasignatura){
	for (i=0;i<asignaturas.length;i++){
		if (asignaturas[i].pk == parseInt(idasignatura)){
			titulo = asignaturas[i].fields.titulo
			var creador = asignaturas[i].fields.creador
			break;
		}
	}
	for (k=0;k<usuarios.length;k++) {
		if (usuarios[k].pk == creador){
			var html = "<div class='panel-heading popupcabecera'><div class='panel-title'><div style='font-style:oblique;font-size:1em;text-align:center;'>Creador del hilo "+titulo+"</div></div></div>";
			html += "<div class='panel-body'><span style='font-size:11px;' class='pull-left'>"+usuarios[k].fields.first_name+" "+usuarios[k].fields.last_name+" ("+usuarios[k].fields.email+")</span></br>";
			break;
		}
	}
	$("#popupinfotutor").append(html);
	$("#popupinfotutor").fadeIn();
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
					var html = "<div class='panel-heading popupcabecera'><div class='panel-title'><img src='../../../../../static/imagenes/"+usuarios[i].fields.imagen+"' class='fotogrande'> </img><span style='margin-left:45px;'>Información de usuario</span></div></div>";
					html += "<div class='panel-body'><span style='font-weight:bold;' class='pull-left'>Usuario:</span><span>&nbsp; "+usuarios[i].fields.first_name+" "+usuarios[i].fields.last_name+"</span></br>";
					html += "<span style='font-weight:bold;' class='pull-left'>Correo:</span><span>&nbsp; "+usuarios[i].fields.email+"</span></br>";
					html += "<span style='font-weight:bold;' class='pull-left'>Puntos:</span><span>&nbsp; "+valoraciones[j].fields.puntos+"</span></br>";
					html += "<span style='font-weight:bold;' class='pull-left'>Nivel:</span><span>&nbsp; "+valoraciones[j].fields.nivel+"</span></div>";
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
	var descripcion = $("#descripcion_comentario"+identrada).val();
	fecha = ConvertirFecha();
	$.ajax({
		data: {'identrada':identrada,'idasignatura':idasignatura,'iduser':iduser,'descripcion':descripcion},
		url: '/planetablogs/agregarcomentario/',
		type: 'GET',
		success: function(datos){
			console.log("exitoso")
			if (descripcion==""){
				console.log("nada")
				$("#comentariosentrada"+identrada).append("<h5 style='color:red;text-align:center;font-style:oblique;font-size:10px;'>Escribe tu comentario antes de enviar.</h5>"); 
			}
			else{
				$("#nohaycomen"+identrada).html("");
				$("#descripcion_comentario"+identrada).val("");
				BorrarInfo();
				var html = "</br><div id='comentario"+datos.comentario[0].pk+"' class='panel panel-warning'>";
				html += "<div id='titulopanel' class='panel-heading'><div class='panel-title'>Comentario publicado por "+datos.usuario[0].fields.username+"<span class='pull-right'>"+fecha+"</span></div></div>";
				html += "<div style='word-wrap:break-word;' class='panel-body'>"+datos.comentario[0].fields.descripcion+"<button id='"+datos.comentario[0].pk+"' onclick='EliminarComentario("+datos.comentario[0].pk+","+datos.comentario[0].fields.asignatura+")' type='button' class='btn btn-danger btn-xs pull-right'>Eliminar comentario</button></div></div>";
				html += "<div id='infocomentario"+datos.comentario[0].pk+"' class='info oculto'><div class='alert alert-success alert-dismissable'><button type='button' class='close' data-dismiss='alert'>&times;</button><strong>¡Comentario borrado!</strong> Vuelve a comentar cuando lo desees.</div></div>";
				$("#comentariosentrada"+identrada).prepend(html);
				$("#infocomentario"+datos.comentario[0].pk).hide();
			}
		},
	});
}

function ConvertirFecha() {
	var nombres_dias = new Array('Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado');
	var nombres_meses = new Array('Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre');
	var now = new Date();
	console.log(nombres_dias);
	if (now.getMinutes()<10){ var minutos = '0' + now.getMinutes()}
	else { var minutos = now.getMinutes() }
	if (now.getHours()<10){ var horas = '0' + now.getHours()}
	else { var horas = now.getHours() }
	var fecha =  now.getDate() + " de " + nombres_meses[now.getMonth()] + " de " + now.getFullYear() + ", " + nombres_dias[now.getDay()] + " a las " + horas + ":" + minutos;
	return fecha;
	//return "hola"
}

function EliminarComentario(idcomentario,idasignatura){
	$('#comentario'+idcomentario).hide("slow");
	$('#infocomentario'+idcomentario).show("slow").delay(2000).hide("slow");
	$.ajax({
		data: {'idcomentario':idcomentario,'idasignatura':idasignatura},
		url: '/planetablogs/eliminarcomentario/',
		type: 'GET',
		success: function(datos){
			
		},
	});
}

function BorrarComentario(idcomentario){
	$('#infocomentario'+idcomentario).hide("slow");
}

function CalcularPlanetsEntrada(id,up,down){
	$("#total"+id).html("")
	var total = up*2-down*1
	$("#total"+id).html(total)
}

function BorrarInfo(){
	$(".info").remove();
}