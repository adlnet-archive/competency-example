<!DOCTYPE html>
<html lang="en">
<head>
        <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->


<!-- support scripts -->
<script type="text/javascript" src="../js/2.5.3-crypto-sha1.js"></script>
<script type="text/javascript" src="../js/base64.js"></script>
<script src="http://popcornjs.org/code/dist/popcorn-complete.min.js"></script>
<script src="http://code.jquery.com/jquery.js"></script>

<!-- ADL scripts -->
<script type="text/javascript" src="../js/verbs.js"></script>
<script type="text/javascript" src="../js/xapiwrapper.js"></script>
<script type="text/javascript" src="../js/xapipopcorn.js"></script>

<script src="https://code.jquery.com/jquery-1.10.1.min.js"></script>
<script src="https://code.jquery.com/jquery-migrate-1.2.1.min.js"></script>
<link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.0.2/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.0.2/css/bootstrap-theme.min.css">
<script src="https://netdna.bootstrapcdn.com/bootstrap/3.0.2/js/bootstrap.min.js"></script>
<script>    
    $(document).ready(function(){
            ADL.XAPIWrapper.lrs['actor'] = {"mbox":"{{email}}", "name":"{{user}}"}
            $("#sub").hide()

        var comp = Popcorn.youtube("#compvid", "{{vidurl}}");
        ADL.XAPIVideo.addVideo(comp, "{{compid}}");

        comp.on("ended", function(){
                $("#sub").show()
        });
    });
</script>

</head>
<body>
<nav class="navbar navbar-inverse navbar-static-top" role="navigation">
<a class="navbar-brand" href="/">Competency</a>
<p class="navbar-text navbar-right">Signed in as {{user}}</p>
</nav>
<div class="container">
        <div class="starter-template" style="padding:40px 15px;text-align:center;">        
            <div style="width:450px;height:360px;margin:0 auto;" id="compvid"></div>
                <form role="form" method="post">
                        <div class="form-group">
                                <input type="hidden" name="compid" class="form-control" value={{compid}}>
                <input type="hidden" name="fwkid" class="form-control" value={{fwkid}}>
                        </div>
                        <button type="submit" class="btn btn-default" id="sub">Submit</button>
                </form>
        </div>
</div>
</body>
</html>