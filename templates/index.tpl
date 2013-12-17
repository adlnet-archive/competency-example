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
	<a class="navbar-brand" href="/">Competency</a>
	%if username:
		<a class="navbar-brand" href="/logout">Logout</a>
	%else:
	<form class="navbar-form navbar-left" role="form" method="post" action="/login">
		<div class="form-group">
			<label class="sr-only" for="username">Username</label>
			<input type="text" class="form-control" name="username" id="username" placeholder="Enter username">
		</div>
		<div class="form-group">
			<label class="sr-only" for="password">Password</label>
			<input type="password" class="form-control" name="password" id="password" placeholder="Password">
		</div>
		<button type="submit" class="btn btn-default">Sign in</button>
	</form>	
	%end
	<a class="navbar-brand" href="/badges" style="float:left">Badges</a>
	<a class="navbar-brand" href="/admin/reset" style="float:right">Admin Reset</a>
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
		%if username:
			%if comps != 0:
				<a href="/me" class="btn btn-primary btn-xs" role="button">Go to your competencies</a>
			%end
		%else:
			<p>You are not signed in. Sign in above if you're an existing member. If you are new, include an email and name, too</p>
			%if error:
				<div class="alert alert-danger">{{error}}</div>
			%end
			<button type="submit" class="btn btn-default" id="newbutton">New?</button>
			<form class="form-inline" role="form" method="post" action="/login" id="newform">
				<div class="form-group">
					<label class="sr-only" for="email">Email</label>
					<input type="email" class="form-control" name="email" id="email" placeholder="Email">
				</div>
				<div class="form-group">
					<label class="sr-only" for="name">Full Name</label>
					<input type="text" class="form-control" name="name" id="name" placeholder="Full Name">
				</div>
				<div class="form-group">
					<label class="sr-only" for="username">Username</label>
					<input type="text" class="form-control" name="username" id="username" placeholder="Username">
				</div>
				<div class="form-group">
					<label class="sr-only" for="password">Password</label>
					<input type="password" class="form-control" name="password" id="password" placeholder="Password">
				</div>			
				<button type="submit" class="btn btn-default">Sign in</button>
			</form>
		%end
		</div>
	</div>
	<br>
	<br>
	<div class="row">
	%if fwks.count() == 0:
		<div class="col-xs-12">
			No competency frameworks? Try these out:
			<ul>
				<li>http://adlnet.gov/competency-framework/computer-science/basic-programming (Basic Programming)</li>
				<li>http://adlnet.gov/competency-framework/scorm/choosing-an-lms (Choosing an LMS)</li>
			</ul>
		</div>
	%else:
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
	%end	
	</div>
</div>
</body>
</html>