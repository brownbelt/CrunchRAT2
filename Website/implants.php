<?php
    # Includes MySQL connector information
    include "config/connector.php";

    # Establishes a connection to the RAT database
    # Uses MySQL connector information from "config/connector.php"
    # "SET NAMES utf8" is necessary to be Unicode-friendly
    $database_connection = new PDO("mysql:host=localhost;dbname=$database_name", $database_user, $database_pass, array(PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8"));
?>

<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=Edge">
        <meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport">
        <title>CrunchRAT</title>
        <link rel="icon" href="favicon.ico" type="image/x-icon">
        <!-- CSS -->
        <link href="https://fonts.googleapis.com/css?family=Roboto:400,700&amp;subset=latin,cyrillic-ext" rel="stylesheet" type="text/css">
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" type="text/css">
        <link href="plugins/bootstrap/css/bootstrap.css" rel="stylesheet" type="text/css">
        <link href="plugins/node-waves/waves.css" rel="stylesheet" type="text/css">
        <link href="plugins/animate-css/animate.css" rel="stylesheet" type="text/css">
        <link href="plugins/morrisjs/morris.css" rel="stylesheet" type="text/css">
        <link href="css/style.css" rel="stylesheet" type="text/css">
        <link href="css/themes/all-themes.css" rel="stylesheet" type="text/css">
        <link href="plugins/jquery-datatable/skin/bootstrap/css/dataTables.bootstrap.css" rel="stylesheet" type="text/css">
    </head>

    <body class="theme-red">
        <!-- Start of navigation bar (top) -->
        <nav class="navbar">
            <div class="container-fluid">
                <div class="navbar-header">
                    <a href="" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar-collapse" aria-expanded="false"></a>
                    <a href="" class="bars"></a>
                    <a class="navbar-brand" href="index.php">CrunchRAT</a>
                </div>
                <!-- Start of notifications drop-down -->
                <div class="collapse navbar-collapse" id="navbar-collapse">
                    <ul class="nav navbar-nav navbar-right">
                        <li class="dropdown">
                            <a href="" class="dropdown-toggle" data-toggle="dropdown" role="button">
                                <i class="material-icons">flag</i>
                                <span class="label-count">79</span><!-- TO DO: Allow this to be dynamically-generated from "notifications" MySQL table -->
                            </a>
                            <!-- Start of unread notifications --><!-- TO DO: Create "x" to allow marking of a notification as "read" -->
                            <ul class="dropdown-menu">
                                <li class="header">UNREAD NOTIFICATIONS</li>
                                <li class="body">
                                    <ul class="menu tasks">
                                        <li>
                                            <a href=""><!-- TO DO: Allow this to be dynamically-generated from "notifications" MySQL table -->
                                                <h4>New Beacon:</h4><h6>t3ntman's MacBook Pro</h6>
                                            </a>
                                        </li>
                                        <li>
                                            <a href=""><!-- TO DO: Allow this to be dynamically-generated from "notifications" MySQL table -->
                                                <h4>New Beacon:</h4><h6>t3ntman's iMac</h6>
                                            </a>
                                        </li>
                                    </ul>
                                </li>
                                <li class="footer">
                                    <a href="notifications.php">View All Notifications</a>
                                </li>
                            </ul><!-- End of unread notifications -->
                        </li>
                    </ul>
                </div><!-- End of notifications drop-down -->
            </div>
        </nav><!-- End of navigation bar (top) -->

        <!-- Start of navigation bar (left) -->
        <section>
            <aside id="leftsidebar" class="sidebar">
            <!-- Start of user information -->
            <div class="user-info">
                <div class="image">
                    <img src="images/Bebop.png" width="48" height="48" alt="User" />
                </div>
                <div class="info-container">
                    <div class="name" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">t3ntman</div><!-- TO DO: Dynamically-generate this -->
                    <div class="btn-group user-helper-dropdown">
                        <i class="material-icons" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">keyboard_arrow_down</i>
                        <ul class="dropdown-menu pull-right">
                            <li><a href=""><i class="material-icons">person</i>User Profile</a></li>
                            <li role="seperator" class="divider"></li>
                            <li><a href=""><i class="material-icons">input</i>Sign Out</a></li>
                        </ul>
                    </div>
                </div>
            </div><!-- End of user information -->

            <!-- Start of left menu links -->
            <div class="menu">
                <ul class="list">
                    <!-- Home -->
                    <li class="active">
                        <a href="index.html">
                            <i class="material-icons">home</i>
                            <span>Home</span>
                        </a>
                    </li>
                    <!-- Users -->
                    <li>
                        <a href="javascript:void(0);" class="menu-toggle">
                            <i class="material-icons">mood</i>
                            <span>Users</span>
                        </a>
                        <ul class="ml-menu">
                            <li>
                                <a href="">View All Users</a>
                            </li>
                            <li>
                                <a href="">Add User</a>
                            </li>
                            <li>
                                <a href="">Remove User</a>
                            </li>
                        </ul>
                    </li>
                    <!-- Implanted Systems -->
                    <li>
                        <a href="javascript:void(0);" class="menu-toggle">
                            <i class="material-icons">computer</i>
                            <span>Implanted Systems</span>
                        </a>
                        <ul class="ml-menu">
                            <?php
                                # Dynamically builds "Implanted Systems" links
                                $statement = $database_connection->prepare("SELECT `hostname`, `process_id` FROM implants");
                                $statement->execute();
                                $results = $statement->fetchAll();

                                foreach ($results as $row)
                                {
                                    echo "<li>";
                                    echo "<a href=''>" . $row["hostname"] . " (" . $row["process_id"] . ")" ."</a>";
                                    echo "</li>";
                                }

                                # Kills database connection
                                $statement->connection = null;
                            ?>
                        </ul>
                    </li>
                    <!-- Payload Generator -->
                    <li>
                        <a href="javascript:void(0);" class="menu-toggle">
                            <i class="material-icons">publish</i>
                            <span>Payload Generator</span>
                        </a>
                        <ul class="ml-menu">
                            <li>
                                <a href="">Python (Native)</a>
                            </li>
                            <li>
                                <a href="">Macro</a>
                            </li>
                        </ul>
                    </li>
                    <!-- Listeners -->
                    <li>
                        <a href="">
                            <i class="material-icons">phone</i>
                            <span>Listeners</span>
                        </a>
                    </li>
                    <!-- Tasks -->
                    <li>
                        <a href="pages/changelogs.html">
                            <i class="material-icons">view_list</i>
                            <span>Tasks</span>
                        </a>
                    </li>
                </ul>
            </div><!-- End of left menu links -->
            </aside>
        </section><!-- End of navigation bar (left) -->

        <!-- Start of main content -->
        <section class="content">
            <div class="container-fluid">
                <!-- Start of dataTable -->
                <div class="row clearfix">
                    <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
                        <div class="card">
                            <div class="header">
                                <h2>IMPLANTS</h2>
                            </div>
                            <div class="body">
                                <table class="table table-bordered table-striped table-hover js-basic-example dataTable">
                                    <thead>
                                        <tr>
                                            <th>Hostname</th>
                                            <th>Username</th>
                                            <th>Process ID</th>
                                            <th>Operating System</th>
                                            <th>Last Seen</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <?php
                                            # Dynamically builds the dataTable
                                            $statement = $database_connection->prepare("SELECT `hostname`, `current_user`, `process_id`, `os`, `last_seen` FROM implants");
                                            $statement->execute();
                                            $results = $statement->fetchAll();

                                            foreach ($results as $row)
                                            {
                                                echo "<tr>";
                                                echo "<td>" . $row["hostname"] ."</td>";
                                                echo "<td>" . $row["current_user"] ."</td>";
                                                echo "<td>" . $row["process_id"] ."</td>";
                                                echo "<td>" . $row["os"] ."</td>";
                                                echo "<td>" . $row["last_seen"] ."</td>";
                                                echo "</tr>";
                                            }

                                            # Kills database connection
                                            $statement->connection = null;
                                        ?>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div><!-- End of dataTable -->
            </div>
        </section><!-- End of main content -->

        <!-- Start of JavaScript -->
        <script src="plugins/jquery/jquery.min.js"></script>
        <script src="plugins/bootstrap/js/bootstrap.js"></script>
        <script src="plugins/bootstrap-select/js/bootstrap-select.js"></script>
        <script src="plugins/jquery-slimscroll/jquery.slimscroll.js"></script>
        <script src="plugins/node-waves/waves.js"></script>
        <script src="plugins/jquery-datatable/jquery.dataTables.js"></script>
        <script src="plugins/jquery-datatable/skin/bootstrap/js/dataTables.bootstrap.js"></script>
        <script src="plugins/jquery-datatable/extensions/export/dataTables.buttons.min.js"></script>
        <script src="plugins/jquery-datatable/extensions/export/buttons.flash.min.js"></script>
        <script src="plugins/jquery-datatable/extensions/export/jszip.min.js"></script>
        <script src="plugins/jquery-datatable/extensions/export/pdfmake.min.js"></script>
        <script src="plugins/jquery-datatable/extensions/export/vfs_fonts.js"></script>
        <script src="plugins/jquery-datatable/extensions/export/buttons.html5.min.js"></script>
        <script src="plugins/jquery-datatable/extensions/export/buttons.print.min.js"></script>
        <script src="js/admin.js"></script>
        <script src="js/pages/tables/jquery-datatable.js"></script>
        <script src="js/demo.js"></script><!-- End of JavaScript -->
    </body>
</html>