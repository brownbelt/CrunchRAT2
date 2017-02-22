<?php
    # This function generates a salted hash using bcrypt
    # Modified from original source: https://www.sitepoint.com/password-hashing-in-php
    function generate_hash($password) {
        # If bcrypt is supported on the system
        if (defined("CRYPT_BLOWFISH") && CRYPT_BLOWFISH) {
            # Generates 22-character random salt
            $salt = substr(md5(uniqid(rand(), true)), 0, 22);

            # Generates hashed password (with salt)
            $hash = crypt($password, $salt);

            # Returns hashed password and salt in an array
            return array($hash, $salt);
        }
    }
?>
