<!DOCTYPE html>
<html lang="en">
<head>
	<!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://code.jquery.com/jquery-1.10.1.min.js"></script>
	<script src="https://code.jquery.com/jquery-migrate-1.2.1.min.js"></script>
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.0.2/css/bootstrap.min.css"/>
	<link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.0.2/css/bootstrap-theme.min.css">
    <script type="text/javascript">
        var data = [
		    {
		        "question": "Python allows multiple assignment.", 
		        "type": "true/false", 
		        "correct": true, 
		        "answers": [
		            true, 
		            false
		        ]
		    }, 
		    {
		        "question": "When creating a string in Python, you can use double or single quotes.", 
		        "type": "true/false", 
		        "correct": true, 
		        "answers": [
		            true, 
		            false
		        ]
		    }, 
		    {
		        "question": "Python list indexes start with 1.", 
		        "type": "true/false", 
		        "correct": false, 
		        "answers": [
		            true, 
		            false
		        ]
		    }, 
		    {
		        "question": "What are variables?", 
		        "type": "short answer", 
		        "correct": [
		            "reserved", 
		            "memory",
		            "locations",
		            "to",
		            "store",
		            "values"
		        ]
		    }, 
		    {
		        "question": "What are the four different numerical types in Python?", 
		        "type": "short answer", 
		        "correct": [
		            "int", 
		            "long",
		            "float",
		            "complex"
		        ]
		    }, 
		    {
		        "question": "In Python, tuples can be thought of as *blank* lists.", 
		        "type": "short answer", 
		        "correct": [
		            "read-only"
		        ]
		    }, 
		    {
		        "question": "What sign is used to assign values to variables in Python?", 
		        "type": "short answer", 
		        "correct": [
		            "="
		        ]
		    }, 
		    {
		        "question": "Which is not a standard data type in Python?", 
		        "type": "choice", 
		        "correct": "Queue", 
		        "answers": [
		            "Numbers", 
		            "String", 
		            "List", 
		            "Queue",
		            "Tuple",
		            "Dictionary"
		        ]
		    }, 
		    {
		        "question": "Python dictionaries are enclosed by what?", 
		        "type": "choice", 
		        "correct": "{}", 
		        "answers": [
		            "{}", 
		            "[]", 
		            "()"
		        ]
		    }, 
		    {
		        "question": "In Python, what function would you use to covert object x to a string representation?", 
		        "type": "choice", 
		        "correct": "str(x)", 
		        "answers": [
		            "repr(x)", 
		            "str(x)", 
		            "chr(x)", 
		            "unichr(x)"
		        ]
		    }
		]

        $(document).ready(function(){
            var question_list = []
            var rand_array = []
            while(rand_array.length < 5){
                var rand_num = Math.floor(Math.random()*10)
                var found = false
                for(i = 0; i < rand_array.length; i++){
                    if(rand_array[i] == rand_num){
                        found = true
                        break
                    }
                }
                if(!found)rand_array[rand_array.length] = rand_num;
            }
            $.each(rand_array, function(index, value){
                    question_list.push(data[value]);
            });

            $.each(question_list, function(index, value){
                display_value = index + 1
                $('#fg' + display_value).append('<label for="' + ('question' + display_value) +'">' + display_value + '. ' + value['question'] + '</label>');
                if (value['type'] != 'short answer'){
                    $.each(value['answers'], function(i, v){
                        $('#fg' + display_value).append('<div class="radio" id="radioDiv' + display_value +'-' + (i + 1) + '"></div>');
                        $('#radioDiv' + display_value + '-' + (i + 1)).append('<label><input type="radio" name="' + ('question' + display_value) +'" value="'+ v +'" required>'+ v +'</label>')
                    });
                }
                else{
                    $('#fg' + display_value).append('<input class="form-control "type="text" name="' + ('question' + display_value) + '" required>');
                }
                $('#fg' + display_value).append('<input type="hidden" name="' + ('answer' + display_value) + '" value="' + value['correct'] + '">');
                $('#fg' + display_value).append('<input type="hidden" name="' + ('type' + display_value) + '" value="' + value['type'] + '">');
                $('#fg' + display_value).append('<input type="hidden" name="' + ('questionasked' + display_value) + '" value="' + value['question'] + '">');
            });
            $('#buttonDiv').append('<button type="submit" class="btn btn-default" action="#" method="post">Submit</button>')
        });
        </script>
</head>
<body>
	<nav class="navbar navbar-inverse navbar-static-top" role="navigation">
	<a class="navbar-brand" href="/">Competency</a>
	<p class="navbar-text navbar-right">Signed in as {{user}}</p>
	</nav>	
    <div class="jumbotron">
        <div class="container">
            <!--
	<form class="navbar-form navbar-left" role="search" method="post">
		<button type="submit" class="btn btn-default">Submit</button>
	</form>-->
            <form action="/test" method="post" id="quiz" role="form">
				<div class="form-group">
					<input type="hidden" name="compid" class="form-control" value={{compid}}>
					<input type="hidden" name="fwkid" class="form-control" value={{fwkid}}>
					<input type="hidden" name="testname" class="form-control" value="understanding-variables">
				</div>
                <div class="form-group" id="fg1">
                </div>
                <div class="form-group" id="fg2">
                </div>
                <div class="form-group" id="fg3">
                </div>
                <div class="form-group" id="fg4">
                </div>
                <div class="form-group" id="fg5">
                </div>
                <div class="form-group">
                    <div class="col-lg-offset-2 col-lg-10" id="buttonDiv"></div>
                </div>                                                                                                                        
            </form> 
        </div>        
</div>
<script src="https://netdna.bootstrapcdn.com/bootstrap/3.0.2/js/bootstrap.min.js"></script>
</body>
</html>