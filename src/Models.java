import util.Utils;

import java.util.Scanner;

// Class to print information about missing critters for models
public class Models {
    public static void main(String[] args) {
        Scanner in = Utils.openFile("models");
        while (in.hasNext()) {
            String line = in.nextLine();
            if (line.contains("!")) {
                // Critters going away at the end of the month that are in complete
                System.out.println(line);
            } else if (line.contains("1") || line.contains("2")) {
                // Other incomplete critters
                System.out.println(line);
            } else if (line.contains(",")) {
                System.err.println("Complete models should remove time ranges: " + line.trim());
            }
        }
    }
}
