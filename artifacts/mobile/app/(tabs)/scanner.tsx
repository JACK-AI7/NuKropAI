import { Ionicons } from "@expo/vector-icons";
import * as Haptics from "expo-haptics";
import * as ImagePicker from "expo-image-picker";
import React, { useCallback, useState } from "react";
import {
  Image,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import Animated, {
  Easing,
  useAnimatedStyle,
  useSharedValue,
  withRepeat,
  withSequence,
  withTiming,
} from "react-native-reanimated";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { useColors } from "@/hooks/useColors";
import { useApp } from "@/contexts/AppContext";
import { ScanResultCard, type ScanResult } from "@/components/ScanResultCard";

function ScanRing({ size, delay, color }: { size: number; delay: number; color: string }) {
  const scale = useSharedValue(0.8);
  const opacity = useSharedValue(0.5);

  React.useEffect(() => {
    const t = setTimeout(() => {
      scale.value = withRepeat(
        withTiming(1.25, { duration: 2000, easing: Easing.out(Easing.ease) }),
        -1,
        false
      );
      opacity.value = withRepeat(
        withSequence(
          withTiming(0, { duration: 2000, easing: Easing.out(Easing.ease) }),
          withTiming(0.5, { duration: 0 })
        ),
        -1,
        false
      );
    }, delay);
    return () => clearTimeout(t);
  }, [delay, opacity, scale]);

  const animStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    opacity: opacity.value,
  }));

  return (
    <Animated.View
      style={[
        styles.ring,
        animStyle,
        { width: size, height: size, borderRadius: size / 2, borderColor: color },
      ]}
    />
  );
}

const SCAN_RESULTS: ScanResult[] = [
  {
    disease: "Early Blight (Alternaria solani)",
    confidence: 94,
    severity: "high",
    affectedArea: 35,
    recommendations: [
      "Remove and destroy infected leaves immediately",
      "Avoid overhead irrigation to reduce leaf wetness",
      "Improve air circulation between plants",
    ],
    treatments: [
      "Mancozeb 75 WP @ 2.5g/L water every 7-10 days",
      "Chlorothalonil 75 WP @ 2g/L water",
    ],
  },
  {
    disease: "Leaf Blight (Helminthosporium sp.)",
    confidence: 88,
    severity: "medium",
    affectedArea: 22,
    recommendations: [
      "Collect and burn infected crop debris",
      "Use certified disease-free seeds next season",
      "Maintain proper plant spacing for airflow",
    ],
    treatments: [
      "Propiconazole 25 EC @ 1ml/L water",
      "Tricyclazole 75 WP @ 0.6g/L water",
    ],
  },
  {
    disease: "Healthy Crop (No Disease Detected)",
    confidence: 97,
    severity: "low",
    affectedArea: 0,
    recommendations: [
      "Continue current farming practices",
      "Monitor regularly for early disease signs",
      "Maintain soil health with organic compost",
    ],
    treatments: [],
  },
];

export default function ScannerScreen() {
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const { addScanRecord } = useApp();
  const topPad = Platform.OS === "web" ? 67 : insets.top + 10;
  const [imageUri, setImageUri] = useState<string | null>(null);
  const [isScanning, setIsScanning] = useState(false);
  const [result, setResult] = useState<ScanResult | null>(null);

  const runScan = useCallback(
    async (uri: string) => {
      setImageUri(uri);
      setIsScanning(true);
      setResult(null);
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);

      await new Promise((r) => setTimeout(r, 2800));

      const r2 = SCAN_RESULTS[Math.floor(Math.random() * SCAN_RESULTS.length)]!;
      setResult(r2);
      setIsScanning(false);
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);

      const id = Date.now().toString() + Math.random().toString(36).substr(2, 9);
      addScanRecord({
        id,
        imageUri: uri,
        disease: r2.disease,
        confidence: r2.confidence,
        severity: r2.severity,
        timestamp: Date.now(),
      });
    },
    [addScanRecord]
  );

  const pickImage = useCallback(async () => {
    const perm = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!perm.granted) return;
    const picked = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ["images"],
      quality: 0.8,
    });
    if (!picked.canceled && picked.assets[0]) runScan(picked.assets[0].uri);
  }, [runScan]);

  const takePhoto = useCallback(async () => {
    if (Platform.OS === "web") {
      pickImage();
      return;
    }
    const perm = await ImagePicker.requestCameraPermissionsAsync();
    if (!perm.granted) return;
    const photo = await ImagePicker.launchCameraAsync({ quality: 0.8 });
    if (!photo.canceled && photo.assets[0]) runScan(photo.assets[0].uri);
  }, [pickImage, runScan]);

  const reset = () => {
    setImageUri(null);
    setResult(null);
    setIsScanning(false);
  };

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <ScrollView
        contentContainerStyle={[
          styles.scroll,
          { paddingTop: topPad, paddingBottom: Platform.OS === "web" ? 100 : 110 },
        ]}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.header}>
          <View>
            <Text style={[styles.title, { color: colors.foreground }]}>Crop Scanner</Text>
            <Text style={[styles.subtitle, { color: colors.mutedForeground }]}>
              AI-powered disease detection
            </Text>
          </View>
          {(imageUri ?? result) && (
            <TouchableOpacity
              onPress={reset}
              style={[styles.resetBtn, { backgroundColor: colors.card, borderColor: colors.border }]}
            >
              <Ionicons name="refresh" size={20} color={colors.foreground} />
            </TouchableOpacity>
          )}
        </View>

        {!imageUri && !result && (
          <View style={styles.scanArea}>
            <View style={styles.rings}>
              <ScanRing size={280} delay={0} color={colors.primary} />
              <ScanRing size={220} delay={700} color={colors.accent} />
              <ScanRing size={160} delay={1400} color={colors.primary} />
              <View
                style={[styles.centerIcon, { backgroundColor: colors.card, borderColor: colors.border }]}
              >
                <Ionicons name="leaf-outline" size={44} color={colors.primary} />
              </View>
            </View>
            <Text style={[styles.hint, { color: colors.mutedForeground }]}>
              Upload a clear photo of the crop leaf or affected area for best results
            </Text>
          </View>
        )}

        {imageUri && (
          <View
            style={[
              styles.previewWrap,
              { borderRadius: colors.radius, borderColor: colors.border },
            ]}
          >
            <Image
              source={{ uri: imageUri }}
              style={[styles.preview, { borderRadius: colors.radius }]}
            />
            {isScanning && (
              <View style={styles.overlay}>
                <View style={styles.overlayRings}>
                  <ScanRing size={200} delay={0} color={colors.accent} />
                  <ScanRing size={130} delay={500} color={colors.primary} />
                </View>
                <Text style={[styles.scanningLabel, { color: colors.accent }]}>Analyzing...</Text>
              </View>
            )}
          </View>
        )}

        {result && !isScanning && (
          <View style={{ marginTop: 16 }}>
            <ScanResultCard result={result} />
          </View>
        )}

        {!isScanning && !result && (
          <View style={styles.buttons}>
            <TouchableOpacity
              style={[styles.btn, { backgroundColor: colors.primary }]}
              onPress={takePhoto}
              activeOpacity={0.8}
            >
              <Ionicons name="camera" size={22} color="#000" />
              <Text style={styles.btnTextDark}>Take Photo</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[
                styles.btn,
                { backgroundColor: colors.card, borderColor: colors.border, borderWidth: 1 },
              ]}
              onPress={pickImage}
              activeOpacity={0.8}
            >
              <Ionicons name="image" size={22} color={colors.foreground} />
              <Text style={[styles.btnText, { color: colors.foreground }]}>Upload</Text>
            </TouchableOpacity>
          </View>
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  scroll: { paddingHorizontal: 16 },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-start",
    marginBottom: 28,
  },
  title: { fontSize: 24, fontWeight: "700", fontFamily: "Inter_700Bold", letterSpacing: -0.5 },
  subtitle: { fontSize: 13, fontFamily: "Inter_400Regular", marginTop: 2 },
  resetBtn: {
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: "center",
    alignItems: "center",
    borderWidth: 1,
  },
  scanArea: { alignItems: "center", paddingVertical: 16 },
  rings: { width: 300, height: 300, justifyContent: "center", alignItems: "center" },
  ring: { position: "absolute", borderWidth: 1.5 },
  centerIcon: {
    width: 96,
    height: 96,
    borderRadius: 48,
    justifyContent: "center",
    alignItems: "center",
    borderWidth: 1,
  },
  hint: {
    textAlign: "center",
    fontSize: 13,
    fontFamily: "Inter_400Regular",
    paddingHorizontal: 32,
    marginTop: 20,
    lineHeight: 20,
  },
  previewWrap: { width: "100%", aspectRatio: 1, borderWidth: 1, overflow: "hidden" },
  preview: { width: "100%", height: "100%" },
  overlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: "rgba(6,12,9,0.75)",
    justifyContent: "center",
    alignItems: "center",
    gap: 20,
  },
  overlayRings: { width: 200, height: 200, justifyContent: "center", alignItems: "center" },
  scanningLabel: { fontSize: 18, fontWeight: "600", fontFamily: "Inter_600SemiBold" },
  buttons: { flexDirection: "row", gap: 12, marginTop: 36 },
  btn: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
    paddingVertical: 16,
    borderRadius: 14,
  },
  btnTextDark: { fontSize: 16, fontWeight: "600", fontFamily: "Inter_600SemiBold", color: "#000" },
  btnText: { fontSize: 16, fontWeight: "600", fontFamily: "Inter_600SemiBold" },
});
