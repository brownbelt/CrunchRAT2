<?php
    # JSON decodes implant POST data
    $post_data = json_decode(file_get_contents("php://input"), true);

    # TO DO: Add in file_put_contents from $post_data array into the <HOSTNAME>/<PID>.log file
?>
