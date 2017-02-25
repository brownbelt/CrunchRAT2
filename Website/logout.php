<?php
    session_start();
    session_destroy();
?>

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
        <h4>...see you later space cowboy</h4>
        <h5>Click <a class="text-info" href="login.php">here</a> to login</h5>
    </body>

    <!-- JavaScript -->
    <script src="plugins/bootstrap/js/bootstrap.min.js"</script>
</html>
