package fr.crazycat256.systemreaper.actions;

import static fr.crazycat256.systemreaper.util.CliUtils.*;

public class Lock extends Action {

    public Lock(String ip) {
        super(ip);
    }

    @Override
    public String getDescription() {
        return "Locks the target's computer, you can unlock using 'unlock'.";
    }

    @Override
    public void execute() {
        print("\n>>> Deploying ransomware module on " + ip + "...", 2500);
        sleep(1000);

        load("Encrypting system files", 5000);
        load("Blocking keyboard and mouse input", 500);
        load("Locking critical system processes", 1000);
        load("Displaying ransom demand", 2500);

        print("\n>>> TARGET SYSTEM HAS BEEN FULLY LOCKED.", 250);
        print(">>> USER ACCESS DENIED!", 250);
    }
}
