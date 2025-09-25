<?php
// Location of log file
$logFile = __DIR__ . "/ble_log.json";

// Read POST body
$data = file_get_contents("php://input");

if ($data) {
    // Append with newline
    file_put_contents($logFile, $data . PHP_EOL, FILE_APPEND | LOCK_EX);
    http_response_code(200);
    echo "Logged successfully";
} else {
    http_response_code(400);
    echo "No data received";
}
?>
