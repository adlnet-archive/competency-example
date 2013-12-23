<!DOCTYPE html>
<html lang="en">
<head>
	<!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->
<script src="https://code.jquery.com/jquery-1.10.1.min.js"></script>
<script src="https://code.jquery.com/jquery-migrate-1.2.1.min.js"></script>
<link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.0.2/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.0.2/css/bootstrap-theme.min.css">
<script src="https://netdna.bootstrapcdn.com/bootstrap/3.0.2/js/bootstrap.min.js"></script>
<style>
.btn-alt {
  color:#999;
  background: #222;
}
.btn-alt:hover, .btn-alt:focus {
	color:#eee;
	background-color: #222;
	background-position: 0 -15px;
}
</style>
<script>    
    $(document).ready(function(){
        $("#newform").hide()
        $("#newbutton").click(function(){
        	$("#newform").show()
        	$("#newbutton").hide()
        });
    });
</script>

</head>
<body>
<nav class="navbar navbar-inverse navbar-static-top" role="navigation">
	%if username:
		<a class="navbar-brand" href="/logout">Logout</a>
	%end
    <form class="navbar-form navbar-right" role="form" method="post">
        <div class="form-group">
            <label class="sr-only" for="frameworkurl">framework url</label>
            <input type="text" class="form-control" name="frameworkurl" id="frameworkurl" placeholder="Framework URL">
        </div>
        <button type="submit" class="btn btn-alt navbar-button">Add framework</button>
    </form>
</nav>
<div class="container">
	<div class="page-header">
		<h1>Competency Demo <small>Demonstrating MedBiquitous' Competency Framework and the Experience API</small></h1>
	</div>
	<div class="row">
		<div class="col-xs-12">	
			Here are some frameworks you can add to the system:
			<ul>
			<li><a href="/add-framework/basicprogramming">Basic Programming</a></li>
			<li><a href="/add-framework/choosinganlms">Choosing an LMS</a></li>
			<li><a href="/add-framework/tetris">Tetris</a></li>
			</ul>
			<br />
			<a href="/me" class="btn btn-primary btn-xs" role="button">My Competencies</a>
			<br />
			<br />
			Below are the frameworks already added to the system. If you want to add one to your list, just click Go!
		</div>
		%for fwk in fwks:
		<div class="col-xs-12">
			<div class="panel panel-default">
				<div class="panel-heading">
					<h3 class="panel-title">{{fwk['title']}}</h3>
				</div>
				<div class="panel-body">
					<p>{{fwk['description']}}</p>
					%if username:
					<p><a href="/me?uri={{fwk['encodedentry']}}" class="btn btn-primary" role="button">Go</a></p>
					%end
				</div>
			</div>
		</div>
		%end
	</div>
</div>
</body>
</html>