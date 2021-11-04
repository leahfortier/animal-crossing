package javacode.gifts;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Scanner;
import java.util.Set;

public class SuggestedGifts {
    private final Map<String, String> gifts;
    private final Set<String> used;

    public SuggestedGifts() {
        this.gifts = new HashMap<>();
        this.used = new HashSet<>();
    }

    public void add(String giftee, String giftName) {
        if (gifts.containsKey(giftee)) {
            System.err.println(giftee + " already has a gift assigned.");
        } else if (used.contains(giftName)) {
            System.err.println(giftName + " has already been used.");
        } else {
            gifts.put(giftee, giftName);
            used.add(this.getUsedName(giftName));
        }
    }

    private String getUsedName(String giftName) {
        Scanner scanner = new Scanner(giftName);
        String first = scanner.next().trim();
        if (Set.of("festivale", "yodel").contains(first)) {
            first += " " + scanner.next().trim();
        }
        return first;
    }

    public boolean isAssigned(String villagerName) {
        return this.gifts.containsKey(villagerName);
    }

    public Set<String> assigned() {
        return this.gifts.keySet();
    }

    public boolean canGift(String giftName) {
        return !used.contains(this.getUsedName(giftName));
    }

    public String get(String giftee) {
        if (gifts.containsKey(giftee)) {
            return gifts.get(giftee);
        }
        return "N/A";
    }
}
