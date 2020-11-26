import org.junit.Assert;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Scanner;
import java.util.Set;

public class Gifts {
    public static void main(String[] args) {
        Scanner in = Utils.openFile("gifts");
        List<Gifts> villagers = new ArrayList<>();
        while (in.hasNext()) {
            villagers.add(new Gifts(in, villagers.size()));
        }

        villagers.sort(bySize());
        int totalGifts = 0;
        for (Gifts gifts : villagers) {
            int numGifts = gifts.gifts.size();
            System.out.println(gifts.villager + ": " + numGifts);
            totalGifts += numGifts;
        }
        System.out.println("\nTotal Gifts: " + totalGifts);
        System.out.println();

        villagers.sort(byIndex());
        Set<String> used = new HashSet<>();
        for (Gifts villagerGifts : villagers) {
            List<String> gifts = new ArrayList<>(villagerGifts.gifts);

            String suggested = "N/A";
            while (!gifts.isEmpty()) {
                int index = Utils.getRandomIndex(gifts);
                String gift = gifts.get(index);
                String first = new Scanner(gift).next();

                if (!used.contains(first)) {
                    suggested = gift;
                    gifts.remove(index);
                    used.add(first);
                    break;
                }
            }

            System.out.println(villagerGifts.villager + ": " + suggested);
        }

        // Print all gifts alphabetically (for storage comparison)
//        List<String> allGifts = new ArrayList<>();
//        for (Gifts gifts : villagers) {
//            allGifts.addAll(gifts.gifts);
//        }
//        allGifts.sort(String::compareTo);
//        for (String gift : allGifts) {
//            System.out.println(gift);
//        }
    }

    private final String villager;
    private final List<String> gifts;
    private final int index;

    private Gifts(Scanner in, int index) {
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

    static Comparator<Gifts> byIndex() {
        return Comparator.comparingInt(gifts -> gifts.index);
    }

    static Comparator<Gifts> bySize() {
        return Comparator.comparingInt(gifts -> gifts.gifts.size());
    }
}
