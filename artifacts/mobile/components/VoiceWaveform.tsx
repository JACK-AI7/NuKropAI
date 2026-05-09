import React, { useEffect } from "react";
import { StyleSheet, View } from "react-native";
import Animated, {
  Easing,
  useAnimatedStyle,
  useSharedValue,
  withRepeat,
  withSequence,
  withTiming,
} from "react-native-reanimated";

const seed = (n: number) => {
  const x = Math.sin(n + 1) * 10000;
  return x - Math.floor(x);
};

const BARS = [0, 1, 2, 3, 4, 5, 6];
const BAR_DELAYS = [0, 70, 140, 0, 140, 70, 0];
const BAR_MAX_H = [18, 26, 22, 32, 22, 26, 18];

function WaveBar({
  index,
  delay,
  maxH,
  isRecording,
  color,
}: {
  index: number;
  delay: number;
  maxH: number;
  isRecording: boolean;
  color: string;
}) {
  const h = useSharedValue(3);

  useEffect(() => {
    if (isRecording) {
      const targetH = maxH * (0.6 + seed(index * 7.3) * 0.4);
      h.value = withRepeat(
        withSequence(
          withTiming(targetH, {
            duration: 180 + seed(index * 3.1) * 120,
            easing: Easing.out(Easing.quad),
          }),
          withTiming(4 + seed(index * 11.7) * 6, {
            duration: 180 + seed(index * 5.9) * 100,
            easing: Easing.in(Easing.quad),
          })
        ),
        -1,
        false
      );
    } else {
      h.value = withTiming(3, { duration: 200 });
    }
    return () => {
      h.value = withTiming(3, { duration: 120 });
    };
  }, [delay, h, index, isRecording, maxH]);

  const s = useAnimatedStyle(() => ({ height: h.value }));

  return (
    <Animated.View
      style={[
        styles.bar,
        s,
        { backgroundColor: color },
      ]}
    />
  );
}

export function VoiceWaveform({
  isRecording,
  color,
}: {
  isRecording: boolean;
  color: string;
}) {
  return (
    <View style={styles.container}>
      {BARS.map((_, i) => (
        <WaveBar
          key={i}
          index={i}
          delay={BAR_DELAYS[i] ?? 0}
          maxH={BAR_MAX_H[i] ?? 20}
          isRecording={isRecording}
          color={color}
        />
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "center",
    gap: 3,
    height: 36,
  },
  bar: {
    width: 4,
    borderRadius: 2,
  },
});
