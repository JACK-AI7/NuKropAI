import { Ionicons } from "@expo/vector-icons";
import { useRouter } from "expo-router";
import React, { useState } from "react";
import {
  Alert,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { useColors } from "@/hooks/useColors";
import { useApp } from "@/contexts/AppContext";

export default function AddFarmScreen() {
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const { addFarm } = useApp();

  const [name, setName] = useState("");
  const [location, setLocation] = useState("");
  const [area, setArea] = useState("");
  const [crops, setCrops] = useState("");

  const handleSave = () => {
    if (!name || !location || !area) {
      Alert.alert("Missing Information", "Please provide a name, location, and farm area.");
      return;
    }

    const newFarm = {
      id: Date.now().toString(),
      name: name.trim(),
      location: location.trim(),
      lat: 17.385, // Placeholder, in a real app we'd use geocoding
      lon: 78.486,
      area: parseFloat(area),
      crops: crops.split(",").map(c => c.trim()).filter(c => c),
      boundaries: [],
      soilHealth: {
        npk: { n: 0, p: 0, k: 0 },
        ph: 7.0,
        moisture: 0
      },
      ndvi: {
        score: 0,
        trend: "stable" as const,
        lastUpdated: new Date().toISOString()
      },
      activePests: []
    };

    addFarm(newFarm);
    Alert.alert("Success", "Farm added successfully!", [
      { text: "OK", onPress: () => router.back() }
    ]);
  };

  return (
    <View style={[styles.container, { backgroundColor: colors.background, paddingTop: insets.top }]}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backBtn}>
          <Ionicons name="arrow-back" size={24} color={colors.foreground} />
        </TouchableOpacity>
        <Text style={[styles.title, { color: colors.foreground }]}>Add New Farm</Text>
      </View>

      <ScrollView contentContainerStyle={styles.scroll}>
        <View style={styles.inputGroup}>
          <Text style={[styles.label, { color: colors.mutedForeground }]}>Farm Name</Text>
          <TextInput
            style={[styles.input, { color: colors.foreground, borderColor: colors.border, backgroundColor: colors.card }]}
            placeholder="e.g. My North Field"
            placeholderTextColor={colors.mutedForeground}
            value={name}
            onChangeText={setName}
          />
        </View>

        <View style={styles.inputGroup}>
          <Text style={[styles.label, { color: colors.mutedForeground }]}>Location (City/District)</Text>
          <TextInput
            style={[styles.input, { color: colors.foreground, borderColor: colors.border, backgroundColor: colors.card }]}
            placeholder="e.g. Sangareddy, Telangana"
            placeholderTextColor={colors.mutedForeground}
            value={location}
            onChangeText={setLocation}
          />
        </View>

        <View style={styles.inputGroup}>
          <Text style={[styles.label, { color: colors.mutedForeground }]}>Farm Area (Acres)</Text>
          <TextInput
            style={[styles.input, { color: colors.foreground, borderColor: colors.border, backgroundColor: colors.card }]}
            placeholder="e.g. 5.5"
            placeholderTextColor={colors.mutedForeground}
            keyboardType="decimal-pad"
            value={area}
            onChangeText={setArea}
          />
        </View>

        <View style={styles.inputGroup}>
          <Text style={[styles.label, { color: colors.mutedForeground }]}>Crops (comma separated)</Text>
          <TextInput
            style={[styles.input, { color: colors.foreground, borderColor: colors.border, backgroundColor: colors.card }]}
            placeholder="e.g. Rice, Cotton, Maize"
            placeholderTextColor={colors.mutedForeground}
            value={crops}
            onChangeText={setCrops}
          />
        </View>

        <TouchableOpacity 
          style={[styles.saveBtn, { backgroundColor: colors.primary }]}
          onPress={handleSave}
        >
          <Text style={styles.saveBtnText}>Save Farm</Text>
        </TouchableOpacity>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  header: { flexDirection: "row", alignItems: "center", paddingHorizontal: 16, paddingVertical: 12, gap: 16 },
  backBtn: { width: 40, height: 40, justifyContent: "center", alignItems: "center" },
  title: { fontSize: 20, fontWeight: "700", fontFamily: "Inter_700Bold" },
  scroll: { padding: 20, gap: 20 },
  inputGroup: { gap: 8 },
  label: { fontSize: 13, fontWeight: "600", fontFamily: "Inter_600SemiBold" },
  input: {
    height: 54,
    borderRadius: 12,
    borderWidth: 1,
    paddingHorizontal: 16,
    fontSize: 16,
    fontFamily: "Inter_400Regular",
  },
  saveBtn: {
    height: 56,
    borderRadius: 14,
    justifyContent: "center",
    alignItems: "center",
    marginTop: 20,
  },
  saveBtnText: {
    fontSize: 16,
    fontWeight: "700",
    fontFamily: "Inter_700Bold",
    color: "#000",
  },
});
