$.noConflict();
$(document).ready(function() {
	$(".oculto").hide();
	$("#subir").hide();

	
	FrasesAleatorias("#slogan");
	$("#slogan").click(function () {
		FrasesAleatorias(this);
	});
	
	
	//Darle el alto y ancho POPUPINFOTUTOR
	$("#popupinfotutor").css('width', 'auto');
	$("#popupinfotutor").css('height', 'auto');
	
	$(".infotutor").mouseover(function() {
		$("#popupinfotutor").css("visibility","visible");
		$("#popupinfotutor").fadeIn();
		SacarPosicionInfoTutor(this);
		var idasignatura = $(this).attr("id");
		InformacionTutores(idasignatura);
	});
	$(".infotutor").mouseout(function() {
		var id = $(this).attr("id");
		$("#popupinfotutor").fadeOut(0);
		$("#popupinfotutor").css("visibility","hidden");
		$("#popupinfotutor").html("");
	});
	
	
	//Darle el alto y ancho POPUPINFOUSUARIO
	$("#popup").css('width', 350 + 'px');
	$("#popup").css('height', 'auto');
	
	$(".usuario").mouseover(function() {
		$("#popup").css("visibility","visible");
		$("#popup").fadeIn();
		SacarPosicion(this);
		var id = $(this).attr("id");
		InformacionUsuario(id);
	});
	$(".usuario").mouseout(function() {
		var id = $(this).attr("id");
		$("#popup").fadeOut(0);
		$("#popup").css("visibility","hidden");
		$("#popup").html("");
	});
	
	
	//POPUPVISITANTES
	$(".numerovisitas").click(function () {
		var idnumerovisitas = $(this).attr("id");
		MostrarVisitasUsuarios(idnumerovisitas);
		SacarPosicionVisitantes(this);
		$("#popupvisitantes").toggle();
	});
	
	
	//FUNCIÓN PARA SUBIR SCROLL DE PÁGINA
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
	
	MostrarEstiloUsuario(usuario);
	
});

function MostrarVisitasUsuarios(idnumerovisitas){
	var parseEntrada = idnumerovisitas.split("-"); 
	var identrada = parseEntrada[1]
	console.log(idnumerovisitas)
	$.ajax({
		data: {'identrada':identrada},
		url: '/planetablogs/mostrarvisitasusuarios/',
		type: 'GET',
		success: function(datos){
			var lista_visitantes = datos.split("|")
			var html = "<table class='table'><thead><tr><th style='font: small-caps 100%/200% serif;color:black;font-weight:bold;' class='centrar'>Visitantes</th></tr></thead><tbody>"
			$("#"+idnumerovisitas).html(lista_visitantes.length-1)
			if (lista_visitantes != "") {
				for (i=0;i<(lista_visitantes.length-1);i++){
					html += "<tr><td style='font-size:12px !important;font: bold 90% monospace;color:#B9C5CD;font-style:oblique;'>"+lista_visitantes[i]+"</td></tr>";
				}
				html += "</tbody></table>";
				$("#popupvisitantes").html(html)
			}
			else {
				html += "<tr><td style='font-size:12px !important;font: bold 90% monospace;color:#ff4d4d;font-style:oblique;'>Esta entrada no tiene visitantes</td></tr>";
				html += "</tbody></table></div>";
				$("#popupvisitantes").html(html)
			}
		},
	});
}

function MostrarEstiloUsuario(usuario) {
	for (i=0;i<disenos.length;i++){
		if (usuario[0].fields.estilo == disenos[i].fields.estilo){
			$("body").prepend("<img id='fondo' src='../../../../../static/imagenes/"+disenos[i].fields.imagen+"'/>");
			break;
		}
	}
}

function MostrarComentarios(id) {
	var totalcomentarios = parseInt($("#totalcomentarios"+id).text())
	if($("#desplieguecomentarios"+id).is(":visible") ){
		$("#despliegueboton"+id).html("<span class='glyphicon glyphicon-arrow-down'></span> Mostrar comentarios (<span id='totalcomentarios"+id+"'>"+totalcomentarios+"</span>)");
	}else{
		$("#despliegueboton"+id).html("<span class='glyphicon glyphicon-arrow-up'></span> Ocultar comentarios (<span id='totalcomentarios"+id+"'>"+totalcomentarios+"</span>)");
	}
	if(totalcomentarios == 0){
		$("#comentariosentrada"+id).html("<div id=nohaycomen"+id+"><p style='text-align:center;font-size:9px;font-weight:bold:font-style:oblique;color:red;'>No hay comentarios en esta entrada.</p></div>");
	}
	var str = $("#comentariosentrada"+id).text()
	var cadena = str.replace(/\s/g, '');
	if(cadena == ''){
		$("#comentariosentrada"+id).html("<div id=nohaycomen"+id+"><p style='text-align:center;font-size:9px;font-weight:bold:font-style:oblique;color:red;'>No hay comentarios en esta entrada. !Sé el primero en escribir!</p></div>");
	}
	$("#desplieguecomentarios"+id).toggle("fast","swing");
}

function MostrarAnimacion(){
	$("#popupanim").fadeIn(250);
	$("#popupanim").fadeOut(3750);
}

function SacarPosicion(elemento){
	var offset = $(elemento).offset();
	var x = offset.left + 235;
	var y = offset.top - 125;
	$("#popup").css("left",x + "px");
	$("#popup").css("top",y + "px");
}

function SacarPosicionInfoTutor(elemento){
	var offset = $(elemento).offset();
	var x = offset.left - 300;
	var y = offset.top + 25;
	$("#popupinfotutor").css("left",x + "px");
	$("#popupinfotutor").css("top",y + "px");
}

function SacarPosicionUp(elemento){
	var offset = $(elemento).offset();
	var x = offset.left - 45;
	var y = offset.top - 50;
	$("#popupUP").css("left",x + "px");
	$("#popupUP").css("top",y + "px");
	$("#popupUP").show()
	$("#popupUP").animate({top:'-=30px'},1000,function(){$("#popupUP").hide();});
}

function SacarPosicionDown(elemento){
	var offset = $(elemento).offset();
	var x = offset.left - 45;
	var y = offset.top - 50;
	$("#popupDOWN").css("left",x + "px");
	$("#popupDOWN").css("top",y + "px");
	$("#popupDOWN").show()
	$("#popupDOWN").animate({top:'-=30px'},1000,function(){$("#popupDOWN").hide();});
}

function SacarPosicionAnimacion(elemento){
	var offset = $(elemento).offset();
	var x = offset.left - 187;
	var y = offset.top;
	$("#popupanim").css("left",x + "px");
	$("#popupanim").css("top",y + "px");
}

function SacarPosicionVisitantes(elemento){
	var offset = $(elemento).offset();
	var x = offset.left + 18;
	var y = offset.top;
	$("#popupvisitantes").css("left",x + "px");
	$("#popupvisitantes").css("top",y + "px");
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
			$("#popupinfotutor").append(html);
			break;
		}
	}
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
					var html = "<div class='panel-heading popupcabecera'><div class='panel-title'><img src='../../../../../static/imagenes/"+usuarios[i].fields.imagen+"' class='fotogrande'> </img><span style=margin-left:45px;'>Información de usuario</span></div></div>";
					html += "<div style='font-family: Verdana, Arial, Helvetica, sans-serif;font-size:11px;' class='panel-body'><span style='font-weight:bold;' class='pull-left'>Usuario:</span><span>&nbsp; "+usuarios[i].fields.first_name+" "+usuarios[i].fields.last_name+"</span></br>";
					html += "<span style='font-weight:bold;' class='pull-left'>Correo:</span><span>&nbsp; "+usuarios[i].fields.email+"</span></br>";
					if (usuarios[i].fields.username != "admin"){
						html += "<span style='font-weight:bold;' class='pull-left'>Puntos:</span><span>&nbsp; "+valoraciones[j].fields.puntos+"</span></br>";
						html += "<span style='font-weight:bold;' class='pull-left'>Nivel:</span><span>&nbsp; "+valoraciones[j].fields.nivel+"</span></div>";
					}
					$("#popup").append(html);
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

function Up(identrada,idusuario,idasignatura,up,down,valortutor){
	var up1 = parseInt(up) + parseInt(1)
	$.ajax({
		data: {'identrada':identrada,'idusuario':idusuario,'idasignatura':idasignatura,'up':up},
		url: '/planetablogs/up/',
		type: 'GET',
		success: function(datos){
			SacarPosicionUp("#up"+identrada);
			if (valortutor == 0){
				var html = "<div class='btn-group'><button type='button' disabled='disabled' class='btn btn-success btn-xs'><span class='badge'>"+up1+"</span></button></div> <div class='btn-group'><button type='button' disabled='disabled' class='btn btn-danger btn-xs'><span class='badge'>"+down+"</span></button></div><div class='btn-group'><button type='button' disabled='disabled' class='btn btn-primary btn-xs'><span style='color:black;' class='badge'> SC </span></button></div></div>"
				$("#updown"+identrada).html(html);
			}
			else {
				var html = "<div class='btn-group'><button type='button' disabled='disabled' class='btn btn-success btn-xs'><span class='badge'>"+up1+"</span></button></div> <div class='btn-group'><button type='button' disabled='disabled' class='btn btn-danger btn-xs'><span class='badge'>"+down+"</span></button></div><div class='btn-group'><button type='button' disabled='disabled' class='btn btn-warning btn-xs'><span style='color:black;' class='badge'>"+valortutor+"</span></button></div></div>"
				$("#updown"+identrada).html(html);
			}
			
		},
	});
}

function Down(identrada,idusuario,idasignatura,up,down,valortutor){
	var down1 = parseInt(down) + parseInt(1)
	$.ajax({
		data: {'identrada':identrada,'idusuario':idusuario,'idasignatura':idasignatura,'down':down},
		url: '/planetablogs/down/',
		type: 'GET',
		success: function(datos){
			SacarPosicionDown("#down"+identrada);
			if (valortutor == 0){
				var html = "<div class='btn-group'><button type='button' disabled='disabled' class='btn btn-success btn-xs'><span class='badge'>"+up+"</span></button></div> <div class='btn-group'><button type='button' disabled='disabled' class='btn btn-danger btn-xs'><span class='badge'>"+down1+"</span></button></div><div class='btn-group'><button type='button' disabled='disabled' class='btn btn-primary btn-xs'><span style='color:black;' class='badge'> SC </span></button></div></div>"
				$("#updown"+identrada).html(html);
			}
			else {
				var html = "<div class='btn-group'><button type='button' disabled='disabled' class='btn btn-success btn-xs'><span class='badge'>"+up+"</span></button></div> <div class='btn-group'><button type='button' disabled='disabled' class='btn btn-danger btn-xs'><span class='badge'>"+down1+"</span></button></div><div class='btn-group'><button type='button' disabled='disabled' class='btn btn-warning btn-xs'><span style='color:black;' class='badge'>"+valortutor+"</span></button></div></div>"
				$("#updown"+identrada).html(html);
			}
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
			if (descripcion==""){
				$("#infoescribircomen"+identrada).remove();
				$("#comentariosentrada"+identrada).prepend("<h5 id=infoescribircomen"+identrada+" style='color:red;text-align:center;font-style:oblique;font-size:10px;'>Escribe tu comentario antes de enviar.</h5>"); 
			}
			else{
				var descripcionConSaltos = ConvertirDescripcion(datos.comentario[0].fields.descripcion);
				SacarPosicionAnimacion("#descripcion_comentario"+identrada);
				MostrarAnimacion();
				$("#infoescribircomen"+identrada).remove();
				var totalcomentarios = parseInt($("#totalcomentarios"+identrada).text()) + 1
				$("#nohaycomen"+identrada).html("");
				$("#descripcion_comentario"+identrada).val("");
				$("#despliegueboton"+identrada).html("<span class='glyphicon glyphicon-arrow-up'></span> Ocultar comentarios (<span id='totalcomentarios"+identrada+"'>"+totalcomentarios+"</span>)");
				BorrarInfo();
				var html = "</br><div id='comentario"+datos.comentario[0].pk+"' class='panel panel-warning'>";
				html += "<div id='titulopanel' class='panel-heading'><div class='panel-title'>Comentario publicado por "+datos.comentario[0].fields.username+"<span class='pull-right'>"+fecha+"</span></div></div>";
				html += "<div style='margin-right:3px;margin-left:3px;font-family:monospace;font-size:11px;word-wrap:break-word;' class='panel-body'>"+descripcionConSaltos+"</br><button id='"+datos.comentario[0].pk+"' onclick='EliminarComentario("+datos.comentario[0].pk+","+datos.comentario[0].fields.asignatura+","+identrada+")' type='button' style='font-family:verdana !important;' class='btn btn-danger btn-xs pull-right'>Eliminar comentario</button></div></div>";
				html += "<div id='infocomentario"+datos.comentario[0].pk+"' class='info oculto'><div class='alert alert-success alert-dismissable'><button type='button' class='close' data-dismiss='alert'>&times;</button><strong>¡Comentario borrado! </strong><em>Se te restarán 3 planets.</em> Vuelve a comentar cuando lo desees.</div></div>";
				$("#comentariosentrada"+identrada).prepend(html);
				$("#infocomentario"+datos.comentario[0].pk).hide();
			}
		},
	});
}

function ConvertirDescripcion(descripcion) {
	var unixNewLine = new RegExp("\n", "g");
	descripcionConSaltos = descripcion.replace(unixNewLine, '<br/>');
	return descripcionConSaltos
}


function ConvertirFecha() {
	var nombres_dias = new Array('Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado');
	var nombres_meses = new Array('Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre');
	var now = new Date();
	if (now.getMinutes()<10){ var minutos = '0' + now.getMinutes()}
	else { var minutos = now.getMinutes() }
	if (now.getHours()<10){ var horas = '0' + now.getHours()}
	else { var horas = now.getHours() }
	var fecha =  now.getDate() + " de " + nombres_meses[now.getMonth()] + " de " + now.getFullYear() + ", " + nombres_dias[now.getDay()] + " a las " + horas + ":" + minutos;
	return fecha;
}

function EliminarComentario(idcomentario,idasignatura,identrada){
	$("#infoescribircomen"+identrada).remove();
	var totalcomentarios = parseInt($("#totalcomentarios"+identrada).text()) - 1
	$("#despliegueboton"+identrada).html("<span class='glyphicon glyphicon-arrow-up'></span> Ocultar comentarios (<span id='totalcomentarios"+identrada+"'>"+totalcomentarios+"</span>)");
	$('#comentario'+idcomentario).remove();
	$('#infocomentario'+idcomentario).show("slow").delay(2000).hide("slow");
	$.ajax({
		data: {'idcomentario':idcomentario,'idasignatura':idasignatura,'identrada':identrada},
		url: '/planetablogs/eliminarcomentario/',
		type: 'GET',
		success: function(datos){
			/*if(totalcomentarios == 0){
				$("#comentariosentrada"+identrada).delay(2500).queue(function(n) {
					$(this).html("<div id=nohaycomen"+identrada+"><p style='text-align:center;font-size:9px;font-weight:bold:font-style:oblique;color:red;'>No hay comentarios en esta entrada.</p></div>");
				})
			}*/
		},
	});
}

function BorrarInfo(){
	$(".info").remove();
}

function FrasesAleatorias(elemento){
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
	//mostrar las citas
	$(elemento).html("");
	$(elemento).html("<span>"+frases[index]+"</span>");
}

function EntradaLeida(identrada,idusuario,idasignatura,visita){	
	var numero = $("#numerovisitas-"+identrada).text();
	$.ajax({
		data: {'identrada':identrada,'idusuario':idusuario,'idasignatura':idasignatura,'visita':visita},
		url: '/planetablogs/entradaleida/',
		type: 'GET',
		datatype: 'json',
		success: function(datos){
			var html = "<button style='text-align:center;' disabled='disabled' type='button' class='btn fotopequeña'><span class='glyphicon glyphicon-eye-close'></span></button>";
			$("#lecturaentrada"+identrada).html(html);
			if (visita == "true"){
				var lista_usuarios_estado_anterior = datos[0].fields.visitantes
				var encontrado = ComprobarVisitasUsuario(idusuario,lista_usuarios_estado_anterior)
				if (encontrado != true) {
					$("#numerovisitas-"+identrada).html(parseInt(numero)+1);
				}
			}
		},
	});
}

function ComprobarVisitasUsuario(idusuario,lista_usuarios) {
	var resultado = (lista_usuarios.search("'"+idusuario+"'"))
	if (resultado == -1){
		var encontrado = false
	}
	else{
		var encontrado = true
	}
	return encontrado
}