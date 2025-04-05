package fr.crazycat256.systemreaper.actions;

import static fr.crazycat256.systemreaper.util.CliUtils.*;

public class StealCreds extends Action {

    public StealCreds(String ip) {
        super(ip);
    }

    @Override
    public String getDescription() {
        return "Extracts saved credentials, cookies, and session tokens from all major platforms.";
    }

    @Override
    public void execute() {
        print("\n>>> Initiating credential extraction on " + ip + "...", 2500);
        sleep(1000);

        load("Scanning browser cookies", 1000);
        load("Decrypting stored passwords", 4000);
        load("Extracting social media tokens", 1500);
        load("Intercepting gaming session data", 500);
        load("Bypassing 2FA security measures", 5000);

        print("\n>>> Data successfully retrieved from " + ip + "!", 250);
        print(">>> Exfiltrating credentials to secure offshore server...", 250);
        load("Uploading encrypted payload", 5000);

        print(">>> OPERATION COMPLETE: All sensitive data secured.", 250);
    }
}
