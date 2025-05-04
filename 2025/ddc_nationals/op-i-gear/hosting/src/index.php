<?php
// Available gears with descriptions
$gears = [
    "gear-1" => "Et roligt gear",
    "gear-2" => "Et moderat gear",
    "gear-3" => "Et hurtigt gear",
    "gear-4" => "Et racergear",
    "gear-5" => "Et turbo gear"
];

// Process when gear is selected
if (isset($_GET['gear'])) {
    $gear = $_GET['gear'];

    // Just check if the command isn't too long for security you know
    if (strlen($gear) <= 30) {

        // Create command to cat the selected gear file
        $command = "cat gears/" . $gear . ".txt";

        // Execute the command
        $output = shell_exec($command . " 2>&1");

        // Set the current gear for image display
        $current_gear = $gear;
    } else {
        $current_gear = "gear-1";
        $output = "Fejl: Gear navn må højst være 30 tegn";
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Kom op i gear!</title>
    <style>
        body { 
            font-family: monospace; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px; 
            background-color: #f5f5f5;
        }
        h1, h2 { color: #333; }
        pre { 
            background-color: #e0e0e0; 
            padding: 10px; 
            border-radius: 5px; 
            overflow-x: auto;
            border: 1px solid #ccc;
            white-space: pre-wrap;
            word-wrap: break-word;
            word-break: break-word;
            line-height: 1.4;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        select, button {
            font-family: monospace;
            padding: 8px;
            margin: 5px 0;
            border-radius: 4px;
            border: 1px solid #ccc;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .gear-image {
            max-width: 500px;
            margin: 20px auto;
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Kom op i gear!</h1>
        <p>Vælg et gear for at læse information om det.</p>

        <form method="get">
            <div>
                <label for="gear">Vælg gear:</label>
                <select name="gear" id="gear" required>
                    <?php foreach ($gears as $gear_id => $description): ?>
                        <option value="<?php echo htmlspecialchars($gear_id); ?>">
                            <?php echo str_replace('-', ' ', ucfirst($gear_id)) . " - " . $description; ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>
            <button type="submit">Vis gear information</button>
        </form>

        <?php if (isset($output) && isset($current_gear)): ?>
            <h2>Gear Information:</h2>

            <!-- Display gear image based on selection -->
            <img src="pics/<?php echo $current_gear; ?>.jpg" alt="Gear billede" class="gear-image">

            <pre><?php echo $output; ?></pre>
        <?php endif; ?>
    </div>
</body>
</html>
