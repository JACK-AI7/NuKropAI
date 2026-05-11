import React, { useEffect, useMemo } from "react";
import { StyleSheet, View } from "react-native";
import Animated, {
  Easing,
  useAnimatedStyle,
  useReducedMotion,
  useSharedValue,
  withRepeat,
  withSequence,
  withTiming,
} from "react-native-reanimated";

interface ParticleData {
  id: number;
  x: number;
  y: number;
  size: number;
  opacity: number;
  driftX: number;
  driftY: number;
  duration: number;
}

function Particle({ p, color }: { p: ParticleData; color: string }) {
  const tx = useSharedValue(0);
  const ty = useSharedValue(0);
  const op = useSharedValue(p.opacity * 0.2);
  const reducedMotion = useReducedMotion();

  useEffect(() => {
    if (reducedMotion) {
      tx.value = 0;
      ty.value = 0;
      op.value = p.opacity * 0.5;
      return;
    }
    tx.value = withRepeat(
      withSequence(
        withTiming(p.driftX, {
          duration: p.duration,
          easing: Easing.inOut(Easing.sin),
        }),
        withTiming(-p.driftX * 0.4, {
          duration: p.duration * 0.9,
          easing: Easing.inOut(Easing.sin),
        })
      ),
      -1,
      false
    );
    ty.value = withRepeat(
      withSequence(
        withTiming(p.driftY, {
          duration: p.duration * 1.15,
          easing: Easing.inOut(Easing.sin),
        }),
        withTiming(-p.driftY * 0.3, {
          duration: p.duration * 0.85,
          easing: Easing.inOut(Easing.sin),
        })
      ),
      -1,
      false
    );
    op.value = withRepeat(
      withSequence(
        withTiming(p.opacity, { duration: p.duration * 0.55 }),
        withTiming(p.opacity * 0.08, { duration: p.duration * 0.55 })
      ),
      -1,
      false
    );
  }, [op, p.driftX, p.driftY, p.duration, p.opacity, tx, ty, reducedMotion]);

  const s = useAnimatedStyle(() => ({
    transform: [{ translateX: tx.value }, { translateY: ty.value }],
    opacity: op.value,
  }));

  return (
    <Animated.View
      style={[
        styles.particle,
        s,
        {
          left: p.x,
          top: p.y,
          width: p.size,
          height: p.size,
          borderRadius: p.size / 2,
          backgroundColor: color,
          pointerEvents: "none",
        },
      ]}
    />
  );
}

const seed = (n: number) => {
  const x = Math.sin(n + 1) * 10000;
  return x - Math.floor(x);
};

export function ParticleBackground({
  color = "#22C55E",
  count = 10,
  width = 390,
  height = 800,
}: {
  color?: string;
  count?: number;
  width?: number;
  height?: number;
}) {
  const particles = useMemo<ParticleData[]>(
    () =>
      Array.from({ length: count }, (_, i) => ({
        id: i,
        x: seed(i * 3.1) * width,
        y: seed(i * 7.3) * height,
        size: 2 + seed(i * 13.7) * 3,
        opacity: 0.08 + seed(i * 5.9) * 0.22,
        driftX: (seed(i * 17.3) - 0.5) * 60,
        driftY: (seed(i * 11.1) - 0.5) * 80,
        duration: 5000 + seed(i * 23.7) * 6000,
      })),
    [count, width, height]
  );

  return (
    <View style={[StyleSheet.absoluteFill, styles.container]}>
      {particles.map((p) => (
        <Particle key={p.id} p={p} color={color} />
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { pointerEvents: "none" },
  particle: { position: "absolute" },
});
