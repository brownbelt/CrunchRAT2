<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>CrunchRAT</title>
        <link rel="shortcut icon" href="favicon.ico" type="image/x-icon">
        <link rel="stylesheet" href="plugins/bootstrap/css/bootstrap.min.css">
        <link rel="stylesheet" href="plugins/bootstrap/css/bootstrap-theme.min.css">
        <style>
            body {
                background-image: url("images/Ed.jpg");
                background-position: left top;
                background-repeat: no-repeat;
                background-color: black;
            }
        </style>
    </head>

    <body class="text-center">
        <h2>CrunchRAT</h2>
        <h3>Version 2.0 - Written by @t3ntman</h3><br>
        <!-- Start login form -->
        <form action="loginSubmit.php" class="form-inline center-block" method="POST">
            <!-- Username -->
            <div class="form-group input-group">
                <span class="input-group-addon"><i class="glyphicon glyphicon-user"></i></span>
                <input class="form-control" type="text" name="username" placeholder="Username"/>
            </div>
            <!-- Password -->
            <div class="form-group input-group">
                <span class="input-group-addon"><i class="glyphicon glyphicon-lock"></i></span>
                <input class="form-control" type="password" name="password" placeholder="Password"/>
            </div>
            <!-- Login -->
            <div class="form-group">
                <button type="submit" class="btn btn-def btn-block">Login</button>
            </div>
        </form><!-- End login form -->
    </body>

    <!-- JavaScript -->
    <script src="plugins/bootstrap/js/bootstrap.min.js"</script>
</html>
