$.noConflict();
$(document).ready(function() {
	$(".oculto").hide();
	$("#subir").hide();
	
	FrasesAleatorias("#slogan");
	$("#slogan").click(function () {
		FrasesAleatorias(this);
	});
	
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
		$("#popupinfotutor").fadeOut(0);
		$("#popupinfotutor").html("");
	});
	
	//Darle el alto y ancho
	$("#popup").css('width', 350 + 'px');
	$("#popup").css('height', 'auto');
	
	$(".usuario").mouseover(function() {
		SacarPosicion(this);
		var id = $(this).attr("id");
		InformacionUsuario(id);
	});
	$(".usuario").mouseout(function() {
		var id = $(this).attr("id");
		$("#popup").fadeOut(0);
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
	var totalcomentarios = parseInt($("#totalcomentarios"+id).text())
	if($("#desplieguecomentarios"+id).is(":visible")){
		$("#despliegueboton"+id).html("<span class='glyphicon glyphicon-arrow-down'></span> Mostrar comentarios (<span id='totalcomentarios"+id+"'>"+totalcomentarios+"</span>)");
	}else{
		$("#despliegueboton"+id).html("<span class='glyphicon glyphicon-arrow-up'></span> Ocultar comentarios (<span id='totalcomentarios"+id+"'>"+totalcomentarios+"</span>)");
	}
	if(totalcomentarios == 0){
		$("#desplieguecomentarios"+id).html("<div id=nohaycomen"+id+"><p style='text-align:center;font-size:9px;font-weight:bold:font-style:oblique;color:red;'>No hay comentarios en esta entrada.</p></div>");
	}
	var str = $("#desplieguecomentarios"+id).text()
	var cadena = str.replace(/\s/g, '');
	if(cadena == ''){
		$("#desplieguecomentarios"+id).html("<div id=nohaycomen"+id+"><p style='text-align:center;font-size:9px;font-weight:bold:font-style:oblique;color:red;'>No hay comentarios en esta entrada.</p></div>");
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
	var x = posicion.left - 200;
	var y = posicion.top + 25;
	$("#popupinfotutor").css("left",x + "px");
	$("#popupinfotutor").css("top",y + "px");
}

function InformacionTutores(idasignatura){
	for (i=0;i<asignaturas.length;i++){
		if (asignaturas[i].pk == parseInt(idasignatura)){
			//titulo = asignaturas[i].fields.titulo
			var creador = asignaturas[i].fields.creador
			break;
		}
	}
	for (k=0;k<usuarios.length;k++) {
		if (usuarios[k].pk == creador){
			var html = "<div class='panel-heading popupcabecera'><div class='panel-title'><div style='font-style:oblique;font-size:1em;text-align:center;'>Creador del hilo</div></div></div>";
			html += "<div class='panel-body'><span style='font-size:11px;' class='pull-left'><img src='../../../../../static/imagenes/"+usuarios[k].fields.imagen+"' style='border:1px solid black;' class='fotopequeña'> </img>"+usuarios[k].fields.first_name+" "+usuarios[k].fields.last_name+" ("+usuarios[k].fields.email+")</span></br>";
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
					html += "<div style='font-family: Verdana, Arial, Helvetica, sans-serif'; class='panel-body'><span style='font-weight:bold;' class='pull-left'>Usuario:</span><span>&nbsp; "+usuarios[i].fields.first_name+" "+usuarios[i].fields.last_name+"</span></br>";
					html += "<span style='font-weight:bold;' class='pull-left'>Correo:</span><span>&nbsp; "+usuarios[i].fields.email+"</span></br>";
					if (usuarios[i].fields.username != "admin"){
						html += "<span style='font-weight:bold;' class='pull-left'>Puntos:</span><span>&nbsp; "+valoraciones[j].fields.puntos+"</span></br>";
						html += "<span style='font-weight:bold;' class='pull-left'>Nivel:</span><span>&nbsp; "+valoraciones[j].fields.nivel+"</span></div>";
					}
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

		},
	});
	var html = "<div class='btn-group'><button type='button' disabled='disabled' class='btn btn-success btn-xs'><span class='badge'>"+up1+"</span></button></div> <div class='btn-group'><button type='button' disabled='disabled' class='btn btn-danger btn-xs'><span class='badge'>"+down+"</span></button></div>"
	$("#updown"+identrada).html(html);
}

function Down(identrada,idusuario,idasignatura,up,down){
	var down1 = parseInt(down) + parseInt(1)
	$.ajax({
		data: {'identrada':identrada,'idusuario':idusuario,'idasignatura':idasignatura,'down':down},
		url: '/planetablogs/down/',
		type: 'GET',
		success: function(datos){
			//datos.entrada[0].fields.down += 1
			//console.log(datos.entrada[0].fields.down)
		},
	});
	var html = "<div class='btn-group'><button type='button' disabled='disabled' class='btn btn-success btn-xs'><span class='badge'>"+up+"</span></button></div> <div class='btn-group'><button type='button' disabled='disabled' class='btn btn-danger btn-xs'><span class='badge'>"+down1+"</span></button></div>"
	$("#updown"+identrada).html(html);
}
/*
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
*/
function EliminarComentario(idcomentario,idasignatura,identrada){
	var totalcomentarios = parseInt($("#totalcomentarios"+identrada).text()) - 1
	$("#despliegueboton"+identrada).html("<span class='glyphicon glyphicon-arrow-up'></span> Ocultar comentarios (<span id='totalcomentarios"+identrada+"'>"+totalcomentarios+"</span>)");
	$('#comentario'+idcomentario).hide("slow");
	$('#infocomentario'+idcomentario).show("slow").delay(2000).hide("slow");
	$.ajax({
		data: {'idcomentario':idcomentario,'idasignatura':idasignatura,'identrada':identrada},
		url: '/planetablogs/eliminarcomentario/',
		type: 'GET',
		success: function(datos){
		},
	});
}

function CalcularPlanetsEntrada(id,up,down){
	$("#total"+id).html("")
	var total = up*2-down*1
	$("#total"+id).html(total)
}

function BorrarInfo(){
	$(".info").remove();
}

function EliminarEntradaPopUp(idasignatura,identrada,nombre,apellidos,entrada){
	var title = "Eliminar entrada correspondiente a "+nombre+" "+apellidos;
	var mensaje = "¿Estás seguro de que quieres eliminar #"+entrada+"?";
	mensaje += "</br></br><span>Se perderá toda la información sobre esta entrada:</span><ul><li>Sus valoraciones positivas y negativas.</li><li>Sus comentarios.</li><li>Se realizará un recálculo de planets.</li></ul>";
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
				EliminarEntrada(idasignatura,identrada);
				dialog.close();
			}
		}]
	});
}

function EliminarEntrada(idasignatura,identrada){
	$('#entrada'+identrada).hide("slow");
	$('#infoentrada'+identrada).show("slow");
	$.ajax({
		data: {'identrada':identrada, 'idasignatura':idasignatura},
		url: '/planetablogs/eliminarentrada/',
		type: 'GET',
		success: function(datos){
			$('#infoentrada'+identrada).show("slow");
		},
	});
}

function EliminarAlumnoPopUp(idasignatura,idalumno,nombre,apellidos){
	var title = "<strong>¡Cuidado!</strong> Vas a eliminar a "+nombre+" "+apellidos;
	var mensaje = "¿Estás seguro de que quieres eliminar a "+nombre+"?";
	mensaje += "</br></br><span>Se perderá toda su información dentro de este hilo:</span><ul><li>Sus entradas impresas.</li><li>Los comentarios que haya realizado.</li><li>Sus valoraciones positivas y negativas.</li><li>Su puntuación obtenida hasta este momento.</li><li>Se realizará un recálculo de planets.</li></ul>";
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
				EliminarAlumno(idasignatura,idalumno);
				dialog.close();
			}
		}]
	});
}

function EliminarAlumno(idasignatura,idalumno){
	$('#alumno'+idalumno).hide("slow");
	$.ajax({
		data: {'idalumno':idalumno, 'idasignatura':idasignatura},
		url: '/planetablogs/eliminaralumno/',
		type: 'GET',
		success: function(datos){

		},
	});
}

function FrasesAleatorias(elemento){
	console.log("hago click")
	//almacenando las citas
	frases = new Array(21);
	frases[0] = "El fracaso derrota a los perdedores, el fracaso inspira a los ganadores.";
	frases[1] = "La única parte donde el ‘éxito’ aparece antes que el ‘trabajo’ es en el diccionario.";
	frases[2] = "Algunas personas sueñan con hacer grandes cosas, mientras otras están despiertas y las hacen.";
	frases[3] = "No puede impedirse el viento, pero hay que saber construir molinos.";
	frases[4] = "Tan solo los mediocres nunca tienen un mal día.";
	frases[5] = "Si vives cada día como si fuera el último, algún día tendrás razón.";
	frases[6] = "Un hombre con una nueva idea es un loco hasta que ésta triunfa.";
	frases[7] = "Tan solo hay tres grupos de personas: los que hacen que las cosas pasen, los que miran las cosas que pasan y los que preguntan qué pasó.";
	frases[8] = "Hombre sin sonrisa no abre tienda.";
	frases[9] = "No he fracasado, he encontrado 10.000 maneras en las que esto no funciona.";
	frases[10] = "Solo cuando baja la marea se sabe quién nadaba desnudo.";
	frases[11] = "Nada tarda tanto en llegar como lo que nunca se empieza.";
	frases[12] = "El genio consta de un 1% de inspiración y un 99% de transpiración.";
	frases[13] = "El crecimiento constante es el mejor mecanismo de supervivencia.";
	frases[14] = "El éxito es la capacidad de ir de fracaso en fracaso sin perder entusiasmo.";
	frases[15] = "Nada muere más rápidamente que una idea en una mente cerrada.";
	frases[16] = "El mejor momento del día es ahora.";
	frases[17] = "Nunca conseguirás seguir adelante si siempre piensas en la venganza.";
	frases[18] = "Elige un trabajo que te guste, y nunca tendrás que volver a trabajar en tu vida.";
	frases[19] = "Los ganadores nunca abandonan y los que abandonan nunca ganan.";
	frases[20] = "Visualizar el final es suficiente para poner en marcha los medios.";
	
	
	//calculando el random
	index = Math.floor(Math.random() * frases.length);
	console.log(index)
	//mostrar las citas
	$(elemento).html("");
	$(elemento).html("<span>"+frases[index]+"</span>");
}