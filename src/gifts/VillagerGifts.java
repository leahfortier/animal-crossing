package gifts;

import org.junit.Assert;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.Iterator;
import java.util.List;
import java.util.Scanner;

public class VillagerGifts implements Iterable<String> {
    private final String villager;
    private final List<String> gifts;
    private final int index;

    public VillagerGifts(Scanner in, int index) {
        this.index = index;

        String villager = in.nextLine().trim();
        if (villager.isEmpty()) {
            villager = in.nextLine().trim();
        }
        Assert.assertTrue(villager, villager.endsWith(":"));
        this.villager = villager.replaceFirst(":", "");

        this.gifts = new ArrayList<>();
        while (in.hasNext() && !in.hasNext("[A-Z][a-z]+:")) {
            String line = in.nextLine().trim();
            if (!line.isEmpty()) {
                Assert.assertTrue(line, line.startsWith("- ") || line.startsWith("+ "));
                gifts.add(line.substring(2));
            }
        }
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
