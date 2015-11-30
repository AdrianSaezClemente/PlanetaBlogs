
$(document).ready(function() {
	$("#subir").hide();
	idopcion = $("input:radio:checked").attr("id");

	if (idopcion == "opcion1"){$(".tablaentradas").hide();}
	
	if (idopcion == "opcion2"){
		$(".tablaentradas").show();
		$(".tablausuario").hide();
	}
	
	if (idopcion == "opcion3"){
		$(".tablaentradas").show();
		$(".tablausuario").show();
	}

	$("#opcion1").change(function(){
		$(".tablaentradas").hide();
		$(".tablausuario").show();
	});
	
	$("#opcion2").change(function(){
		$(".tablaentradas").show();
		$(".tablausuario").hide();
	});
	
	$("#opcion3").change(function(){
		$(".tablaentradas").show();
		$(".tablausuario").show();
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
