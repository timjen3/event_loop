function get_values( mode ){
	var url = "getValues?type=" + mode;
	var apps = $.get(
		url,
		function(data) {
			var opt_json = JSON.parse(data);
			var options = $("#opt" + mode);
			options.append("<option>" + mode + "</option>")
			$.each(opt_json, function() {
				options.append($("<option />").text(this));
			});
		}
	)
};
get_options( "resources" );
get_options( "tasks" );
