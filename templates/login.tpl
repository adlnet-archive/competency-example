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
</head>
<body>
<nav class="navbar navbar-inverse navbar-static-top" role="navigation">
<a class="navbar-brand" href="/">Competency</a>
</nav>
<div class="container">
	<p>Enter a username and password. If they are new, it'll create them</p>
	%if error:
		<div class="alert alert-danger">{{error}}</div>
	%end
	<form class="form-inline" role="form" method="post">
		<div class="form-group">
			<label class="sr-only" for="username">username</label>
			<input type="text" class="form-control" name="username" id="username" placeholder="Enter username">
		</div>
		<div class="form-group">
			<label class="sr-only" for="password">Password</label>
			<input type="password" class="form-control" name="password" id="password" placeholder="Password">
		</div>
		<p>New? Add your email and name.</p>
		<div class="form-group">
			<label class="sr-only" for="email">username</label>
			<input type="email" class="form-control" name="email" id="email" placeholder="Enter email">
		</div>
		<div class="form-group">
			<label class="sr-only" for="name">username</label>
			<input type="text" class="form-control" name="name" id="name" placeholder="Enter name">
		</div>
		<button type="submit" class="btn btn-default">Sign in</button>
	</form>
</div>
</body>
</html>