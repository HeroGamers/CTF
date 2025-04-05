package fr.crazycat256.systemreaper.util;

public class CliUtils {
    public static void print(String message, long durationMs) {
        long timeBetweenEachChar = durationMs / message.length();
        for (char c : message.toCharArray()) {
            System.out.print(c);
            sleep(timeBetweenEachChar);
        }
        System.out.println();
    }

    public static void sleep(long milliseconds) {
        try {
            Thread.sleep(milliseconds);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public static void load(String message, long durationMs) {
        final int barLength = 30;
        final int steps = 100;
        final long stepDuration = durationMs / steps;

        for (int i = 0; i <= steps; i++) {
            int filled = (i * barLength) / steps;
            String bar = "█".repeat(filled) + "-".repeat(barLength - filled);

            System.out.printf("\r%s [%s] %3d%%", message, bar, i);
            System.out.flush();

            sleep(stepDuration);
        }
        System.out.println();
    }

}
