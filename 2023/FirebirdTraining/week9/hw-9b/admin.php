<?php
// Very secure: Do not read X-Forwarded-For header
if ($_SERVER['REMOTE_ADDR'] !== "127.0.0.1") {
    die("<h1>Admin panel only accessible from localhost (127.0.0.1)! Go away hackers</h1>");
}

if(isset($_REQUEST['cmd'])){
    echo "<pre>";
    $cmd = ($_REQUEST['cmd']);
    system($cmd);
    echo "</pre>";
}
?>

<form action="admin.php" method="post">
    <input name="cmd" type="text" tab="1" autofocus="autofocus"/>
</form>