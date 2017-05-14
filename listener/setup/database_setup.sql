CREATE TABLE listeners (protocol TEXT, external_address TEXT, port TEXT, profile TEXT);
CREATE TABLE implants (hostname TEXT, operating_system TEXT, process_id TEXT, current_user TEXT, encryption_key TEXT, last_beacon TEXT);
CREATE TABLE tasks (hostname TEXT, process_id TEXT, task_action TEXT, task_secondary TEXT, task_id TEXT);
