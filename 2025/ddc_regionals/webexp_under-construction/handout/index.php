<?php
$time = time();
$ip = $_SERVER["REMOTE_ADDR"] . PHP_EOL;
file_put_contents("logs/log.txt", "$time $ip", FILE_APPEND);
?>

<?php
$key = "fake-value-replacing-a-uuid";
if (isset($_GET[$key])) {
    $file = $_GET[$key];
    $file_path = "logs/" . $file;

    if (file_exists($file_path)) {
        echo nl2br(file_get_contents($file_path));
    } else {
        echo "File not found";
    }
}
?>

<?php
date_default_timezone_set("Europe/Copenhagen");
$current_hour = date("H");

if ($current_hour >= 5 && $current_hour < 12) {
    $greeting = "Good morning!";
} elseif ($current_hour >= 12 && $current_hour < 18) {
    $greeting = "Good
afternoon!";
} else {
    $greeting = "Good evening!";
} ?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Under Construction</title>
    <style>
        body {
            background-color: #282c34;
            color: #61dafb;
            font-family: "Courier New", Courier, monospace;
            text-align: center;
            margin-top: 50px;
        }

        h1 {
            font-family: monospace;
            font-size: 3.5em;
        }

        .message {
            font-size: 1.2em;
        }
    </style>
</head>

<body>
    <h1>🚧 Under Construction 🚧</h1>
    <p class="message"><?php echo $greeting; ?></p>
    <p class="message">
        This site is currently under development. Please check back soon for updates.
    </p>
</body>

</html>