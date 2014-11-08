$(document).ready(function(){
	$("#intercabecera").hide();
	$("#iden").click(function(event){
		$("#intercabecera").toggle("blind");
	});
	$("#boton_iden").click(function(event){
		nick = document.getElementById("intro_nick").value;
		contra = document.getElementById("intro_pass").value;
		$.ajax({
			data: {'nick':nick,'password':contra},
			url: '/planetablogs',
			type: 'get',
			success: function(data){
				console.log(data)
			}
		})
		CompararNick(nick,contra);
	});
});

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

function Up(identrada,idusuario){
	for (var i=0;i<usuario.length;i++){
		var usu = usuario[i]
		if (usu.pk == idusuario){
			usu.fields.puntuaciontotal += 3
			usu.save()
			break;
		}
	}
	for (var i=0;i<entrada.length;i++){
		var ent = entrada[i]
		if (ent.pk == identrada){
			ent.fields.up += 1
			ent.save()
			break;
		}
	}
	//$("#up").append("<a href="+url_blog+">"+nombre+"</a>");
}

function Down(identrada,idusuario){

}