import { Ionicons } from "@expo/vector-icons";
import * as Haptics from "expo-haptics";
import * as ImagePicker from "expo-image-picker";
import * as Device from "expo-device";
import React, { useCallback, useEffect, useRef, useState } from "react";
import {
  Alert,
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
  withSpring,
  withTiming,
} from "react-native-reanimated";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { ref, uploadBytes, getDownloadURL } from "firebase/storage";
import { useColors } from "@/hooks/useColors";
import { useApp } from "@/contexts/AppContext";
import { useAuth } from "@/contexts/AuthContext";
import { storage } from "@/utils/firebase";
import { ScanResultCard, type ScanResult } from "@/components/ScanResultCard";
import { request } from "@/utils/api";
import { logEvent } from "@/utils/analytics";

function ScanRing({ size, delay, color }: { size: number; delay: number; color: string }) {
  const scale = useSharedValue(0.7);
  const opacity = useSharedValue(0.5);

  useEffect(() => {
    const t = setTimeout(() => {
      scale.value = withRepeat(
        withTiming(1.2, { duration: 2200, easing: Easing.out(Easing.ease) }),
        -1,
        false
      );
      opacity.value = withRepeat(
        withSequence(
          withTiming(0, { duration: 2200, easing: Easing.out(Easing.ease) }),
          withTiming(0.5, { duration: 0 })
        ),
        -1,
        false
      );
    }, delay);
    return () => clearTimeout(t);
  }, [delay, opacity, scale]);

  const s = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    opacity: opacity.value,
  }));

  return (
    <Animated.View
      style={[styles.ring, s, { width: size, height: size, borderRadius: size / 2, borderColor: color }]}
    />
  );
}

function ScanLine({ containerHeight }: { containerHeight: number }) {
  const y = useSharedValue(0);

  useEffect(() => {
    if (containerHeight <= 0) return;
    y.value = withRepeat(
      withSequence(
        withTiming(containerHeight, { duration: 1400, easing: Easing.linear }),
        withTiming(0, { duration: 1400, easing: Easing.linear })
      ),
      -1,
      false
    );
  }, [containerHeight, y]);

  const s = useAnimatedStyle(() => ({ transform: [{ translateY: y.value }] }));

  return (
    <Animated.View style={[styles.scanLine, s, { pointerEvents: "none" }]} />
  );
}

function ProgressCounter({ isRunning }: { isRunning: boolean }) {
  const [pct, setPct] = useState(0);
  const interval = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (isRunning) {
      setPct(0);
      interval.current = setInterval(() => {
        setPct((p) => {
          if (p >= 93) {
            if (interval.current) clearInterval(interval.current);
            return 93;
          }
          return p + Math.random() * 4;
        });
      }, 120);
    } else {
      if (interval.current) clearInterval(interval.current);
      setPct(100);
    }
    return () => { if (interval.current) clearInterval(interval.current); };
  }, [isRunning]);

  return (
    <Text style={styles.progressText}>{Math.round(pct)}%</Text>
  );
}

const BASE_RESULTS: ScanResult[] = [
  {
    disease: "Early Blight (Alternaria solani)",
    confidence: 94,
    severity: "high",
    affectedArea: 35,
    isHealthy: false,
    explanation: "Classic early blight showing characteristic concentric-ring lesions with yellowing halos on lower leaves. Infection likely spread during high-humidity periods.",
    recommendations: [
      "Remove and destroy all infected leaves immediately",
      "Avoid overhead irrigation — use drip or furrow",
      "Increase plant spacing for better air circulation",
    ],
    treatments: [
      "Mancozeb 75 WP @ 2.5g/L water every 7–10 days",
      "Chlorothalonil 75 WP @ 2g/L water",
    ],
  },
  {
    disease: "Healthy Crop (No Disease Detected)",
    confidence: 97,
    severity: "low",
    affectedArea: 0,
    isHealthy: true,
    explanation: "Plant shows strong, uniform green foliage with no visible lesions, discolouration, or pest damage. Growth appears vigorous and healthy.",
    recommendations: [
      "Continue current fertilizer and irrigation schedule",
      "Apply preventive copper fungicide before rainy season",
      "Monitor weekly for early disease signs",
    ],
    treatments: [],
  },
];

export default function ScannerScreen() {
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const { addScanRecord } = useApp();
  const { user } = useAuth();
  const topPad = Platform.OS === "web" ? 67 : insets.top + 10;

  const [imageUri, setImageUri] = useState<string | null>(null);
  const [isScanning, setIsScanning] = useState(false);
  const [result, setResult] = useState<ScanResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [containerHeight, setContainerHeight] = useState(0);
  const lastBase64 = useRef<string | null>(null);

  const resultOpacity = useSharedValue(0);
  const resultY = useSharedValue(30);

  const showResult = useCallback((r: ScanResult) => {
    setResult(r);
    resultOpacity.value = withTiming(1, { duration: 400 });
    resultY.value = withSpring(0, { damping: 18 });
  }, [resultOpacity, resultY]);

  const resultStyle = useAnimatedStyle(() => ({
    opacity: resultOpacity.value,
    transform: [{ translateY: resultY.value }],
  }));

  const runScan = useCallback(
    async (uri: string, base64: string) => {
      setImageUri(uri);
      lastBase64.current = base64;
      setIsScanning(true);
      setResult(null);
      setError(null);
      resultOpacity.value = 0;
      resultY.value = 30;
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);

      const controller = new AbortController();

      try {
        // Parallel: API Scan + Cloud Upload (if authenticated)
        const scanPromise = request<ScanResult>("/api/scan", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ imageBase64: base64 }),
          signal: controller.signal,
        });

        let cloudUrl = uri;
        let uploadSucceeded = false;

        if (user) {
          try {
            const response = await fetch(uri);
            const blob = await response.blob();
            const imageId = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
            const storageRef = ref(storage, `scans/${user.uid}/${imageId}.jpg`);
            await uploadBytes(storageRef, blob);
            cloudUrl = await getDownloadURL(storageRef);
            uploadSucceeded = true;
          } catch (storageErr) {
            console.warn("Cloud storage upload failed, using local URI:", storageErr);
            // Non-blocking for the user, but we should log it
            logEvent(user.uid, "upload_failure", { error: String(storageErr) });
          }
        }

        const data = await scanPromise;

        setIsScanning(false);
        showResult(data);
        Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);

        const id = Date.now().toString() + Math.random().toString(36).substr(2, 9);
        addScanRecord({
          id,
          imageUri: cloudUrl,
          disease: data.disease,
          confidence: data.confidence,
          severity: data.severity,
          timestamp: Date.now(),
        });

        // Log analytics
        logEvent(user?.uid, "scan_success", {
          disease: data.disease,
          confidence: data.confidence,
          severity: data.severity,
          isHealthy: data.isHealthy,
          cloudSync: uploadSucceeded,
        });
      } catch (err: any) {
        if (err.name === "AbortError") return;
        setIsScanning(false);
        
        const isNetworkError = err.message?.toLowerCase().includes("network") || err.message?.toLowerCase().includes("fetch");
        const userMsg = isNetworkError 
          ? "Connection too weak for AI analysis. Please move to an area with better signal and retry." 
          : (err.message || "AI Service temporarily unavailable. Please try again in a moment.");
          
        setError(userMsg);
        Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
        
        // Log to Crashlytics / Analytics
        logEvent(user?.uid, "scan_error", {
          message: err.message,
          type: isNetworkError ? "network" : "api",
        });
      }
    },
    [addScanRecord, resultOpacity, resultY, showResult, user]
  );


  const pickImage = useCallback(async () => {
    const perm = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!perm.granted) {
      Alert.alert(
        "Permission Required",
        "Please allow access to your photo library to upload crop images for analysis."
      );
      return;
    }
    // Adaptive quality based on device memory for stability
    const totalMem = Device.totalMemory ?? 4000000000;
    const quality = totalMem < 3000000000 ? 0.4 : 0.6;

    const picked = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ["images"],
      quality,
      base64: true,
    });
    if (!picked.canceled && picked.assets[0]) {
      const { uri, base64 } = picked.assets[0];
      runScan(uri, base64 ?? "");
    }
  }, [runScan]);

  const takePhoto = useCallback(async () => {
    if (Platform.OS === "web") { pickImage(); return; }
    const perm = await ImagePicker.requestCameraPermissionsAsync();
    if (!perm.granted) {
      Alert.alert(
        "Permission Required",
        "Please allow camera access to take photos of your crops for AI diagnosis."
      );
      return;
    }
    // Adaptive quality based on device memory for stability
    const totalMem = Device.totalMemory ?? 4000000000;
    const quality = totalMem < 3000000000 ? 0.4 : 0.6;

    const photo = await ImagePicker.launchCameraAsync({ quality, base64: true });
    if (!photo.canceled && photo.assets[0]) {
      const { uri, base64 } = photo.assets[0];
      runScan(uri, base64 ?? "");
    }
  }, [pickImage, runScan]);

  const reset = () => {
    setImageUri(null);
    setResult(null);
    setIsScanning(false);
    setError(null);
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
              Real AI disease detection
            </Text>
          </View>
          {(imageUri ?? result) ? (
            <TouchableOpacity
              onPress={reset}
              style={[styles.resetBtn, { backgroundColor: colors.card, borderColor: colors.border }]}
            >
              <Ionicons name="refresh" size={20} color={colors.foreground} />
            </TouchableOpacity>
          ) : null}
        </View>

        {!imageUri && !result && (
          <View style={styles.scanArea}>
            <View style={styles.rings}>
              <ScanRing size={290} delay={0} color={colors.primary} />
              <ScanRing size={220} delay={800} color={colors.accent} />
              <ScanRing size={150} delay={1600} color={colors.primary} />
              <View
                style={[styles.centerIcon, { backgroundColor: colors.card, borderColor: colors.border }]}
              >
                <Ionicons name="leaf-outline" size={44} color={colors.primary} />
              </View>
            </View>
            <Text style={[styles.hint, { color: colors.mutedForeground }]}>
              Point your camera at a crop leaf or diseased area. AI will diagnose in seconds.
            </Text>
          </View>
        )}

        {imageUri && (
          <View
            style={[styles.previewWrap, { borderRadius: colors.radius, borderColor: colors.border }]}
            onLayout={(e) => setContainerHeight(e.nativeEvent.layout.height)}
          >
            <Image
              source={{ uri: imageUri }}
              style={[styles.preview, { borderRadius: colors.radius }]}
            />
            {isScanning && (
              <View style={styles.overlay}>
                <ScanLine containerHeight={containerHeight} />
                <View style={styles.analyzeBox}>
                  <View style={styles.analyzeRow}>
                    <View style={[styles.aiDot, { backgroundColor: colors.accent }]} />
                    <Text style={[styles.analyzeLabel, { color: colors.accent }]}>
                      AI Analyzing
                    </Text>
                    <ProgressCounter isRunning={isScanning} />
                  </View>
                  <Text style={[styles.analyzeSubtitle, { color: colors.mutedForeground }]}>
                    Identifying disease patterns...
                  </Text>
                </View>
              </View>
            )}
          </View>
        )}

        {result && !isScanning && (
          <Animated.View style={[{ marginTop: 16 }, resultStyle]}>
            <ScanResultCard result={result} />
          </Animated.View>
        )}

        {error && (
          <View style={[styles.errorBox, { backgroundColor: "#FF453A15", borderColor: "#FF453A30" }]}>
            <View style={{ flex: 1, flexDirection: "row", alignItems: "center", gap: 8 }}>
              <Ionicons name="warning" size={16} color="#FF453A" />
              <Text style={[styles.errorText, { color: "#FF453A" }]}>{error}</Text>
            </View>
            <TouchableOpacity 
              onPress={() => lastBase64.current && runScan(imageUri!, lastBase64.current)}
              style={[styles.retryBtn, { backgroundColor: colors.primary }]}
            >
              <Text style={styles.retryText}>Retry</Text>
            </TouchableOpacity>
          </View>
        )}

        {!isScanning && !result && (
          <View style={styles.buttons}>
            <TouchableOpacity
              style={[styles.btn, { backgroundColor: colors.primary }]}
              onPress={takePhoto}
              activeOpacity={0.85}
            >
              <Ionicons name="camera" size={22} color="#000" />
              <Text style={styles.btnDark}>Take Photo</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[styles.btn, { backgroundColor: colors.card, borderColor: colors.border, borderWidth: 1 }]}
              onPress={pickImage}
              activeOpacity={0.85}
            >
              <Ionicons name="image" size={22} color={colors.foreground} />
              <Text style={[styles.btnLight, { color: colors.foreground }]}>Upload</Text>
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
    width: 40, height: 40, borderRadius: 20,
    justifyContent: "center", alignItems: "center", borderWidth: 1,
  },
  scanArea: { alignItems: "center", paddingVertical: 10 },
  rings: { width: 310, height: 310, justifyContent: "center", alignItems: "center" },
  ring: { position: "absolute", borderWidth: 1.5 },
  centerIcon: {
    width: 96, height: 96, borderRadius: 48,
    justifyContent: "center", alignItems: "center", borderWidth: 1,
  },
  hint: {
    textAlign: "center", fontSize: 13, fontFamily: "Inter_400Regular",
    paddingHorizontal: 28, marginTop: 20, lineHeight: 20,
  },
  previewWrap: { width: "100%", aspectRatio: 1, borderWidth: 1, overflow: "hidden" },
  preview: { width: "100%", height: "100%" },
  overlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: "rgba(6,12,9,0.55)",
    justifyContent: "flex-end",
  },
  scanLine: {
    position: "absolute",
    left: 0,
    right: 0,
    top: 0,
    height: 2,
    backgroundColor: "rgba(74,222,128,0.7)",
    ...Platform.select({
      web: { boxShadow: "0 0 8px 3px rgba(74,222,128,0.7)" },
      default: {
        shadowColor: "#4ADE80",
        shadowOffset: { width: 0, height: 0 },
        shadowOpacity: 0.9,
        shadowRadius: 6,
      },
    }),
  },
  analyzeBox: {
    backgroundColor: "rgba(6,12,9,0.82)",
    padding: 14,
    gap: 4,
    borderTopWidth: 1,
    borderTopColor: "rgba(74,222,128,0.2)",
  },
  analyzeRow: { flexDirection: "row", alignItems: "center", gap: 8 },
  aiDot: { width: 8, height: 8, borderRadius: 4 },
  analyzeLabel: { fontSize: 15, fontWeight: "600", fontFamily: "Inter_600SemiBold" },
  progressText: { fontSize: 15, fontWeight: "700", fontFamily: "Inter_700Bold", color: "#4ADE80", marginLeft: "auto" },
  analyzeSubtitle: { fontSize: 12, fontFamily: "Inter_400Regular" },
  buttons: { flexDirection: "row", gap: 12, marginTop: 36 },
  btn: {
    flex: 1, flexDirection: "row", alignItems: "center",
    justifyContent: "center", gap: 8, paddingVertical: 16, borderRadius: 14,
  },
  btnDark: { fontSize: 16, fontWeight: "600", fontFamily: "Inter_600SemiBold", color: "#000" },
  btnLight: { fontSize: 16, fontWeight: "600", fontFamily: "Inter_600SemiBold" },
  errorBox: {
    flexDirection: "row", alignItems: "center", gap: 8,
    padding: 12, borderRadius: 10, borderWidth: 1, marginTop: 16,
  },
  errorText: { fontSize: 13, fontFamily: "Inter_400Regular", flex: 1 },
  retryBtn: { paddingHorizontal: 12, paddingVertical: 6, borderRadius: 8 },
  retryText: { fontSize: 12, fontWeight: "700", fontFamily: "Inter_700Bold", color: "#000" },
});
