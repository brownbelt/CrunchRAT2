<?php
    $database_user = "root";
    $database_pass = "root";
    $database_name = "RAT";
    $database_connection = new PDO("mysql:host=localhost;dbname=$database_name", $database_user, $database_pass, array(PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8"));
?>
