CREATE TABLE implants (`hostname` TEXT, `current_user` TEXT, `process_id` TEXT, `operating_system` TEXT, `last_seen` TEXT, `encryption_key` TEXT);
CREATE TABLE users (`username` TEXT, `hashed_password` TEXT, `salt` TEXT);
CREATE TABLE listeners (`id` INT(16) AUTO_INCREMENT, `external_address` TEXT, `protocol` TEXT, `port` TEXT, `beacon_uri` TEXT, `update_uri` TEXT, `handshake_uri` TEXT, `user_agent` TEXT, `sleep_interval` TEXT, `implant_filename` TEXT, PRIMARY KEY (`id`));
CREATE TABLE tasks (`hostname` TEXT, `process_id` TEXT, `task_action` TEXT, `task_secondary` TEXT, `unique_id` TEXT);
