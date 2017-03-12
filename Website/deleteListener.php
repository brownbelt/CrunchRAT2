<?php
    # Purpose: This file will delete a specified listener (based on ID) from the "listeners" table
    # Parameters: "id" GET parameter

    # Necessary at the top of every page for session management
    session_start();

    # If unauthenticated
    if (!isset($_SESSION["authenticated"])) {
        header("Location: 403.php");
    }

    include "connector.php";

    # Determines if the supplied "uid" value is valid and not a fuzzed parameter
    $statement = $database_connection->prepare("SELECT * FROM `listeners` WHERE `id` = :id");
    $statement->bindValue(":id", $_GET["id"]);
    $statement->execute();
    $row_count = $statement->rowCount();

    # Redirects to "404.php" page if invalid or fuzzed parameters
    if ($row_count == "0") {
        header("Location: 404.php");
    }
    # Else deletes specified listener
    else {
        # Deletes specified listener
        $statement = $database_connection->prepare("DELETE FROM `listeners` WHERE `id` = :id");
        $statement->bindValue(":id", $_GET["id"]);
        $statement->execute();

        # Kills the "beacon.php" and "update.php" symbolic links
        $statement = $database_connection->prepare("SELECT `beacon_uri`, `update_uri` FROM `listeners` WHERE `id` = :id");
        $statement->bindValue(":id", $_GET["id"]);
        $statement->execute();
        $results = $statement->fetch();
        unlink($results["beacon_uri"]);
        unlink($results["update_uri"]);

        # Redirects to "listeners.php"
        header("Location: listeners.php");
    }

    # Kills database connection
    $statement->connection = null;
?>