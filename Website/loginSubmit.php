<?php
    # Necessary at the top of every page for session management
    session_start();

    include "connector.php";

    $username = $_POST["username"];
    $password = $_POST["password"];

    # Gets salt from the "users" table and generates hash to validate
    $statement = $database_connection->prepare("SELECT `salt` FROM users WHERE `username` = :username");
    $statement->bindValue(":username", $username);
    $statement->execute();
    $salt = $statement->fetchColumn();
    $hash = crypt($password, $salt);

    # Validates the hash generated above
    $statement = $database_connection->prepare("SELECT * FROM users WHERE `username` = :username AND `hashed_password` = :hashed_password");
    $statement->bindValue(":username", $username);
    $statement->bindValue(":hashed_password", $hash);
    $statement->execute();
    $row_count = $statement->rowCount();

    # If valid authentication
    if ($row_count == 1) {
        $_SESSION["authenticated"] = 1;
        $_SESSION["username"] = $username;
        header("Location: index.php");
    }
    # Else invalid authentication
    else {
        header("Location: login.php?err=1");
    }
?>
