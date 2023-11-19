<!DOCTYPE html>
<html>
<head><title>M$Office Meta Reader</title></head>
<body>
<h1>M$Office Meta Reader</h1>
<form action="." method="post" enctype="multipart/form-data">
    Select some office file (docx, xlsx, pptx) to get its metainfo: (Max size: 1M)<br />
    <input type="file" name="file" id="file"> <br />
    <input type="submit" value="Upload" name="submit">
</form>

<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// flag{no flag here, sorry!}
// https://gist.github.com/jobertabma/2900f749967f83b6d59b87b90c6b85ff


// Make sure we can fetch external entities.
// @see http://nl1.php.net/manual/en/function.libxml-disable-entity-loader.php
libxml_disable_entity_loader(false);

// Catch any and all libxml errors
// @see http://nl1.php.net/manual/en/function.libxml-use-internal-errors.php
libxml_use_internal_errors(true);

if (isset($_FILES['file'])) {
    
    $ALLOWED_EXTS = ['docx', 'xlsx', 'pptx'];

    $file = $_FILES['file'];
    if (!in_array(pathinfo($file['name'], PATHINFO_EXTENSION), $ALLOWED_EXTS)) {
        die("extension incorrect");
    }

    if ($file['size'] == 0) {
        die("file empty");
    }

    $zip = new ZipArchive;
    $res = $zip->open($file['tmp_name']);
    if($res !== TRUE) {
        die("Error while reading zip file: $res");
    }

    $coreStat = $zip->statName('docProps/core.xml');
    if ($coreStat == FALSE) {
        die("Zip file does not have core.xml");
    }
    if ($coreStat['size'] > 10240) {
        die("core.xml too big! " . $coreStat['size'] . " - max 10240");
    }

    $xmlstring = $zip->getFromName('docProps/core.xml');
    $zip->close();

    $xml = new SimpleXMLElement($xmlstring, LIBXML_NOENT);
    if ($xml === FALSE) {
        die("invaild xml");
    }
    $ns = $xml->getNamespaces(true);

    echo "<pre>";
    echo "Title: " . $xml->children($ns['dc'])->title . "\n";
    echo "Subject: " . $xml->children($ns['dc'])->subject . "\n";
    echo "Creator: " . $xml->children($ns['dc'])->creator . "\n";
    echo "Description: " . $xml->children($ns['dc'])->description . "\n";
    echo "Last Modified By: " . $xml->children($ns['cp'])->lastModifiedBy . "\n";
    echo "Revision: " . $xml->children($ns['cp'])->revision . "\n";
    echo "</pre>";
}
?>
<br />
<?php /* <a href="admin.php"><small>[Admin panel]</small></a> */ ?>
</body>
</html>