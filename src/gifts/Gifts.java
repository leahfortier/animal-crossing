package gifts;

import util.Utils;

import java.util.AbstractMap.SimpleEntry;
import java.util.ArrayList;
import java.util.List;
import java.util.Map.Entry;
import java.util.Scanner;
import java.util.Set;
import java.util.stream.Collectors;

public class Gifts {
    private final List<VillagerGifts> villagers;

    private Gifts() {
        this.villagers = this.readGifts();
    }

    public List<VillagerGifts> readGifts() {
        Scanner in = Utils.openFile("gifts");
        List<VillagerGifts> villagers = new ArrayList<>();
        while (in.hasNext()) {
            villagers.add(new VillagerGifts(in, villagers.size()));
        }
        return villagers;
    }

    public void printAmounts() {
        int totalGifts = 0;
        for (VillagerGifts gifts : villagers) {
            System.out.println(gifts);
            totalGifts += gifts.numGifts();
        }
        System.out.println("\nTotal Gifts: " + totalGifts);
        System.out.println();
    }

    // Returns a random villager/gift pair from all the gifts that match the gift name
    private Entry<String, String> getRandomGift(String giftName, Set<String> toSkip) {
        List<Entry<String, String>> hasGift = new ArrayList<>();
        for (VillagerGifts villagerGifts : villagers) {
            String villagerName = villagerGifts.villagerName();
            if (toSkip.contains(villagerName)) {
                continue;
            }

            for (String gift : villagerGifts) {
                if (gift.startsWith(giftName)) {
                    hasGift.add(new SimpleEntry<>(villagerName, gift));
                }
            }
        }

        return hasGift.isEmpty() ? null : Utils.getRandomValue(hasGift);
    }

    public void printSuggested(String... required) {
        SuggestedGifts suggestedGifts = new SuggestedGifts();
        for (String requiredGift : required) {
            Entry<String, String> toGive = this.getRandomGift(requiredGift, suggestedGifts.assigned());
            if (toGive == null) {
                System.err.println("Missing required gift: " + requiredGift);
            } else {
                suggestedGifts.add(toGive.getKey(), toGive.getValue());
            }
        }

        for (VillagerGifts villagerGifts : villagers) {
            String villagerName = villagerGifts.villagerName();
            if (suggestedGifts.isAssigned(villagerName)) {
                continue;
            }

            List<String> gifts = villagerGifts.copy().stream()
                                              .filter(suggestedGifts::canGift)
                                              .collect(Collectors.toList());
            String gift = gifts.isEmpty() ? "N/A" : Utils.getRandomValue(gifts);
            suggestedGifts.add(villagerName, gift);
        }

        for (VillagerGifts villagerGifts : villagers) {
            String villagerName = villagerGifts.villagerName();
            System.out.println(villagerName + ": " + suggestedGifts.get(villagerName));
        }
    }

    // Print all gifts alphabetically (for storage comparison)
    public void printAll() {
        List<String> allGifts = new ArrayList<>();
        for (VillagerGifts gifts : villagers) {
            allGifts.addAll(gifts.copy());
        }
        allGifts.sort(String::compareTo);
        for (String gift : allGifts) {
            System.out.println(gift);
        }
    }

    public static void main(String[] args) {
        Gifts allGifts = new Gifts();

        allGifts.villagers.sort(VillagerGifts.bySize());
        allGifts.printAmounts();

        allGifts.villagers.sort(VillagerGifts.byIndex());
        allGifts.printSuggested();
    }
}
