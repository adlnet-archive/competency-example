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
<div class="jumbotron">
	<div class="container">
		<h1>{{fwk['title']}}</h1>
		<p>{{fwk['description']}}</p>
		%if fwk.get('met', False):
			<div class="alert alert-success">
				Congrats! You've achieved all the competencies in this list!
			</div>
		%else:
			%if username:
			<!-- work in progress
			<p><a href="/me?update={{fwk['encodedentry']}}" class="btn btn-primary" role="button">Check for Updates</a></p>
			-->
			%end
		%end
	</div>
</div>
<div class="container">
	%for comp in fwk['competencies']:
		%if comp['type'] == 'framework': 
			<div class="row">
				<div class="col-xs-12">
				%if comp.get('met', False):
					<div class="panel panel-success">
				%else:
					<div class="panel panel-default">
				%end
						<div class="panel-heading">
							<h3 class="panel-title">{{comp['title']}}</h3>
						</div>
						<div class="panel-body">
							{{comp['description']}}
						</div>
					</div>
				</div>
				%for subcomp in comp['competencies']:
				<div class="row">
					<div class = "col-xs-1"></div>
					<div class="col-xs-11">
					%if subcomp.get('met', False):
						<div class="panel panel-success">
							<div class="panel-heading alert-success">
					%else:
						<div class="panel panel-default">
							<div class="panel-heading alert-info">
					%end
							<a href="./test?compid={{subcomp['encodedentry']}}" class="alert-link">{{subcomp['title']}}</a></div>
							<div class="panel-body">
								{{subcomp['description']}}
							</div>
						</div>
					</div>
				</div>
				%end
			</div>
		%else:
			<div class="row">
				<div class="col-xs-12">
				%if comp.get('met', False):
					<div class="panel panel-success">
						<div class="panel-heading alert-success">
				%else:
					<div class="panel panel-default">
						<div class="panel-heading alert-info">
				%end
						<a href="./test?compid={{comp['encodedentry']}}" class="alert-link">{{comp['title']}}</a></div>
						<div class="panel-body">
							{{comp['description']}}
						</div>
					</div>
				</div>
			</div>
		%end
	%end
</div>
</body>
</html>