import React, { useEffect } from "react";
import { View } from "react-native";
import Animated, {
  Easing,
  useAnimatedStyle,
  useSharedValue,
  withRepeat,
  withSequence,
  withTiming,
} from "react-native-reanimated";
import { useColors } from "@/hooks/useColors";

interface PulseIndicatorProps {
  size?: number;
  color?: string;
}

export function PulseIndicator({ size = 10, color }: PulseIndicatorProps) {
  const colors = useColors();
  const dotColor = color ?? colors.accent;
  const scale = useSharedValue(1);
  const opacity = useSharedValue(0.8);

  useEffect(() => {
    scale.value = withRepeat(
      withSequence(
        withTiming(1.5, { duration: 900, easing: Easing.out(Easing.ease) }),
        withTiming(1, { duration: 900, easing: Easing.in(Easing.ease) })
      ),
      -1,
      false
    );
    opacity.value = withRepeat(
      withSequence(
        withTiming(0.2, { duration: 900 }),
        withTiming(0.9, { duration: 900 })
      ),
      -1,
      false
    );
  }, [opacity, scale]);

  const ringStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    opacity: opacity.value,
  }));

  return (
    <View style={{ width: size * 2.5, height: size * 2.5, justifyContent: "center", alignItems: "center" }}>
      <Animated.View
        style={[
          ringStyle,
          {
            position: "absolute",
            width: size * 2.5,
            height: size * 2.5,
            borderRadius: size * 1.25,
            backgroundColor: dotColor + "30",
          },
        ]}
      />
      <View
        style={{
          width: size,
          height: size,
          borderRadius: size / 2,
          backgroundColor: dotColor,
        }}
      />
    </View>
  );
}
