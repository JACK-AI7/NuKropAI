import { Ionicons } from "@expo/vector-icons";
import { LinearGradient } from "expo-linear-gradient";
import { useRouter } from "expo-router";
import React, { useState, useRef } from "react";
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  Dimensions,
  FlatList,
  NativeSyntheticEvent,
  NativeScrollEvent,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import * as Notifications from "expo-notifications";
import * as Location from "expo-location";
import { useApp } from "@/contexts/AppContext";
import { useColors } from "@/hooks/useColors";

const { width, height } = Dimensions.get("window");

const SLIDES = [
  {
    id: "1",
    title: "Predictive Intelligence",
    description: "AI-powered outbreak forecasting and yield estimation to keep your farm ahead of the curve.",
    icon: "analytics-outline",
    color: "#22C55E",
  },
  {
    id: "2",
    title: "Disease Diagnosis",
    description: "Scan crops instantly with our advanced vision model to identify 40+ common pests and diseases.",
    icon: "scan-outline",
    color: "#4ADE80",
  },
  {
    id: "3",
    title: "Market Edge",
    description: "Get real-time Mandi prices and AI-driven profitability forecasting to maximize your earnings.",
    icon: "trending-up-outline",
    color: "#3B82F6",
  },
];

export default function OnboardingScreen() {
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const { setHasSeenOnboarding } = useApp();
  const [activeIndex, setActiveIndex] = useState(0);
  const flatListRef = useRef<FlatList>(null);

  const onScroll = (event: NativeSyntheticEvent<NativeScrollEvent>) => {
    const index = Math.round(event.nativeEvent.contentOffset.x / width);
    setActiveIndex(index);
  };

  const handleNext = async () => {
    if (activeIndex < SLIDES.length - 1) {
      flatListRef.current?.scrollToIndex({ index: activeIndex + 1 });
    } else {
      // Final Slide: Request Permissions and Finish
      try {
        await Location.requestForegroundPermissionsAsync();
        await Notifications.requestPermissionsAsync();
      } catch (e) {
        console.warn("Permission request failed", e);
      }
      setHasSeenOnboarding(true);
      router.replace("/(tabs)");
    }
  };

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <FlatList
        ref={flatListRef}
        data={SLIDES}
        horizontal
        pagingEnabled
        showsHorizontalScrollIndicator={false}
        onScroll={onScroll}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={styles.slide}>
            <LinearGradient
              colors={[item.color + "20", "transparent"]}
              style={styles.gradient}
            />
            <View style={[styles.iconCircle, { backgroundColor: item.color + "15", borderColor: item.color + "40" }]}>
              <Ionicons name={item.icon as any} size={80} color={item.color} />
            </View>
            <Text style={[styles.title, { color: colors.foreground }]}>{item.title}</Text>
            <Text style={[styles.description, { color: colors.mutedForeground }]}>{item.description}</Text>
          </View>
        )}
      />

      <View style={[styles.footer, { paddingBottom: insets.bottom + 40 }]}>
        <View style={styles.pagination}>
          {SLIDES.map((_, i) => (
            <View
              key={i}
              style={[
                styles.dot,
                {
                  backgroundColor: i === activeIndex ? colors.primary : colors.border,
                  width: i === activeIndex ? 24 : 8,
                },
              ]}
            />
          ))}
        </View>

        <TouchableOpacity
          style={[styles.button, { backgroundColor: colors.primary }]}
          onPress={handleNext}
        >
          <Text style={styles.buttonText}>
            {activeIndex === SLIDES.length - 1 ? "Get Started" : "Continue"}
          </Text>
          <Ionicons
            name={activeIndex === SLIDES.length - 1 ? "checkmark-circle" : "arrow-forward"}
            size={20}
            color="#000"
          />
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  slide: {
    width,
    height: height * 0.75,
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 40,
  },
  gradient: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    height: height * 0.4,
  },
  iconCircle: {
    width: 180,
    height: 180,
    borderRadius: 90,
    justifyContent: "center",
    alignItems: "center",
    borderWidth: 1,
    marginBottom: 40,
  },
  title: {
    fontSize: 28,
    fontWeight: "800",
    fontFamily: "Inter_700Bold",
    textAlign: "center",
    marginBottom: 16,
  },
  description: {
    fontSize: 16,
    fontFamily: "Inter_400Regular",
    textAlign: "center",
    lineHeight: 24,
  },
  footer: {
    paddingHorizontal: 40,
    alignItems: "center",
  },
  pagination: {
    flexDirection: "row",
    gap: 8,
    marginBottom: 32,
  },
  dot: {
    height: 8,
    borderRadius: 4,
  },
  button: {
    width: "100%",
    height: 60,
    borderRadius: 30,
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    gap: 12,
  },
  buttonText: {
    fontSize: 18,
    fontWeight: "700",
    fontFamily: "Inter_700Bold",
    color: "#000",
  },
});
