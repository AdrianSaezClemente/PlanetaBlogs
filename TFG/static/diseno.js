
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


function EliminarDiseno(iddiseno){
	console.log(iddiseno)
	$.ajax({
		data: {'iddiseno':iddiseno},
		url: '/planetablogs/eliminardiseno/',
		type: 'GET',
		success: function(datos){
			console.log("nah")
			$("#diseno"+iddiseno).hide();
		},
	});
	console.log("que pasa")
}