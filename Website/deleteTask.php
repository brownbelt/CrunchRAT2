<?php
    # Purpose: This file will delete a specified task (based on UID) from the "tasks" table
    # Parameters: "uid" GET parameter

    # Necessary at the top of every page for session management
    session_start();

    # If unauthenticated
    if (!isset($_SESSION["authenticated"])) {
        header("Location: 403.php");
    }

    include "connector.php";

    # Determines if the supplied "uid" value is valid and not a fuzzed parameter
    $statement = $database_connection->prepare("SELECT * FROM `tasks` WHERE `unique_id` = :unique_id");
    $statement->bindValue(":unique_id", $_GET["uid"]);
    $statement->execute();
    $row_count = $statement->rowCount();

    # Redirects to "404.php" page if invalid or fuzzed parameters
    if ($row_count == "0") {
        header("Location: 404.php");
    }
    # Else deletes specified task and redirects to previous page
    else {
        $statement = $database_connection->prepare("DELETE FROM tasks WHERE `unique_id` = :unique_id");
        $statement->bindValue(":unique_id", $_GET["uid"]);
        $statement->execute();

        header("Location: " . $_SERVER["HTTP_REFERER"]);
    }

    # Kills database connection
    $statement->connection = null;
?>