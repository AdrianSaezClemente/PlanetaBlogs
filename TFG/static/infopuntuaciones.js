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
	
	$("#nivel0").mouseover(function() {$( this ).addClass("nivel0");})
	$("#nivel0").mouseout(function() {$( this ).removeClass("nivel0");});
	
	$("#nivel1").mouseover(function() {$( this ).addClass("nivel1");})
	$("#nivel1").mouseout(function() {$( this ).removeClass("nivel1");});
	
	$("#nivel2").mouseover(function() {$( this ).addClass("nivel2");})
	$("#nivel2").mouseout(function() {$( this ).removeClass("nivel2");});
	
	$("#nivel3").mouseover(function() {$( this ).addClass("nivel3");})
	$("#nivel3").mouseout(function() {$( this ).removeClass("nivel3");});
	
	$("#nivel4").mouseover(function() {$( this ).addClass("nivel4");})
	$("#nivel4").mouseout(function() {$( this ).removeClass("nivel4");});
	
	$("#nivel5").mouseover(function() {$( this ).addClass("nivel5");})
	$("#nivel5").mouseout(function() {$( this ).removeClass("nivel5");});
	
	$("#nivel6").mouseover(function() {$( this ).addClass("nivel6");})
	$("#nivel6").mouseout(function() {$( this ).removeClass("nivel6");});
	
	$("#nivel7").mouseover(function() {$( this ).addClass("nivel7");})
	$("#nivel7").mouseout(function() {$( this ).removeClass("nivel7");});
	
	$("#nivel8").mouseover(function() {$( this ).addClass("nivel8");})
	$("#nivel8").mouseout(function() {$( this ).removeClass("nivel8");});
	
	$("#nivel9").mouseover(function() {$( this ).addClass("nivel9");})
	$("#nivel9").mouseout(function() {$( this ).removeClass("nivel9");});
	
	$("#nivel10").mouseover(function() {$( this ).addClass("nivel10");})
	$("#nivel10").mouseout(function() {$( this ).removeClass("nivel10");});
	
	$("#nivel11").mouseover(function() {$( this ).addClass("nivel11");})
	$("#nivel11").mouseout(function() {$( this ).removeClass("nivel11");});
	
	$("#nivel12").mouseover(function() {$( this ).addClass("nivel12");})
	$("#nivel12").mouseout(function() {$( this ).removeClass("nivel12");});
	
	$("#nivel13").mouseover(function() {$( this ).addClass("nivel13");})
	$("#nivel13").mouseout(function() {$( this ).removeClass("nivel13");});
	
	$("#nivel14").mouseover(function() {$( this ).addClass("nivel14");})
	$("#nivel14").mouseout(function() {$( this ).removeClass("nivel14");});
	
	$("#nivel15").mouseover(function() {$( this ).addClass("nivel15");})
	$("#nivel15").mouseout(function() {$( this ).removeClass("nivel15");});
	
	$("#nivel16").mouseover(function() {$( this ).addClass("nivel16");})
	$("#nivel16").mouseout(function() {$( this ).removeClass("nivel16");});
	
	$("#nivel17").mouseover(function() {$( this ).addClass("nivel17");})
	$("#nivel17").mouseout(function() {$( this ).removeClass("nivel17");});
	
	$("#nivel18").mouseover(function() {$( this ).addClass("nivel18");})
	$("#nivel18").mouseout(function() {$( this ).removeClass("nivel18");});
	
	$("#nivel19").mouseover(function() {$( this ).addClass("nivel19");})
	$("#nivel19").mouseout(function() {$( this ).removeClass("nivel19");});
	
	$("#nivel20").mouseover(function() {$( this ).addClass("nivel20");})
	$("#nivel20").mouseout(function() {$( this ).removeClass("nivel20");});

});