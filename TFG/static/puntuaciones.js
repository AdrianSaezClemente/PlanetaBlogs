$.noConflict();
$(document).ready(function() {
	
	$("#nivel").mouseover(function() {
		var nivel = $("#nivel").text()
		console.log(nivel)
		if nivel == 0 {$(this).addClass("nivel0");}
		if nivel == 1 {$(this).addClass("nivel1");}
		if nivel == 2 {$(this).addClass("nivel2");}
		if nivel == 3 {$(this).addClass("nivel3");}
		if nivel == 4 {$(this).addClass("nivel4");}
		if nivel == 5 {$(this).addClass("nivel5");}
		if nivel == 6 {$(this).addClass("nivel6");}
		if nivel == 7 {$(this).addClass("nivel7");}
		if nivel == 8 {$(this).addClass("nivel8");}
		if nivel == 9 {$(this).addClass("nivel9");}
		if nivel == 10 {$(this).addClass("nivel10");}
		if nivel == 11 {$(this).addClass("nivel11");}
	})

});