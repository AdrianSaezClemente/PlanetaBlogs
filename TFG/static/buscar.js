					
$(document).ready(function() {
	
					
	idopcion = $('select').val();
	$('select').on('change',Dameidopcion);

	function Dameidopcion() {
		idopcion = $(this).val();
	}

	$("#buscar").click(function(){
			var texto = $("#texto").val();
			$.ajax({
				data: {'idopcion':idopcion, 'texto':texto},
				url: '/planetablogs/buscarNickUsuario/',
				type: 'GET',
				success: function(datos){
					$("#resultado").html("");
					if(idopcion == 1){
						var html = "<h2>Soy la opcion 1</h2>"
						$("#resultado").append(html);
					}
					if(idopcion == 2){
						if(datos.entradas.length == 0){
							$("#resultado").append("<h2>No hay ninguna entrada para este usuario</h2>"); 
						}
						for (var i=0; i<datos.entradas.length; i++){
							var html = "<div class='blog-post'><div id='entrada'><h2 class='blog-post-title'><a target='_blank' href='"+datos.usuario[0].fields.url_blog+"'>"+datos.usuario[0].fields.nombre_apellidos+"</a><span class='blog-post-meta'>"+datos.entradas[i].fields.fecha+" por <a target='_blank' href='"+datos.usuario[0].fields.url_blog+"'>"+datos.usuario[0].fields.nick+"</a></span></h2>";
							html += "<h3><a target='_blank' href='"+datos.entradas[i].fields.link+"'>"+datos.entradas[i].fields.titulo+"</a></h3>";
							html += "<p>"+datos.entradas[i].fields.descripcion+"</p></div></div>";
							$("#resultado").append(html); 
						}
					}
					if(idopcion == 3){
						var html = "<h2>Soy la opcion 3</h2>"
						$("#resultado").append(html);
					}
				},
			});
		}
	);

});

	
		
			
				

	/*



	
		
			<a href='javascript:void(0)' onclick="Up('{{ entrada.id }}','{{ entrada.usuario.id }}');"><button type="button" class="btn btn-success btn-xs">Up <span id="up" class="badge"> 0 </span></button></a>
		</div> 
		<div class="btn-group">
			<a href='javascript:void(0)' onclick="Down('{{ entrada.id }}');"><button type="button" class="btn btn-danger btn-xs">Down <span id="down" class="badge"> 0 </span></button></a>
		</div>
	</div>
</div>*/