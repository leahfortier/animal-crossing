package javacode;

import org.junit.Assert;
import javacode.util.Utils;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

// Class to print pretty list of extra flowers by color
public class Flowers {
    public static void main(String[] args) {
        Scanner in = Utils.openFile("extra-flowers");
        List<Flowers> flowers = new ArrayList<>();
        while (in.hasNext()) {
            Flowers color = new Flowers(in);
            if (!color.flowers.isEmpty()) {
                flowers.add(color);
            }
        }

        int totalFlowers = 0;
        for (Flowers color : flowers) {
            System.out.println(color);
            totalFlowers += color.numFlowers;
        }
        System.out.println("\nTotal Flowers: " + totalFlowers);
    }

    private final String color;
    private final List<String> flowers;
    private int numFlowers;

    private Flowers(Scanner in) {
        String color = in.nextLine().trim();
        if (color.isEmpty()) {
            color = in.nextLine().trim();
        }
        Assert.assertTrue(color, color.matches("^[A-Z]+:$"));
        this.color = color.replaceFirst(":", "");

        this.flowers = new ArrayList<>();
        this.numFlowers = 0;

        while (in.hasNext() && !in.hasNext("[A-Z]+:")) {
            String line = in.nextLine().trim();
            if (!line.isEmpty()) {
                Assert.assertTrue(line, line.matches("^-*[a-z]+$"));
                int numFlowers = line.lastIndexOf('-') + 1;
                if (numFlowers > 0) {
                    String flowerName = line.substring(numFlowers);
                    this.flowers.add(numFlowers + " " + flowerName);
                }
                this.numFlowers += numFlowers;
            }
        }
    }

    public String toString() {
        return this.color + ": " + String.join(", ", this.flowers);
    }
}
