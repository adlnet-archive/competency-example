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
</nav>
<div class="jumbotron">
	<div class="container">
		<h1>Tetris</h1>
	</div>
</div>
<div class="container">
	<div class="page-header">
		%if my_total < total:
			<h1>Tetris Badges <small>Can you become the Tetris master and collect all of the badges? <b>{{my_total}}/{{total}}</b></small></h1>
		%else:
			<h1>Tetris Badges <small>You are the Tetris master! <b>{{my_total}}/{{total}}</b></small></h1>
		%end
	</div>
	%for competency in comps["competencies"]:
		<div class="col-xs-12">
			<div class="panel panel-default">
				<div class="panel-heading">
					%ctit = competency["title"]
					%if ctit == "Experience API Tetris Level Competency":
						%tot = levels
						%mytot = my_levels
					%elif ctit == "Experience API Tetris Line Competency":
						%tot = lines
						%mytot = my_lines
					%elif ctit == "Experience API Tetris Score Competency":
						%tot = scores
						%mytot = my_scores
					%else:
						%tot = times
						%mytot = my_times
					%end
					<h3 class="panel-title">{{ctit}} - {{mytot}}/{{tot}}</h3>
				</div>
				<div class="panel-body">
					%if 'performances' in competency:			
						%for perf in competency["performances"]:
							%png = perf["levelid"] + ".png"
							%tit = perf["levelid"].replace("_", " ")
							<p><img src="../static/badges/{{png}}"><b>{{tit}}</b> - {{perf["leveldescription"]}}</p>
						%end
					%end
				</div>
			</div>
		</div>
	%end
</div>
</body>
</html>