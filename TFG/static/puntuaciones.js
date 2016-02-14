$.noConflict();
$(document).ready(function() {

	$("#popup").hide()
	
	
	//Darle el alto y ancho
	$("#popup").css('width', 166 + 'px');
	$("#popup").css('height', 166 + 'px');
	
	$(".foto").mouseover(function() {
		$("#popup").css("visibility","visible");
		$("#popup").fadeIn();
		SacarPosicion(this);
		var id = $(this).attr("id");
		InformacionUsuario(id);
	});
	$(".foto").mouseout(function() {
		var id = $(this).attr("id");
		$("#popup").fadeOut(0);
		$("#popup").css("visibility","hidden");
		$("#popup").html("");
	});
	
	
	$(".nivel").mouseover(function() {
		var nivel = $(this).html()
		console.log(nivel)
		if (nivel == 0) {$(this).addClass("nivel0");}
		if (nivel == 1) {$(this).addClass("nivel1");}
		if (nivel == 2) {$(this).addClass("nivel2");}
		if (nivel == 3) {$(this).addClass("nivel3");}
		if (nivel == 4) {$(this).addClass("nivel4");}
		if (nivel == 5) {$(this).addClass("nivel5");}
		if (nivel == 6) {$(this).addClass("nivel6");}
		if (nivel == 7) {$(this).addClass("nivel7");}
		if (nivel == 8) {$(this).addClass("nivel8");}
		if (nivel == 9) {$(this).addClass("nivel9");}
		if (nivel == 10) {$(this).addClass("nivel10");}
		if (nivel == 11) {$(this).addClass("nivel11");}
		if (nivel == 12) {$(this).addClass("nivel12");}
	});
	$(".nivel").mouseout(function() {
		var nivel = $(this).html()
		if (nivel == 0) {$(this).removeClass("nivel0");}
		if (nivel == 1) {$(this).removeClass("nivel1");}
		if (nivel == 2) {$(this).removeClass("nivel2");}
		if (nivel == 3) {$(this).removeClass("nivel3");}
		if (nivel == 4) {$(this).removeClass("nivel4");}
		if (nivel == 5) {$(this).removeClass("nivel5");}
		if (nivel == 6) {$(this).removeClass("nivel6");}
		if (nivel == 7) {$(this).removeClass("nivel7");}
		if (nivel == 8) {$(this).removeClass("nivel8");}
		if (nivel == 9) {$(this).removeClass("nivel9");}
		if (nivel == 10) {$(this).removeClass("nivel10");}
		if (nivel == 11) {$(this).removeClass("nivel11");}
		if (nivel == 12) {$(this).removeClass("nivel12");}
	});
	
	MostrarEstiloUsuario(usuario);
});

function SacarPosicion(elemento){
	var offset = $(elemento).offset();
	var x = offset.left - 60;
	var y = offset.top + 40;
	$("#popup").css("left",x + "px");
	$("#popup").css("top",y + "px");
}

function InformacionUsuario(id){
	for (i=0;i<usuarios.length;i++){
		if (usuarios[i].pk == id){
			var html = "<img src='../../../../../static/imagenes/"+usuarios[i].fields.imagen+"' class='fotogrande'> </img>";
			$("#popup").append(html);
			$("#popup").fadeIn();
			break;
		}
	}
}

function MostrarEstiloUsuario(usuario) {
	for (i=0;i<disenos.length;i++){
		if (usuario[0].fields.estilo == disenos[i].fields.estilo){
			$("body").prepend("<img id='fondo' src='../../../../../static/imagenes/"+disenos[i].fields.imagen+"'/>");
			break;
		}
	}
}