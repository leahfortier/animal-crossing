package javacode.gifts;

import org.junit.Assert;

import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Iterator;
import java.util.List;
import java.util.Scanner;

public class VillagerGifts implements Iterable<String> {
    private final String villager;
    private final List<String> gifts;
    private final List<Integer> breaks;
    private final int index;

    private String selectedGift;

    public VillagerGifts(Scanner in, int index) {
        this.index = index;

        String villager = in.nextLine().trim();
        if (villager.isEmpty()) {
            villager = in.nextLine().trim();
        }
        Assert.assertTrue(villager, villager.endsWith(":"));
        this.villager = villager.replaceFirst(":", "");

        this.gifts = new ArrayList<>();
        this.breaks = new ArrayList<>();
        while (in.hasNext() && !in.hasNext("[A-Z][a-z]+:")) {
            String line = in.nextLine().trim();
            if (!line.isEmpty()) {
                Assert.assertTrue(line, line.startsWith("- "));
                gifts.add(line.substring(2));
            } else {
                this.breaks.add(gifts.size());
            }
        }
    }

    public void setSelectedGift(String giftName) {
        this.selectedGift = giftName;
    }

    public void write(PrintStream out) {
        System.out.println(this.villager + ": " + this.selectedGift);

        boolean printedSelected = false;
        out.println(this.villager + ":");
        for (int i = 0, j = 0; i < gifts.size(); i++) {
            if (j < breaks.size() && i == breaks.get(j)) {
                j++;
                out.println();
            }

            String giftName = gifts.get(i);
            char prefix = '-';
            if (!printedSelected && giftName.equals(this.selectedGift)) {
                prefix = '+';
                printedSelected = true;
            }
            out.println("\t" + prefix + " " + giftName);
        }
        out.println();
    }

    public String villagerName() {
        return this.villager;
    }

    public int numGifts() {
        return this.gifts.size();
    }

    public String toString() {
        return this.villager + ": " + this.numGifts();
    }

    public List<String> copy() {
        return new ArrayList<>(this.gifts);
    }

    public static Comparator<VillagerGifts> byIndex() {
        return Comparator.comparingInt(gifts -> gifts.index);
    }

    public static Comparator<VillagerGifts> bySize() {
        return Comparator.comparingInt(gifts -> gifts.gifts.size());
    }

    @Override
    public Iterator<String> iterator() {
        return this.gifts.iterator();
    }
}
