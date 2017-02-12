<?php
    # Includes MySQL connector information
    include "config/connector.php";

    # Establishes a connection to the RAT database
    # Uses MySQL connector information from "config/connector.php"
    # "SET NAMES utf8" is necessary to be Unicode-friendly
    $DatabaseConnection = new PDO("mysql:host=localhost;dbname=$DatabaseName", $DatabaseUser, $DatabasePass, array(PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8"));
?>

<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=Edge">
        <meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport">
        <title>CrunchRAT</title>
        <link rel="icon" href="favicon.ico" type="image/x-icon">
        <!-- CSS -->
        <link href="https://fonts.googleapis.com/css?family=Roboto:400,700&amp;subset=latin,cyrillic-ext" rel="stylesheet" type="text/css">
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" type="text/css">
        <link href="plugins/bootstrap/css/bootstrap.css" rel="stylesheet">
        <link href="plugins/node-waves/waves.css" rel="stylesheet" />
        <link href="plugins/animate-css/animate.css" rel="stylesheet" />
        <link href="plugins/morrisjs/morris.css" rel="stylesheet" />
        <link href="css/style.css" rel="stylesheet">
        <link href="css/themes/all-themes.css" rel="stylesheet" />
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
                                <span class="label-count">79</span> <!-- TO DO: Allow this to be dynamically-generated from "notifications" MySQL table -->
                            </a>
                            <!-- Start of unread notifications --> <!-- TO DO: Create "x" to allow marking of a notification as "read" -->
                            <ul class="dropdown-menu">
                                <li class="header">UNREAD NOTIFICATIONS</li>
                                <li class="body">
                                    <ul class="menu tasks">
                                        <li>
                                            <a href=""> <!-- TO DO: Allow this to be dynamically-generated from "notifications" MySQL table -->
                                                <h4>New Beacon:</h4><h6>t3ntman's MacBook Pro</h6>
                                            </a>
                                        </li>
                                        <li>
                                            <a href=""> <!-- TO DO: Allow this to be dynamically-generated from "notifications" MySQL table -->
                                                <h4>New Beacon:</h4><h6>t3ntman's iMac</h6>
                                            </a>
                                        </li>
                                    </ul>
                                </li>
                                <li class="footer">
                                    <a href="notifications.php">View All Notifications</a>
                                </li>
                            </ul> <!-- End of unread notifications -->
                        </li>
                    </ul>
                </div> <!-- End of notifications drop-down -->
            </div>
        </nav> <!-- End of navigation bar (top) -->

        <!-- Start of navigation bar (left) -->
        <section>
            <aside id="leftsidebar" class="sidebar">
            <!-- Start of user information -->
            <div class="user-info">
                <div class="image">
                    <img src="images/Bebop.png" width="48" height="48" alt="User" />
                </div>
                <div class="info-container">
                    <div class="name" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">t3ntman</div> <!-- TO DO: Dynamically-generate this -->
                    <div class="btn-group user-helper-dropdown">
                        <i class="material-icons" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">keyboard_arrow_down</i>
                        <ul class="dropdown-menu pull-right">
                            <li><a href=""><i class="material-icons">person</i>User Profile</a></li>
                            <li role="seperator" class="divider"></li>
                            <li><a href=""><i class="material-icons">input</i>Sign Out</a></li>
                        </ul>
                    </div>
                </div>
            </div> <!-- End of user information -->

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
                            <li>
                                <a href="">Hunter's MacBook Pro (664)</a> <!-- Where "664" is the PID -->
                            </li>
                            <li>
                                <a href="">Hunter's MacBook Pro (1238)</a> <!-- Where "1238" is the PID -->
                            </li>
                            <li>
                                <a href="">Hunter's MacBook Pro (6890)</a> <!-- Where "6890" is the PID -->
                            </li>
                            <li>
                                <a href="">t3ntman's iMac (7364)</a> <!-- Where "7364" is the PID -->
                            </li>
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
            </div> <!-- End of left menu links -->
            </aside>
        </section> <!-- End of navigation bar (left) -->
        <!-- Start of main content -->
        <section class="content">
        <div class="container-fluid">
            <div class="row">
                <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
                    <div class="card">
                        <div class="header">
                            <h2>Hunter's MacBook Pro</h2> <!-- TO DO: Dynamically-generate this from the "hosts" table -->
                        </div>
                        <div class="body">
                            <!-- Tab headings -->
                            <ul class="nav nav-tabs tab-nav-right" role="tablist">
                                <li role="presentation" class="active"><a href="#console" data-toggle="tab">CONSOLE</a></li>
                                <li role="presentation"><a href="#screenshots" data-toggle="tab">SCREENSHOTS</a></li>
                                <li role="presentation"><a href="#tasks" data-toggle="tab">TASKS</a></li>
                            </ul>
                            <!-- Tab content -->
                            <div class="tab-content">
                                <!-- "CONSOLE" tab -->
                                <div role="tabpanel" class="tab-pane fade in active" id="console">
                                    <b>CONSOLE</b>
                                    <p>Example text here.</p>
                                </div>
                                <!-- "SCREENSHOTS" tab -->
                                <div role="tabpanel" class="tab-pane fade" id="screenshots">
                                    <b>SCREENSHOTS</b>
                                    <p>Example text here.</p>
                                </div>
                                <!-- "TASKS" tab -->
                                <div role="tabpanel" class="tab-pane fade" id="tasks">
                                    <b>TASKS</b>
                                    <p>Example text here.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section> <!-- End of main content -->
        <!-- JavaScript -->
        <script src="plugins/jquery/jquery.min.js"></script>
        <script src="plugins/bootstrap/js/bootstrap.js"></script>
        <script src="plugins/bootstrap-select/js/bootstrap-select.js"></script>
        <script src="plugins/jquery-slimscroll/jquery.slimscroll.js"></script>
        <script src="plugins/node-waves/waves.js"></script>
        <script src="plugins/jquery-countto/jquery.countTo.js"></script>
        <script src="plugins/raphael/raphael.min.js"></script>
        <script src="plugins/morrisjs/morris.js"></script>
        <script src="plugins/chartjs/Chart.bundle.js"></script>
        <script src="plugins/flot-charts/jquery.flot.js"></script>
        <script src="plugins/flot-charts/jquery.flot.resize.js"></script>
        <script src="plugins/flot-charts/jquery.flot.pie.js"></script>
        <script src="plugins/flot-charts/jquery.flot.categories.js"></script>
        <script src="plugins/flot-charts/jquery.flot.time.js"></script>
        <script src="plugins/jquery-sparkline/jquery.sparkline.js"></script>
        <script src="js/admin.js"></script>
        <script src="js/pages/index.js"></script>
    </body>
</html>
