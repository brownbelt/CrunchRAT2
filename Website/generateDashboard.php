<?php
    function get_implants_count() {
        # Purpose: This function gets the total number of listeners
        # Returns: Returns an integer that contains the total number of implants
        include "connector.php";
        $statement = $database_connection->prepare("SELECT * FROM `implants`");
        $statement->execute();
        $implants_count = $statement->rowCount();
        return $implants_count;
    }

    function get_listeners_count() {
        # Purpose: This function gets the total number of listeners
        # Returns: Returns an integer that contains the total number of listeners
        include "connector.php";
        $statement = $database_connection->prepare("SELECT * FROM `listeners`");
        $statement->execute();
        $listeners_count = $statement->rowCount();
        return $listeners_count;
    }

    function get_tasks_count() {
        # Purpose: This function gets the total number of tasks
        # Returns: Returns an integer that contains the total number of tasks
        include "connector.php";
        $statement = $database_connection->prepare("SELECT * FROM `tasks`");
        $statement->execute();
        $tasks_count = $statement->rowCount();
        return $tasks_count;
    }
?>
