import java.io.*;
import java.nio.file.*;
import java.util.Scanner;

public class chall {
    
    public static String readFlag() {
        try {
            return new String(Files.readAllBytes(Paths.get("flag.txt")));
        } catch (IOException e) {
            e.printStackTrace();
            return "";
        }
    }

    public static String readPwd() {
        try {
            return new String(Files.readAllBytes(Paths.get("pwd.txt")));
        } catch (IOException e) {
            e.printStackTrace();
            return "";
        }
    }

// // // // // // // // // // // 
// ::CHALLANGE STARTS HERE:: // 
// // // // // // // // // // 

    public static String magic(String input) {
        long j = 1337;
        int k = 57 - 30 + 3 + 1;  
        int l = 222/6;  
        
        for (int i = 0; i < input.length(); i++) {
            j *= (input.charAt(i) + k) * l;
            j %= 1_000_000_007;
        }
        
        j = ((j << 16) | (j >> 48)) & 0xFFFFFFFFFFFFL;
        return Long.toHexString(j);
    }


    public static boolean check(String password, String storedHash) {
        String hashedPassword = magic(password);
        return hashedPassword.equals(storedHash);
    }

    public static void main(String[] args) {

        String password = readPwd();
        String storedHash = magic(password);
        

        Scanner scanner = new Scanner(System.in);
        System.out.println("***ID");
        System.out.println("**" + storedHash);
        System.out.println("***ENTER PASSWORD:");
        String userInput = scanner.nextLine();
        
        if (check(userInput, storedHash)) {
            System.out.println("***CRACKED: " + readFlag());
        } else {
            System.out.println("***WRONG***.");
        }
    }
}
