<?php
    include "connector.php";
    include "rc4.php";

    # Gets raw POST data because we don't know if it's going to be Base64 encoded or RC4 encrypted
    $post_data = file_get_contents("php://input");

    # If Base64 encoded POST data (initial beacon)
    if (base64_decode($post_data, true) == true) {
        echo "base64 data";
    }
    # Else RC4 encrypted POST data (recurring beacon)
    else {
        echo "rc4 data";
    }
?>
