package javacode.util;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.OutputStream;
import java.io.PrintStream;
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

    private static File getFile(String baseName) {
        return new File(IN_PATH + baseName + ".txt");
    }

    public static Scanner openFile(String baseName) {
        File file = getFile(baseName);
        try {
            return new Scanner(new FileReader(file));
        } catch (FileNotFoundException e) {
            System.err.println(file.getName() + " not found.");
            return new Scanner("");
        }
    }

    public static PrintStream openWriter(String baseName) {
        File file = new File(IN_PATH + baseName + ".txt");
        try {
            return new PrintStream(file);
        } catch (FileNotFoundException e) {
            System.err.println("Unable to open writer for " + file.getName());
            return new PrintStream(new NullOutputStream());
        }
    }

    public static class NullOutputStream extends OutputStream {
        @Override
        public void write(int b) {}
    }

    public static <T> int getRandomIndex(List<T> list) {
        return getRandomInt(list.size());
    }

    public static <T> T getRandomValue(List<T> list) {
        return list.get(getRandomIndex(list));
    }

    // Returns a random int with exclusive upper bound from range [0, upperBound)
    public static int getRandomInt(final int upperBound) {
        if (upperBound <= 0) {
            return 0;
        }

        return RANDOM.nextInt(upperBound);
    }

    public static <T extends Enum<T>> T enumValueOf(Class<T> enumClass, String name) {
        try {
            String enumName = name.toUpperCase().replaceAll("[\\s-]", "_").replaceAll("['.:]", "");
            return Enum.valueOf(enumClass, enumName);
        } catch (IllegalArgumentException exception) {
            System.err.println("Invalid " + enumClass.getCanonicalName() + ": " + name);
            return null;
        }
    }
}
