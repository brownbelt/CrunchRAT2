<?php
    function generate_random_string() {
        # Description: Generates a random 2048 character string
        # Source: http://www.xeweb.net/2011/02/11/generate-a-random-string-a-z-0-9-in-php

        $length = 2048;
        $generated_string = "";
        $allowed_characters = array_merge(range("A","Z"), range("a","z"), range("0","9"));
        $max = count($allowed_characters) - 1;

        for ($i = 0; $i < $length; $i++) {
            $random = mt_rand(0, $max);
            $generated_string .= $allowed_characters[$random];
        }

        return $generated_string;
    }
?>
