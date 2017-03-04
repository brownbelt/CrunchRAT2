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
        <link href="plugins/bootstrap/css/bootstrap.css" rel="stylesheet" type="text/css">
        <link href="plugins/node-waves/waves.css" rel="stylesheet" type="text/css">
        <link href="plugins/animate-css/animate.css" rel="stylesheet" type="text/css">
        <link href="plugins/morrisjs/morris.css" rel="stylesheet" type="text/css">
        <link href="css/style.css" rel="stylesheet" type="text/css">
        <link href="css/themes/all-themes.css" rel="stylesheet" type="text/css">
        <link href="plugins/jquery-datatable/skin/bootstrap/css/dataTables.bootstrap.css" rel="stylesheet" type="text/css">
    </head>

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
                                <h2>LISTENERS</h2>
                            </div>
                            <div class="body">
                                <table class="table table-bordered table-striped table-hover js-basic-example dataTable">
                                    <thead>
                                        <tr>
                                            <th>External Address</th>
                                            <th>Protocol</th>
                                            <th>Port</th>
                                            <th>Beacon URI</th>
                                            <th>Update URI</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <?php
                                            # Dynamically builds the dataTable
                                            $statement = $database_connection->prepare("SELECT `external_address`, `protocol`, `port`, `beacon_uri`, `update_uri` FROM `listeners`");
                                            $statement->execute();
                                            $results = $statement->fetchAll();
                                            $statement->connection = null;

                                            foreach ($results as $row) {
                                                echo "<tr>";
                                                echo "<td>" . htmlentities($row["external_address"]) ."</td>";
                                                echo "<td>" . htmlentities($row["protocol"]) ."</td>";
                                                echo "<td>" . htmlentities($row["port"]) ."</td>";
                                                echo "<td>" . htmlentities($row["beacon_uri"]) ."</td>";
                                                echo "<td>" . htmlentities($row["update_uri"]) ."</td>";
                                                echo "</tr>";
                                            }
                                        ?>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div><!-- End of dataTable -->
            </div>
        </section><!-- End of main content -->

        <!-- JavaScript -->
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
        <script src="js/demo.js"></script>
    </body>
</html>