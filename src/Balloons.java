import org.junit.Assert;
import util.Utils;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Balloons {
    // <color> - <contentType> (<value>)
    // Ex: blue - materials (5 clay)
    private static final Pattern pattern = Pattern.compile("^([a-z]+) - ([a-z]+) \\([a-z0-9'\\- ]+\\)$");

    public static void main(String[] args) {
//        Scanner in = Utils.openFile("balloons");
        Scanner in = Utils.openFile("balloons-marcos");

        int totalDiys = 0;
        int totalBalloons = 0;

        List<Balloon> balloons = new ArrayList<>();
        while (in.hasNext()) {
            String line = in.nextLine().replaceAll("[?*]", "");
            Matcher matcher = pattern.matcher(line);
            if (matcher.matches()) {
                Balloon balloon = new Balloon(matcher.group(1), matcher.group(2));
                balloons.add(balloon);
                totalBalloons++;
                if (balloon.content == BalloonContent.DIY) {
                    totalDiys++;
                }
            } else {
                String[] split = line.split("/");
                if (split.length != 2) {
                    System.err.println(line);
                    continue;
                }
                totalDiys += Integer.parseInt(split[0]);
                totalBalloons += Integer.parseInt(split[1]);
            }
        }

        ColorMap colorMap = new ColorMap();
        ContentMap totalContent = new ContentMap();
        for (Balloon balloon : balloons) {
            colorMap.add(balloon);
            totalContent.add(balloon.content);
        }

        System.out.println("Total Balloons: " + balloons.size());
        totalContent.print();

        System.out.println();
        colorMap.print();

        System.out.printf("Total DIYS/Balloons: %d/%d %.2f%%%n", totalDiys, totalBalloons, 100.0*totalDiys/totalBalloons);
    }

    public static class Balloon {
        private final BalloonColor color;
        private final BalloonContent content;

        public Balloon(String color, String contentType) {
            this.color = BalloonColor.valueOf(color.toUpperCase());
            this.content = BalloonContent.valueOf(contentType.toUpperCase());
        }
    }

    public static class ColorMap extends FreqMap<BalloonColor> {
        private static final BalloonColor[] colors = BalloonColor.values();
        private final ContentMap[] colorContent;

        public ColorMap() {
            super(BalloonColor.values());

            colorContent = new ContentMap[colors.length];
            for (BalloonColor color : colors) {
                colorContent[color.ordinal()] = new ContentMap();
            }
        }

        public void add(Balloon balloon) {
            super.add(balloon.color);
            this.colorContent[balloon.color.ordinal()].add(balloon.content);
        }

        @Override
        public String printValue(BalloonColor color) {
            StringBuilder builder = new StringBuilder(super.printValue(color));
            ContentMap contentMap = this.colorContent[color.ordinal()];
            builder.append(contentMap.toString());
            return builder.append("\n\n").toString();
        }
    }

    public static class ContentMap extends FreqMap<BalloonContent> {
        public ContentMap() {
            super(BalloonContent.values());
        }

        public String toString() {
            return "\t" + super.toString().trim().replaceAll("\n", "\n\t");
        }
    }

    public static class FreqMap<E extends Enum<E>> {
        private final E[] values;
        private final int[] frequency;
        private int size;

        public FreqMap(E[] values) {
            this.values = values;
            this.frequency = new int[values.length];
            this.size = 0;
        }

        public void add(E value) {
            this.frequency[value.ordinal()]++;
            this.size++;
        }

        @Override
        public String toString() {
            StringBuilder builder = new StringBuilder();
            for (E value : values) {
                builder.append(printValue(value));
            }
            return builder.toString();
        }

        public void print() {
            Assert.assertEquals(this.size, Arrays.stream(frequency).sum());
            System.out.println(this);
        }

        public String printValue(E value) {
            String name = value.name();
            name = name.charAt(0) + name.substring(1).toLowerCase();
            int freq = this.frequency[value.ordinal()];
            int percentage = (int)Math.round(100*(double)freq/size);
            return String.format("%s: %s (%d%%)%n", name, freq, percentage);
        }
    }

    public enum BalloonColor {
        BLUE, GREEN, RED, YELLOW
    }

    public enum BalloonContent {
        BELLS, CLOTHING, DIY, FURNITURE, MATERIALS
    }
}
