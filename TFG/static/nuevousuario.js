$(document).ready(function(){
	$("#dialog").hide();
	$("#result").hide();
	$("#nick").keypress(nickPress);
	$("#nick").keydown(nickDown);
	$("#nick").keyup(nickUp);
	//$("#contraseña").keypress(contraseñaPress);
	//$("#contraseña").keydown(contraseñaDown);
	//$("#contraseña").keyup(contraseñaUp);
	$("#imagen").mouseover(function(evento){
		$("#dialog").show({width: 590,
            height: 150,
            show: "Puff"
		});
	});
	ComprobarInfo();
})


function ComprobarInfo(){
	if (info == 'False'){
		$("#result").show("Puff");
	}
}


function ComprobarNick(){
	var entrada = document.getElementById("nick").value;
	var salida = document.getElementById("salida");
	var nick = false;
	for (var i=0;i<usuarios.length;i++){
		if (usuarios[i].fields.username == entrada){
			var nick = true;
		}
	}	
	if (nick == true){ 
		$("#salida").addClass("red");
		salida.innerHTML = "Nick ocupado"; 
	}
	else if (entrada == ""){ salida.innerHTML = "" }
	else { 
		$("#salida").addClass("green");
		salida.innerHTML = "Nick correcto" ;
	}
}

function nickDown(evento){
	$("#salida").removeClass("red");
	$("#salida").removeClass("green");
	$("#salida").html("");
}

function nickUp(evento){
	$("#salida").html("");
	$("#anima").removeClass("animacion"); 
	ComprobarNick();
}

function nickPress(evento){
	$("#anima").addClass("animacion");
	if(evento.which == 0){
		$("#anima").removeClass("animacion");
	}
}
/*
function contraseñaDown(evento){
	$("#contraseñaSalida").removeClass("animacion");
	$("#contraseñaSalida").html(""); 
}

function contraseñaUp(evento){
	$("#contraseñaSalida").removeClass("animacion");
	$("#contraseñaSalida").html(""); 
}

function contraseñaPress(evento){
	$("#contraseñaSalida").addClass("animacion");
}

*/
