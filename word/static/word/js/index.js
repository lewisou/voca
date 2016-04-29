$(document).ready(function() {
	$(".practice").keydown(function( event ) {
		if(event.which == 192) {
			$('#' + $(this).attr('audio')).trigger('play');
			event.preventDefault();
		}
	});

	$(".practice").click(function() {
		$('#' + $(this).attr('audio')).trigger('play');
	});

	$(".practice").focus(function() {
		$('#' + $(this).attr('audio')).trigger('play');
	});


	$(".practice").keyup(function() {
		if($(this).val() == $(this).attr('word')) {
			$(this).parent().addClass("has-success");
			
		} else {
			$(this).parent().removeClass("has-success");
		}
	});
});