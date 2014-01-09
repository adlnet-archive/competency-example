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
</nav>
<div class="container">
	<p>After you took the quiz, behind the scenes this app calculated your results and set the passed field for that competetency in your competetency framework. Ideally, these 
	quizzes would be hosted independently and the app would read from their performance frameworks to see what warrants a passing grade (kind of like how the Tetris example awards badges). 
	For now this is just another quick way to show the use of the LRS in these situations.</p>
	<br>
	<br>
	%if passed:
	<p>Your progress has been recorded. You passed the competency {{theid}} <a href='/me'>Back to list</a></p>
	%else:
	<p>Your progress has been recorded. You did not pass the competency {{theid}} <a href='/me'>Back to list</a></p>
</div>
</body>
</html>