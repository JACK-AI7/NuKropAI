import { Ionicons } from "@expo/vector-icons";
import * as Haptics from "expo-haptics";
import React, { useState } from "react";
import {
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { useColors } from "@/hooks/useColors";
import { useApp, type Language } from "@/contexts/AppContext";
import { GlassCard } from "@/components/GlassCard";

const LANGS: { key: Language; label: string; native: string }[] = [
  { key: "en", label: "English", native: "English" },
  { key: "hi", label: "Hindi", native: "हिन्दी" },
  { key: "te", label: "Telugu", native: "తెలుగు" },
];

function Row({
  icon,
  label,
  value,
  onPress,
  color,
  last,
}: {
  icon: string;
  label: string;
  value?: string;
  onPress?: () => void;
  color?: string;
  last?: boolean;
}) {
  const colors = useColors();
  const ic = color ?? colors.primary;
  return (
    <TouchableOpacity
      style={[styles.row, !last && { borderBottomWidth: 1, borderBottomColor: colors.border }]}
      onPress={onPress}
      activeOpacity={onPress ? 0.7 : 1}
    >
      <View style={[styles.rowIcon, { backgroundColor: ic + "18" }]}>
        <Ionicons name={icon as never} size={18} color={ic} />
      </View>
      <Text style={[styles.rowLabel, { color: colors.foreground }]}>{label}</Text>
      {value && <Text style={[styles.rowValue, { color: colors.mutedForeground }]}>{value}</Text>}
      {onPress && <Ionicons name="chevron-forward" size={14} color={colors.mutedForeground} />}
    </TouchableOpacity>
  );
}

export default function ProfileScreen() {
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const {
    farmerName,
    farmLocation,
    language,
    setFarmerName,
    setFarmLocation,
    setLanguage,
    scanHistory,
    clearChatHistory,
  } = useApp();
  const topPad = Platform.OS === "web" ? 67 : insets.top + 10;
  const [editName, setEditName] = useState(false);
  const [editLoc, setEditLoc] = useState(false);
  const [nameInput, setNameInput] = useState(farmerName);
  const [locInput, setLocInput] = useState(farmLocation);

  const saveName = () => {
    if (nameInput.trim()) setFarmerName(nameInput.trim());
    setEditName(false);
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
  };

  const saveLoc = () => {
    if (locInput.trim()) setFarmLocation(locInput.trim());
    setEditLoc(false);
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
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
        <Text style={[styles.title, { color: colors.foreground }]}>Profile</Text>

        <GlassCard style={styles.profileCard}>
          <View
            style={[
              styles.avatar,
              { backgroundColor: colors.primary + "1A", borderColor: colors.primary + "40" },
            ]}
          >
            <Ionicons name="person" size={38} color={colors.primary} />
          </View>

          {editName ? (
            <View style={styles.editRow}>
              <TextInput
                style={[
                  styles.editInput,
                  {
                    color: colors.foreground,
                    borderColor: colors.border,
                    backgroundColor: colors.background,
                  },
                ]}
                value={nameInput}
                onChangeText={setNameInput}
                autoFocus
                onSubmitEditing={saveName}
              />
              <TouchableOpacity onPress={saveName}>
                <Ionicons name="checkmark-circle" size={28} color={colors.primary} />
              </TouchableOpacity>
            </View>
          ) : (
            <TouchableOpacity style={styles.nameRow} onPress={() => setEditName(true)}>
              <Text style={[styles.farmerName, { color: colors.foreground }]}>{farmerName}</Text>
              <Ionicons name="pencil" size={15} color={colors.mutedForeground} />
            </TouchableOpacity>
          )}

          {editLoc ? (
            <View style={styles.editRow}>
              <TextInput
                style={[
                  styles.editInput,
                  styles.editSmall,
                  {
                    color: colors.foreground,
                    borderColor: colors.border,
                    backgroundColor: colors.background,
                  },
                ]}
                value={locInput}
                onChangeText={setLocInput}
                onSubmitEditing={saveLoc}
              />
              <TouchableOpacity onPress={saveLoc}>
                <Ionicons name="checkmark-circle" size={24} color={colors.primary} />
              </TouchableOpacity>
            </View>
          ) : (
            <TouchableOpacity style={styles.nameRow} onPress={() => setEditLoc(true)}>
              <Ionicons name="location" size={13} color={colors.mutedForeground} />
              <Text style={[styles.location, { color: colors.mutedForeground }]}>{farmLocation}</Text>
              <Ionicons name="pencil" size={13} color={colors.mutedForeground} />
            </TouchableOpacity>
          )}

          <View style={styles.statsRow}>
            {[
              { label: "Scans", value: String(scanHistory.length) },
              { label: "Health", value: "78%" },
              { label: "Alerts", value: "3" },
            ].map((s, i) => (
              <React.Fragment key={i}>
                {i > 0 && (
                  <View style={[styles.statDiv, { backgroundColor: colors.border }]} />
                )}
                <View style={styles.statItem}>
                  <Text style={[styles.statVal, { color: colors.foreground }]}>{s.value}</Text>
                  <Text style={[styles.statLbl, { color: colors.mutedForeground }]}>{s.label}</Text>
                </View>
              </React.Fragment>
            ))}
          </View>
        </GlassCard>

        <Text style={[styles.section, { color: colors.mutedForeground }]}>Language</Text>
        <GlassCard style={{ marginBottom: 16 }} padding={0}>
          {LANGS.map((opt, i) => (
            <TouchableOpacity
              key={opt.key}
              style={[
                styles.langRow,
                {
                  borderBottomWidth: i < LANGS.length - 1 ? 1 : 0,
                  borderBottomColor: colors.border,
                },
              ]}
              onPress={() => {
                setLanguage(opt.key);
                Haptics.selectionAsync();
              }}
            >
              <View>
                <Text style={[styles.langLabel, { color: colors.foreground }]}>{opt.label}</Text>
                <Text style={[styles.langNative, { color: colors.mutedForeground }]}>
                  {opt.native}
                </Text>
              </View>
              {language === opt.key && (
                <Ionicons name="checkmark-circle" size={22} color={colors.primary} />
              )}
            </TouchableOpacity>
          ))}
        </GlassCard>

        <Text style={[styles.section, { color: colors.mutedForeground }]}>Settings</Text>
        <GlassCard padding={0}>
          <Row icon="notifications" label="AI Notifications" value="On" />
          <Row icon="wifi" label="Offline Mode" value="Coming Soon" />
          <Row
            icon="chatbubble-ellipses"
            label="Clear Chat History"
            onPress={() => {
              clearChatHistory();
              Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
            }}
            color={colors.destructive}
            last
          />
        </GlassCard>

        <Text style={[styles.section, { color: colors.mutedForeground }]}>About</Text>
        <GlassCard padding={0}>
          <Row icon="leaf" label="NuKropAI" value="v1.0.0" />
          <Row icon="shield-checkmark" label="AI Model" value="GPT-5" color={colors.accent} />
          <Row icon="globe" label="Languages" value="3 Supported" color="#8B5CF6" last />
        </GlassCard>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  scroll: { paddingHorizontal: 16 },
  title: { fontSize: 24, fontWeight: "700", fontFamily: "Inter_700Bold", letterSpacing: -0.5, marginBottom: 20 },
  profileCard: { alignItems: "center", gap: 10, marginBottom: 24 },
  avatar: {
    width: 76,
    height: 76,
    borderRadius: 38,
    justifyContent: "center",
    alignItems: "center",
    borderWidth: 2,
    marginBottom: 2,
  },
  nameRow: { flexDirection: "row", alignItems: "center", gap: 6 },
  farmerName: { fontSize: 20, fontWeight: "700", fontFamily: "Inter_700Bold" },
  location: { fontSize: 13, fontFamily: "Inter_400Regular" },
  editRow: { flexDirection: "row", alignItems: "center", gap: 10, width: "100%" },
  editInput: {
    flex: 1,
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 10,
    borderWidth: 1,
    fontSize: 16,
    fontFamily: "Inter_400Regular",
  },
  editSmall: { fontSize: 14 },
  statsRow: { flexDirection: "row", alignItems: "center", marginTop: 12, width: "100%" },
  statItem: { flex: 1, alignItems: "center", gap: 4 },
  statVal: { fontSize: 20, fontWeight: "700", fontFamily: "Inter_700Bold" },
  statLbl: { fontSize: 11, fontFamily: "Inter_400Regular" },
  statDiv: { width: 1, height: 38 },
  section: { fontSize: 13, fontWeight: "600", fontFamily: "Inter_600SemiBold", marginBottom: 10, marginTop: 6, textTransform: "uppercase", letterSpacing: 0.5 },
  langRow: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", paddingVertical: 12, paddingHorizontal: 16 },
  langLabel: { fontSize: 15, fontFamily: "Inter_500Medium" },
  langNative: { fontSize: 13, fontFamily: "Inter_400Regular", marginTop: 2 },
  row: { flexDirection: "row", alignItems: "center", gap: 12, paddingVertical: 14, paddingHorizontal: 16 },
  rowIcon: { width: 34, height: 34, borderRadius: 10, justifyContent: "center", alignItems: "center" },
  rowLabel: { flex: 1, fontSize: 15, fontFamily: "Inter_400Regular" },
  rowValue: { fontSize: 13, fontFamily: "Inter_400Regular" },
});
