					
$(document).ready(function() {
	idopcion = $('select').val();
	$('select').on('change',Dameidopcion);

	function Dameidopcion() {
		idopcion = $(this).val();
	}
});

	
function Buscar(){
	var texto = $("#texto").val();
	if(idopcion == 1){
		$.ajax({
			data: {'idopcion':idopcion, 'texto':texto},
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
					for (var i=0; i<datos.entradas.length; i++){
						var html = "<div class='blog-post'><div id='entrada'><h2 class='blog-post-title'><label id='label'>#"+datos.entradas[i].fields.entrada+"&nbsp;<img src=../../../../../static/imagenes/"+datos.usuario[0].fields.imagen+" class='fotopequeña'> </img></label><a target='_blank' href='"+datos.entradas[i].fields.url_blog+"'> "+datos.usuario[0].fields.first_name+" "+datos.usuario[0].fields.last_name+"</a><span class='blog-post-meta'>"+datos.entradas[i].fields.fecha+" por <a target='_blank' href='"+datos.entradas[i].fields.url_blog+"'>"+datos.usuario[0].fields.username+"</a></span></h2>";
						html += "<h3><a target='_blank' href='"+datos.entradas[i].fields.link+"'>"+datos.entradas[i].fields.titulo+"</a></h3>";
						html += "<p>"+datos.entradas[i].fields.descripcion+"</p>";
						html += "<div id='valoracion'><div class='btn-toolbar' role='toolbar'><div class='btn-group'><button type='button' disabled='disabled' class='btn btn-success btn-xs'><span class='badge'>"+datos.entradas[i].fields.totalup+"</span></button></div><div class='btn-group'><button type='button' disabled='disabled' class='btn btn-danger btn-xs'><span class='badge'>"+datos.entradas[i].fields.totaldown+"</span></button></div></div></div></div></div>";
						$("#resultado").append(html); 
					}
				}
			},
		});
	}
	if(idopcion == 2){
		$.ajax({
			data: {'idopcion':idopcion, 'texto':texto},
			url: '/planetablogs/buscarIdEntrada/',
			type: 'GET',
			success: function(datos){
				$("#resultado").html("");
				if (texto==""){
					$("#resultado").append("<h5 style='color:red;text-align:center;font-style:oblique;'>Elige una opción y escribe un texto antes de buscar, por favor.</h5>"); 
				}
				if(datos.entrada.length == 0 & texto!=""){
					$("#resultado").append("<h5 style='color:red;text-align:center;font-style:oblique;'>No hay ninguna entrada con identificador #"+texto+". La entrada ha sido eliminada o nunca existió.</h5>"); 
				}
				else{
					var html = "<div class='blog-post'><div id='entrada'><h2 class='blog-post-title'><label id='label'>#"+datos.entrada[0].fields.entrada+"&nbsp;<img src=../../../../../static/imagenes/"+datos.usuario[0].fields.imagen+" class='fotopequeña'> </img></label><a target='_blank' href='"+datos.entrada[0].fields.url_blog+"'> "+datos.usuario[0].fields.first_name+" "+datos.usuario[0].fields.last_name+"</a><span class='blog-post-meta'>"+datos.entrada[0].fields.fecha+" por <a target='_blank' href='"+datos.entrada[0].fields.url_blog+"'>"+datos.usuario[0].fields.username+"</a></span></h2>";
						html += "<h3><a target='_blank' href='"+datos.entrada[0].fields.link+"'>"+datos.entrada[0].fields.titulo+"</a></h3>";
						html += "<p>"+datos.entrada[0].fields.descripcion+"</p>";
						html += "<div id='valoracion'><div class='btn-toolbar' role='toolbar'><div class='btn-group'><button type='button' disabled='disabled' class='btn btn-success btn-xs'><span class='badge'>"+datos.entrada[0].fields.totalup+"</span></button></div><div class='btn-group'><button type='button' disabled='disabled' class='btn btn-danger btn-xs'><span class='badge'>"+datos.entrada[0].fields.totaldown+"</span></button></div></div></div></div></div>";
						$("#resultado").append(html); 
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
						console.log()
						var html = "<div class='blog-post'><div id='entrada'><h2 class='blog-post-title'><label>#"+datos.entradas[i].fields.entrada+"</label><a target='_blank' href='"+datos.usuario[0].fields.url_blog+"'> "+datos.entradas[i].alumno+"</a><span class='blog-post-meta'>"+datos.entradas[i].fields.fecha+" por <a target='_blank' href='"+datos.usuario[0].fields.url_blog+"'>"+datos.usuario[0].fields.nick+"</a></span></h2>";
						html += "<h3><a target='_blank' href='"+datos.entradas[i].fields.link+"'>"+datos.entradas[i].fields.titulo+"</a></h3>";
						html += "<p>"+datos.entradas[i].fields.descripcion+"</p></div></div>";
						$("#resultado").append(html); 
					}
				}
			},
		});
	}
}
			
				

	/*



	
		
			<a href='javascript:void(0)' onclick="Up('{{ entrada.id }}','{{ entrada.usuario.id }}');"><button type="button" class="btn btn-success btn-xs">Up <span id="up" class="badge"> 0 </span></button></a>
		</div> 
		<div class="btn-group">
			<a href='javascript:void(0)' onclick="Down('{{ entrada.id }}');"><button type="button" class="btn btn-danger btn-xs">Down <span id="down" class="badge"> 0 </span></button></a>
		</div>
	</div>
</div>*/