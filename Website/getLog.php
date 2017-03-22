<?php
    # Necessary at the top of every page for session management
    session_start();

    # If unauthenticated
    if (!isset($_SESSION["authenticated"])) {
        header("Location: 403.php");
    }

    include "connector.php";

    $hostname = $_GET["h"];
    $process_id = $_GET["pid"];

    # Determines if the supplied "h" and "pid" values are valid and not fuzzed parameters
    $statement = $database_connection->prepare("SELECT * FROM `implants` WHERE `hostname` = :hostname AND `process_id` = :process_id");
    $statement->bindValue(":hostname", $hostname);
    $statement->bindValue(":process_id", $process_id);
    $statement->execute();
    $row_count = $statement->rowCount();
    $statement->connection = null;

    # Redirects to "404.php" page if invalid or fuzzed parameters
    if ($row_count == "0") {
        header("Location: 404.php");
    }

    # Gets file path to store implant logs
    # This will be where the "logs" directory is created
    $statement = $database_connection->prepare("SELECT `executed_out_of` FROM `listeners`");
    $statement->execute();
    $results = $statement->fetch();
    $execution_path = $results["executed_out_of"];

    # Builds log file path based off "h" and "pid" GET parameters
    $path = "/var/log/CrunchRAT/" . $hostname . "/" . $process_id . ".log";

    # Echo's contents of <PID>.log to the screen
    echo file_get_contents($path);
?>
