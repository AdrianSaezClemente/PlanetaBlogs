$.noConflict();
$(document).ready(function() {

	$("#popup").hide()
	//Darle el alto y ancho
	$("#popup").css('width', 120 + 'px');
	$("#popup").css('height', 120 + 'px');
	
	$(".foto").mouseover(function() {
		SacarPosicion(this);
		var id = $(this).attr("id");
		InformacionUsuario(id);
	});
	$(".foto").mouseout(function() {
		var id = $(this).attr("id");
		$("#popup").fadeOut(200);
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
	});

});

function SacarPosicion(elemento){
	var posicion = $(elemento).position();
	var x = posicion.left + 360;
	var y = posicion.top + 250;
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