import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.List;
import java.util.Random;
import java.util.Scanner;

public final class Utils {
    private static final String IN_PATH = "/Users/leahfortier/Dropbox/games/animal crossing/";

    private static final Random RANDOM = new Random();
    private static final long SEED = RANDOM.nextLong();

    static {
        RANDOM.setSeed(SEED);
    }

    public static Scanner openFile(String baseName) {
        File file = new File(IN_PATH + baseName + ".txt");
        try {
            return new Scanner(new FileReader(file));
        } catch (FileNotFoundException e) {
            System.err.println(file.getName() + " not found.");
            return new Scanner("");
        }
    }

    public static <T> int getRandomIndex(List<T> list) {
        return getRandomInt(list.size());
    }

    // Returns a random int with exclusive upper bound from range [0, upperBound)
    public static int getRandomInt(final int upperBound) {
        if (upperBound <= 0) {
            return 0;
        }

        return RANDOM.nextInt(upperBound);
    }
}
