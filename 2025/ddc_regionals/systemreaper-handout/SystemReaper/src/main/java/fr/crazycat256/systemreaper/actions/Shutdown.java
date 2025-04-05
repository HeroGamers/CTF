package fr.crazycat256.systemreaper.actions;

import static fr.crazycat256.systemreaper.util.CliUtils.*;

public class Shutdown extends Action {

    public Shutdown(String ip) {
        super(ip);
    }

    @Override
    public String getDescription() {
        return "Forces an immediate system shutdown.";
    }

    @Override
    public void execute() {
        print("\n>>> Engaging silent termination protocol on " + ip + "...", 2500);
        sleep(1000);

        load("Disabling power management", 1500);
        load("Injecting fatal shutdown command", 1500);
        load("Overriding system defenses", 3500);

        print("\n>>> SYSTEM SHUTDOWN INITIATED!", 2000);
        System.out.print(">>> TERMINATING CONNECTION IN ");
        print("3... 2... 1...", 3000);
        print(">>> CONNECTION LOST.", 250);
    }

}
