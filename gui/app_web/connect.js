function get_options( mode ){
	var url = "get_options_json?app=configurator&section=" + mode;
	var apps = $.get(
		url,
		function(data) {
			var opt_json = JSON.parse(data);
			var options = $("#opt" + mode);
			options.append("<option>Choose One</option>")
			$.each(opt_json, function() {
				options.append($("<option />").text(this));
			});
		}
	)
};
get_options( "user" );
get_options( "default" );

function new_form(){
	var fc = $("#myform").remove();
	$( '<form id="myform" style="text-align:left; border=1px;"></form>' ).appendTo(
		$("#formcontainer")
	);
}

var other_option = {
	"user": "default",
	"default": "user"
};
function load_form( mode ){
	var options = $( "#opt" + mode );
	var oo = $( "#opt" + other_option[mode] );
	oo.val( "Choose One" );
	new_form();
	if (options.val() != "Choose One") {
		$.get(
				"get_data?app=configurator&section=" + mode + "&name=" + options.val(),
				function(data) {
					var this_json = JSON.parse(data);
					$('#myform').jsonForm({
						"schema": this_json["schema"],
						"value": this_json["value"],
						"form": this_json["form"],
						onSubmit: function (errors, values) {
							if (errors) {
									$('#res').html('<p>I beg your pardon?</p>');
							}
							else {
									$('#res').html('<p>Hello ' + values.name + '.' + (values.age ? '<br/>You are ' + values.age + '.' : '') + "Session Id: " + session_id + '</p>');
									console.log(values);
							}
						}
					});
					session_id = this_json["session_id"];
			});
	};
};
