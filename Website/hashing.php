<?php
    function generate_salted_hash($password) {
        # Purpose: This function takes a password and generates a salted hash using bcrypt
        # Returns: Array containing hashed password and salt (22 randomly-generated characters)
        # Modified from original source: https://www.sitepoint.com/password-hashing-in-php
        if (defined("CRYPT_BLOWFISH") && CRYPT_BLOWFISH) {
            $salt = substr(md5(uniqid(rand(), true)), 0, 22);
            $hash = crypt($password, $salt);
            return array($hash, $salt);
        }
    }
?>
