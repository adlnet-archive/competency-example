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
</head>
<body>
<nav class="navbar navbar-inverse navbar-static-top" role="navigation">
	<a class="navbar-brand" href="/" style=>Home</a>
</nav>
<div class="container">
	<div class="page-header">
		<h1>Tetris Badges <small>Can you become the Tetris master and collect all of the badges?</small></h1>
	</div>
	%if error:
		<div class="alert alert-danger">{{error}}</div>
	%else:
		%for component in fwk["components"]:
			<div class="col-xs-12">
				<div class="panel panel-default">
					<div class="panel-heading">
						<h3 class="panel-title">{{component["id"]}}</h3>
					</div>
					<div class="panel-body">
						<p><b>{{component["title"]}}</b></p>
						<br>
						%for pl in component["performancelevels"]:
							%png = pl["id"] + ".png"
							%tit = pl["id"].replace("_", " ")
							<p><img src="../static/badges/{{png}}"><b>{{tit}}</b> - {{pl["description"]}}</p>
						%end
					</div>
				</div>
			</div>
		%end	
	%end
	<br>
	<br>
</div>
</body>
</html>