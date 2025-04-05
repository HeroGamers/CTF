package fr.crazycat256.systemreaper.actions;

import static fr.crazycat256.systemreaper.util.CliUtils.*;

public class Destroy extends Action {

    public Destroy(String ip) {
        super(ip);
    }

    @Override
    public String getDescription() {
        return "Destroys the target's computer, this action is irreversible.";
    }

    @Override
    public void execute() {
        print("\n>>> WARNING: SYSTEM DESTRUCTION SEQUENCE INITIATED!", 1000);
        print(">>> TARGET: " + ip, 1000);
        sleep(500);

        print("\n>>> GAINING ROOT ACCESS...", 1000);
        load("Bypassing firewalls", 3000);
        load("Disabling antivirus", 1000);
        load("Escalating privileges", 1000);
        print(">>> ROOT ACCESS GRANTED!", 250);
        sleep(500);

        print("\n>>> EXECUTING APOCALYPSE PROTOCOL...", 1500);
        load("Overwriting boot sector", 500);
        load("Encrypting critical system files", 4000);
        load("Injecting irrecoverable malware", 500);
        print("\n>>> SYSTEM FILES OBLITERATED!", 250);
        sleep(1000);

        print("\n>>> ACTIVATING HARDWARE DESTRUCTION MODULE...", 2000);
        load("Overclocking CPU to unsafe levels", 3500);
        load("Disabling cooling systems", 2500);
        load("Initiating BIOS corruption", 750);
        print("\n>>> HARDWARE FAILURE IMMINENT!", 250);
        sleep(1000);

        print("\n>>> ERASING NETWORK TRACES...", 1500);
        load("Spoofing MAC address", 500);
        load("Deleting system logs", 3000);
        load("Wiping forensic data", 1000);
        print("\n>>> DIGITAL FOOTPRINT ERASED!", 250);
        sleep(1000);

        print("\n>>> FINAL STAGE: TOTAL SYSTEM MELTDOWN!", 2000);
        load("Forcing motherboard voltage surge", 2000);
        load("Shredding storage partitions", 2000);
        load("Bricking network adapter", 2000);
        System.out.print("\n>>> SYSTEM CRITICAL ERROR! ERROR CODE: 0x");
        sleep(500);
        print("DEAD", 2000);

        print("\n>>> *** CONNECTION LOST ***", 250);
        sleep(1000);
        print("\n>>> *** TARGET STATUS: NON-EXISTENT ***", 250);
    }
}
