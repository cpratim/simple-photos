$(document).ready(function() {
	$('#x').click(function() {
		$('#upload-form').css('z-index', '-1');
		$('#upload-form').css('opacity', '0');
	});
	$('#add-button').click(function() {
		$('#upload-form').css('z-index', '3');
		$('#upload-form').css('opacity', '1');
	});
});