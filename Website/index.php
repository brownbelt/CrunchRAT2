<?php
    # Necessary at the top of every page for session management
    session_start();

    include "connector.php";
    include "generateDashboard.php";

    # If unauthenticated
    if (!isset($_SESSION["authenticated"])) {
        header("Location: 403.php");
    }
?>

<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
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
                    <div class="name" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><?php echo htmlentities($_SESSION["username"]); ?></div>
                    <div class="btn-group user-helper-dropdown">
                        <i class="material-icons" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">keyboard_arrow_down</i>
                        <ul class="dropdown-menu pull-right">
                            <li><a href="">Change Password</a></li>
                            <li role="seperator" class="divider"></li>
                            <li><a href="logout.php"><i class="material-icons">input</i>Sign Out</a></li>
                        </ul>
                    </div>
                </div>
            </div><!-- End of user information -->

            <!-- Start of left menu links -->
            <div class="menu">
                <ul class="list">
                    <!-- Home -->
                    <li class="active">
                        <a href="index.php">
                            <i class="material-icons">home</i>
                            <span>Home</span>
                        </a>
                    </li>
                    <!-- Implanted Systems -->
                    <li>
                        <a href="javascript:void(0);" class="menu-toggle">
                            <i class="material-icons">computer</i>
                            <span>Implanted Systems</span>
                        </a>
                        <ul class="ml-menu">
                            <li><a href="viewImplants.php">View All</a></li>
                            <?php
                                # Dynamically generates "Implanted Systems" links
                                $statement = $database_connection->prepare("SELECT `hostname`, `process_id` FROM `implants`");
                                $statement->execute();
                                $results = $statement->fetchAll();

                                foreach ($results as $row) {
                                    $url = "interact.php?h=" . urlencode($row["hostname"]) . "&pid=" . $row["process_id"];
                                    echo "<li><a href='" . $url . "'>" . htmlentities($row["hostname"]) . " (" . htmlentities($row["process_id"]) . ") " . "</a></li>";
                                }

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
                        <a href="viewListeners.php">
                            <i class="material-icons">phone</i>
                            <span>Listeners</span>
                        </a>
                    </li>
                </ul>
            </div><!-- End of left menu links -->
            </aside>
        </section><!-- End of navigation bar (left) -->

        <!-- Start of dashboard -->
        <section class="content">
            <div class="container-fluid">
                <div class="block-header">
                    <h2>DASHBOARD</h2>
                </div>
                <div class="row clearfix">
                    <!-- "Implants" widget -->
                    <div class="col-lg-3 col-md-3 col-sm-6 col-xs-12">
                        <div class="info-box bg-red hover-expand-effect">
                            <div class="icon">
                                <i class="material-icons">computer</i>
                            </div>
                            <div class="content">
                                <div class="text">IMPLANTS</div>
                                <div class="number count-to" data-from="0" data-to="<?php echo get_implants_count(); ?>" data-speed="15" data-fresh-interval="20"></div>
                            </div>
                        </div>
                    </div>
                    <!-- "Listeners" widget -->
                    <div class="col-lg-3 col-md-3 col-sm-6 col-xs-12">
                        <div class="info-box bg-cyan hover-expand-effect">
                            <div class="icon">
                                <i class="material-icons">phone</i>
                            </div>
                            <div class="content">
                                <div class="text">LISTENERS</div>
                                <div class="number count-to" data-from="0" data-to="<?php echo get_listeners_count(); ?>" data-speed="1000" data-fresh-interval="20"></div>
                            </div>
                        </div>
                    </div>
                    <!-- "Tasks" widget -->
                    <div class="col-lg-3 col-md-3 col-sm-6 col-xs-12">
                        <div class="info-box bg-green hover-expand-effect">
                            <div class="icon">
                                <i class="material-icons">view_list</i>
                            </div>
                            <div class="content">
                                <div class="text">TASKS</div>
                                <div class="number count-to" data-from="0" data-to="<?php echo get_tasks_count(); ?>" data-speed="1000" data-fresh-interval="20"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section><!-- End of dashboard -->

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