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
</nav>
<div class="container">
	<div class="page-header">
		<h1>Competency Demo <small>Demonstrating MedBiquitous' Competency Framework and the Experience API</small></h1>
	</div>
	<div class="row">
		<div class="col-xs-12">
		%if username:
			<a href="/all_comps" class="btn btn-primary btn-xs" role="button">Get Started</a>
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
	<p>Welcome to the ADL Competency App! To get started, please login, or if you're new, create a username and password. Once you click the 'Get Started' button, the app will take you to the All Competencies page that lists all of the competency frameworks that have been added to the system. If there aren't any listed, there are three links above you can click to add those competencies to the system. Once you add the ones you want, they will appear below and you can click them to add them to YOUR competency list. Once they have been added to your list, click 'My Competencies' to begin the activites associated with each competency. When viewing the competency, you have the chance to change the LRS endpoint above it. Click each competency link listed to complete the necessary activity to achieve the competency. If you're looking at the Tetris competency, you'll be able to view the badges you have earned while playing by clicking the 'My Badges' button. NOTE: Before you click the 'Get Started' button, if you click the 'Badges' link above in the navigation bar it lists all of the possible badges you can achieve while playing Tetris.</p>
</div>
</body>
</html>