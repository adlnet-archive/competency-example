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
	<div class="row">
		<div class="col-xs-12">
		%if username:
			<div class="page-header">
			<h1>{{username}} <small>Competencies you signed up for</small></h1>
		%else:
			<p>You are not signed in. Enter a username and password. If they are new, include an email and name, too.</p>
			%if error:
				<div class="alert alert-danger">{{error}}</div>
			%end
		%end
		</div>
	</div>
	<div class="row">
		%if not fwks:
			<div class="col-xs-12">You have no competencies yet!</div>
		%else:
			%for fwk in fwks:
				<div class="col-xs-12">
					%if fwk.get('met', False):
						<div class="panel panel-success">
					%else:
						<div class="panel panel-default">
					%end
						<div class="panel-heading">
							<h3 class="panel-title">{{fwk['title']}}</h3>
						</div>
						<div class="panel-body">
							<p>{{fwk['description']}}</p>
							%if username:
								<p><a href="/me?uri={{fwk['encodedentry']}}" class="btn btn-primary btn-sm" role="button">Details</a></p>
							%end
						</div>
						</div>
						</div>
				</div>
			%end
		%end
	</div>
</body>
</html>