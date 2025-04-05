package fr.crazycat256.systemreaper.actions;

import static fr.crazycat256.systemreaper.util.CliUtils.*;

public class Unlock extends Action {

    public Unlock(String ip) {
        super(ip);
    }

    @Override
    public String getDescription() {
        return "Unlocks the target's computer.";
    }

    @Override
    public void execute() {
        print("\n>>> Deploying decryption keys to " + ip + "...", 2500);
        sleep(1000);

        load("Bypassing security measures", 1000);
        load("Decrypting locked files", 5000);
        load("Restoring user privileges", 1000);
        load("Reactivating system components", 2000);

        print("\n>>> SYSTEM RESTORED TO NORMAL OPERATION!", 250);
        print(">>> ACCESS GRANTED.", 250);
    }
}
