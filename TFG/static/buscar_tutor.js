					
$(document).ready(function() {
	$(".oculto").hide();
	$("#subir").hide();
	console.log("subir")
	idopcion = $('select').val();
	$('select').on('change',Dameidopcion);
	console.log(idopcion)
	function Dameidopcion() {
		idopcion = $(this).val();
	}
	
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

	
function Buscar(idasignatura,iduser){
	console.log("hola")
	var texto = $("#texto").val();
	if(idopcion == 1){
		$.ajax({
			data: {'idopcion':idopcion, 'texto':texto, 'idasignatura':idasignatura},
			url: '/planetablogs/buscarNickUsuario/',
			type: 'GET',
			success: function(datos){
				$("#resultado").html("");
				if (texto==""){
					$("#resultado").append("<h5 style='color:red;text-align:center;font-style:oblique;'>Elige una opción y escribe un texto antes de buscar, por favor.</h5>"); 
				}
				if(datos.entradas.length == 0 & texto!=""){
					$("#resultado").append("<h5 style='color:red;text-align:center;font-style:oblique;'>"+texto+" no existe o no tiene ninguna entrada.</h5>"); 
				}
				else{
					console.log("hola")
					datos.comentarios = datos.comentarios.reverse()
					datos.entradas = datos.entradas.reverse();
					for (var i=0; i<datos.entradas.length; i++){
						var fecha = ConvertirFecha(datos.entradas[i].fields.fecha);
						var descripcionConSaltos = ConvertirDescripcion(datos.entradas[i].fields.descripcion);
						var html = "<div class='blog-post'><div id='entrada'><h2 class='blog-post-title'><label id='label'>#"+datos.entradas[i].fields.entrada+"&nbsp;<img src=../../../../../static/imagenes/"+datos.usuario[0].fields.imagen+" class='fotopequeña'> </img></label><a target='_blank' href='"+datos.entradas[i].fields.url_blog+"'> "+datos.usuario[0].fields.first_name+" "+datos.usuario[0].fields.last_name+"</a><span class='blog-post-meta'>"+fecha+" por <a target='_blank' href='"+datos.entradas[i].fields.url_blog+"'><strong>"+datos.usuario[0].fields.username+"</strong></a></span></h2>";
						html += "<h3><a target='_blank' href='"+datos.entradas[i].fields.link+"'>"+datos.entradas[i].fields.titulo+"</a></h3>";
						html += "<p id='entradadescripcion"+datos.entradas[i].pk+"' style='word-wrap:break-word;'>"+descripcionConSaltos+"</p>";
						html += "<div id='valoracion'><div class='btn-toolbar' role='toolbar'><div class='btn-group'><button type='button' disabled='disabled' class='btn btn-success btn-xs'><span class='badge'>"+datos.entradas[i].fields.totalup+"</span></button></div><div class='btn-group'><button type='button' disabled='disabled' class='btn btn-danger btn-xs'><span class='badge'>"+datos.entradas[i].fields.totaldown+"</span></button></div></div></div>";
						var htmlInfo = InfoEntrada(datos.entradas[i].pk,datos.entradas[i]);
						htmlInfo += "<div id='comentariosentrada"+datos.entradas[i].pk+"'>";
						var htmlComentarios = ObtenerComentarios(datos.comentarios,datos.entradas[i].pk,idasignatura);
						$("#resultado").append(html+htmlInfo+htmlComentarios);
					}
				}
			},
		});
	}
	if(idopcion == 2){
		var texto = $("#texto").val();
		$.ajax({
			data: {'idopcion':idopcion, 'texto':texto, 'idasignatura':idasignatura},
			url: '/planetablogs/buscarIdEntrada/',
			type: 'GET',
			success: function(datos){
				$("#resultado").html("");
				if (texto==""){
					$("#resultado").append("<h5 style='color:red;text-align:center;font-style:oblique;'>Elige una opción y escribe un texto antes de buscar, por favor.</h5>"); 
				}
				if (datos.entrada.length == 0 & texto!=""){
					$("#resultado").append("<h5 style='color:red;text-align:center;font-style:oblique;'>No hay ninguna entrada con identificador #"+texto+". La entrada ha sido eliminada o nunca existió.</h5>"); 
				}
				else{
					datos.comentarios = datos.comentarios.reverse()
					var fecha = ConvertirFecha(datos.entrada[0].fields.fecha);
					var descripcionConSaltos = ConvertirDescripcion(datos.entrada[0].fields.descripcion);
					var html = "<div class='blog-post'><div id='entrada'><h2 class='blog-post-title'><label id='label'>#"+datos.entrada[0].fields.entrada+"&nbsp;<img src=../../../../../static/imagenes/"+datos.usuario[0].fields.imagen+" class='fotopequeña'> </img></label><a target='_blank' href='"+datos.entrada[0].fields.url_blog+"'> "+datos.usuario[0].fields.first_name+" "+datos.usuario[0].fields.last_name+"</a><span class='blog-post-meta'>"+fecha+" por <a target='_blank' href='"+datos.entrada[0].fields.url_blog+"'><strong>"+datos.usuario[0].fields.username+"</strong></a></span></h2>";
					html += "<h3><a target='_blank' href='"+datos.entrada[0].fields.link+"'>"+datos.entrada[0].fields.titulo+"</a></h3>";
					html += "<p id='entradadescripcion"+datos.entrada[0].pk+"' style='word-wrap:break-word;'>"+descripcionConSaltos+"</p>";
					html += "<div id='valoracion'><div class='btn-toolbar' role='toolbar'><div class='btn-group'><button type='button' disabled='disabled' class='btn btn-success btn-xs'><span class='badge'>"+datos.entrada[0].fields.totalup+"</span></button></div><div class='btn-group'><button type='button' disabled='disabled' class='btn btn-danger btn-xs'><span class='badge'>"+datos.entrada[0].fields.totaldown+"</span></button></div></div></div>";
					var htmlInfo = InfoEntrada(datos.entrada[0].pk,datos.entrada[0]);
						htmlInfo += "<div id='comentariosentrada"+datos.entrada[0].pk+"'>";
						var htmlComentarios = ObtenerComentarios(datos.comentarios,datos.entrada[0].pk,idasignatura);
						$("#resultado").append(html+htmlInfo+htmlComentarios);
				}
			},
		});
	}
	if(idopcion == 3){
		$.ajax({
			data: {'idopcion':idopcion, 'texto':texto},
			url: '/planetablogs/buscarNombreUsuario/',
			type: 'GET',
			success: function(datos){
				console.log("exitoso")
				$("#resultado").html("");
				if (texto==""){
					$("#resultado").append("<h5 style='color:red;text-align:center;font-style:oblique;'>Elige una opción y escribe un texto antes de buscar, por favor.</h5>"); 
				}
				if(datos.entradas.length == 0 & texto!=""){
					$("#resultado").append("<h5 style='color:red;text-align:center;font-style:oblique;'>"+texto+" no existe o no tiene ninguna entrada.</h5>"); 
				}
				else{
					for (var i=0; i<datos.entradas.length; i++){
						var descripcionConSaltos = ConvertirDescripcion(datos.entradas[i].fields.descripcion);
						var html = "<div class='blog-post'><div id='entrada'><h2 class='blog-post-title'><label>#"+datos.entradas[i].fields.entrada+"</label><a target='_blank' href='"+datos.usuario[0].fields.url_blog+"'> "+datos.entradas[i].alumno+"</a><span class='blog-post-meta'>"+datos.entradas[i].fields.fecha+" por <a target='_blank' href='"+datos.usuario[0].fields.url_blog+"'>"+datos.usuario[0].fields.nick+"</a></span></h2>";
						html += "<h3><a target='_blank' href='"+datos.entradas[i].fields.link+"'>"+datos.entradas[i].fields.titulo+"</a></h3>";
						html += "<p>"+descripcionConSaltos+"</p></div></div>";
						$("#resultado").append(html); 
					}
				}
			},
		});
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

function EliminarComentario(idcomentario,idasignatura,identrada){
	$("#infoescribircomen"+identrada).remove();
	var totalcomentarios = parseInt($("#totalcomentarios"+identrada).text()) - 1
	$("#despliegueboton"+identrada).html("<span class='glyphicon glyphicon-arrow-up'></span> Ocultar comentarios (<span id='totalcomentarios"+identrada+"'>"+totalcomentarios+"</span>)");
	$('#comentario'+idcomentario).remove();
	//$('#infocomentario'+idcomentario).show("slow").delay(2000).hide("slow");
	$.ajax({
		data: {'idcomentario':idcomentario,'idasignatura':idasignatura,'identrada':identrada},
		url: '/planetablogs/eliminarcomentario/',
		type: 'GET',
		success: function(datos){

		},
	});
}

function InfoEntrada(identrada,entrada){
	var html = "<button id=despliegueboton"+identrada+" onclick=MostrarComentarios("+identrada+"); style='background-color:#A8ADB1;color:white;' class='col-sm-12 btn btn-xs'><span class='glyphicon glyphicon-arrow-up'></span> Ocultar comentarios (<span id='totalcomentarios"+identrada+"'>"+entrada.fields.totalcomentarios+"</span>)</button></br></br>";
	html += "<div class='oculto' id='desplieguecomentarios"+identrada+"'>";
	return html
}

function ObtenerComentarios(lista_comentarios,identrada,idasignatura){
	var html = ""
	var lista_comentarios = lista_comentarios.reverse()
	for (var i=0; i<lista_comentarios.length; i++){
		if (identrada == lista_comentarios[i].fields.entrada){
			var descripcionConSaltos = ConvertirDescripcion(lista_comentarios[i].fields.descripcion);
			var fecha = ConvertirFechaMilisec(lista_comentarios[i].fields.fecha);
			html += "<div id='comentarios'><div id='comentario"+lista_comentarios[i].pk+"' class='panel panel-warning'>";
			html += "<div id='titulopanel' class='panel-heading'><div class='panel-title'>Comentario publicado por "+lista_comentarios[i].fields.username+"<span class='pull-right'>"+fecha+"</span></div></div>";
			html += "<div style='margin-bottom:10px;margin-left:10px;margin-right:10px;font-family:verdana;font-size:12px;word-wrap:break-word;' class='panel-body'>";
			html += descripcionConSaltos+"</br><button id="+lista_comentarios[i].pk+" onclick=EliminarComentario('"+lista_comentarios[i].pk+"','"+idasignatura+"','"+identrada+"') type='button' class='btn btn-danger btn-xs pull-right'>Eliminar comentario</button></div></div></div>"
		}
	}
	html += "</div></div></div></div>";
	return html
}

function ConvertirDescripcion(descripcion) {
	var unixNewLine = new RegExp("\n", "g");
	descripcionConSaltos = descripcion.replace(unixNewLine, '<br/>');
	return descripcionConSaltos
}

function ConvertirFecha(fecha) {
	var nombres_dias = new Array('Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado');
	var nombres_meses = new Array('Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre');
	var now = new Date((fecha || "").replace(/-/g,"/").replace(/[TZ]/g," "));
	if (now.getMinutes()<10){ var minutos = '0' + now.getMinutes()}
	else { var minutos = now.getMinutes() }
	if ((now.getHours()+1<10) && (now.getHours()!=23)) { var horas = '0' + now.getHours()+1}
	else if (now.getHours()+1>23){var horas = '00'}
	else { var horas = now.getHours()+1 }
	var fecha =  now.getDate() + " de " + nombres_meses[now.getMonth()] + " de " + now.getFullYear() + ", " + nombres_dias[now.getDay()] + " a las " + horas + ":" + minutos;
	return fecha;
}

function ConvertirFechaMilisec(fecha) {
	var nombres_dias = new Array('Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado');
	var nombres_meses = new Array('Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre');
	var prueba = (fecha || "").replace(/-/g,"/").replace(/[TZ]/g," ").replace(/\./g," ")
	var fecha = prueba.split(" ");
	fechaFinal = fecha[0]+" "+fecha[1]+" "
	var now = new Date(fechaFinal);
	if (now.getMinutes()<10){ var minutos = '0' + now.getMinutes()}
	else { var minutos = now.getMinutes() }
	if ((now.getHours()+1<10) && (now.getHours()!=23)) { var horas = '0' + now.getHours()+1}
	else if (now.getHours()+1>23){var horas = '00'}
	else { var horas = now.getHours()+1 }
	var fecha =  now.getDate() + " de " + nombres_meses[now.getMonth()] + " de " + now.getFullYear() + ", " + nombres_dias[now.getDay()] + " a las " + horas + ":" + minutos;
	return fecha;
}