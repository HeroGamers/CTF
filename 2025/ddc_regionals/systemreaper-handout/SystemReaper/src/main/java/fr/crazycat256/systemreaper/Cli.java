package fr.crazycat256.systemreaper;

import fr.crazycat256.systemreaper.actions.*;

import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;
import java.util.regex.Pattern;

import static fr.crazycat256.systemreaper.util.CliUtils.*;
import static fr.crazycat256.systemreaper.util.CliUtils.print;

public class Cli {

    private static final String BANNER = """
        ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗    ██████╗ ███████╗ █████╗ ██████╗ ███████╗██████╗\s
        ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║    ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗
        ███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║    ██████╔╝█████╗  ███████║██████╔╝█████╗  ██████╔╝
        ╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║    ██╔══██╗██╔══╝  ██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
        ███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║    ██║  ██║███████╗██║  ██║██║     ███████╗██║  ██║
        ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
                                                                                                                \s
        Hack anything, anywhere, anytime!
        """;

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Pattern ipPattern = Pattern.compile("^(?:[0-9]{1,3}\\.){3}[0-9]{1,3}$");

        System.out.println(BANNER);
        print("..........", 2000);

        String ip;
        while (true) {
            System.out.print("\n>> Enter the IP address of your target: ");
            ip = scanner.nextLine();

            if (ipPattern.matcher(ip).matches()) {
                print(">>> Target acquired: " + ip + " <<<", 250);
                break;
            } else {
                print(">>> ERROR: Invalid IP address! <<<", 250);
            }
        }

        print("\n>>> INFECTING SYSTEM " + ip + "...", 100);
        load("Loading", 5000);
        print(">>> Deploying trojan payload...", 1000);
        print(">>> Establishing backdoor access...", 1000);
        print(">>> SYSTEM INFECTED. READY FOR EXECUTION.", 250);

        Map<String, Action> actions = new HashMap<>();
        actions.put("1", new Shutdown(ip));
        actions.put("2", new Lock(ip));
        actions.put("3", new Unlock(ip));
        actions.put("4", new StealCreds(ip));
        actions.put("5", new Destroy(ip));

        while (true) {
            System.out.println(">>> Choose your attack method:\n");
            for (Map.Entry<String, Action> entry : actions.entrySet()) {
                System.out.println("[" + entry.getKey() + "] " + entry.getValue().getDescription());
            }
            System.out.println();

            String choice = scanner.nextLine();
            if (actions.containsKey(choice)) {
                actions.get(choice).execute();
                break;
            } else {
                print(">>> INVALID SELECTION. CHOOSE WISELY. <<<", 250);
            }
        }
    }
}
