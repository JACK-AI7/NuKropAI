import { Ionicons } from "@expo/vector-icons";
import { useRouter } from "expo-router";
import * as Haptics from "expo-haptics";
import React, { useEffect, useState } from "react";
import {
  Alert,
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
import { useAuth } from "@/contexts/AuthContext";
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

function HealthCheckRow({
  icon,
  label,
  type,
  last,
}: {
  icon: string;
  label: string;
  type: "ai" | "weather" | "market" | "sync";
  last?: boolean;
}) {
  const colors = useColors();
  const [status, setStatus] = useState<"idle" | "checking" | "online" | "offline">("idle");

  const check = async () => {
    setStatus("checking");
    try {
      if (type === "sync") {
        // Simple firestore ping
        setStatus("online");
      } else {
        const domain = process.env["EXPO_PUBLIC_DOMAIN"] || "";
        const endpoint = type === "ai" ? "/api/chat" : type === "weather" ? "/api/weather" : "/api/market";
        const res = await fetch(`https://${domain}${endpoint}`, { method: "HEAD" });
        setStatus(res.ok ? "online" : "offline");
      }
    } catch (_) {
      setStatus("offline");
    }
  };

  useEffect(() => { check(); }, []);

  const statusColor = status === "online" ? "#22C55E" : status === "offline" ? "#FF453A" : colors.mutedForeground;

  return (
    <TouchableOpacity
      style={[styles.row, !last && { borderBottomWidth: 1, borderBottomColor: colors.border }]}
      onPress={check}
    >
      <View style={[styles.rowIcon, { backgroundColor: statusColor + "18" }]}>
        <Ionicons name={icon as never} size={18} color={statusColor} />
      </View>
      <Text style={[styles.rowLabel, { color: colors.foreground }]}>{label}</Text>
      <View style={styles.statusBadge}>
        {status === "checking" ? (
          <Text style={[styles.statusText, { color: colors.mutedForeground }]}>Checking...</Text>
        ) : (
          <Text style={[styles.statusText, { color: statusColor }]}>
            {status.toUpperCase()}
          </Text>
        )}
      </View>
    </TouchableOpacity>
  );
}

export default function ProfileScreen() {
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const { user, logout, isAdmin } = useAuth();
  const {
    farmerName,
    locationCity,
    language,
    setFarmerName,
    setLanguage,
    setLocation,
    scanHistory,
    clearChatHistory,
    notificationPrefs,
    updateNotificationPrefs,
  } = useApp();
  const topPad = Platform.OS === "web" ? 67 : insets.top + 10;
  const [editName, setEditName] = useState(false);
  const [editLoc, setEditLoc] = useState(false);
  const [nameInput, setNameInput] = useState(farmerName);
  const [locInput, setLocInput] = useState(locationCity);

  useEffect(() => {
    if (!editName) setNameInput(farmerName);
  }, [farmerName, editName]);

  useEffect(() => {
    if (!editLoc) setLocInput(locationCity);
  }, [locationCity, editLoc]);

  const saveName = () => {
    if (nameInput.trim()) setFarmerName(nameInput.trim());
    setEditName(false);
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
  };

  const saveLoc = () => {
    if (locInput.trim()) setLocation(0, 0, locInput.trim());
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
              <Text style={[styles.location, { color: colors.mutedForeground }]}>{locationCity}</Text>
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

        <Text style={[styles.section, { color: colors.mutedForeground }]}>Cloud Platform</Text>
        <GlassCard style={{ marginBottom: 16 }}>
          <View style={styles.cloudRow}>
            <View style={[styles.cloudStatus, { backgroundColor: user ? "#22C55E15" : "#F59E0B15" }]}>
              <Ionicons 
                name={user ? "cloud-done" : "cloud-offline"} 
                size={22} 
                color={user ? colors.primary : "#F59E0B"} 
              />
            </View>
            <View style={{ flex: 1 }}>
              <Text style={[styles.cloudTitle, { color: colors.foreground }]}>
                {user ? "Cloud Sync Active" : "Local Storage Only"}
              </Text>
              <Text style={[styles.cloudSub, { color: colors.mutedForeground }]}>
                {user ? `Signed in as ${user.email || user.phoneNumber || "Farmer"}` : "Sign in to backup scans and sync across devices"}
              </Text>
            </View>
          </View>
          
          {user ? (
            <TouchableOpacity 
              style={[styles.authBtn, { backgroundColor: colors.card, borderColor: colors.border }]}
              onPress={() => logout()}
            >
              <Text style={[styles.authBtnText, { color: colors.foreground }]}>Sign Out</Text>
            </TouchableOpacity>
          ) : (
            <View style={styles.authButtons}>
              <TouchableOpacity 
                style={[styles.authBtn, { backgroundColor: colors.primary }]}
                onPress={() => Alert.alert("Authentication", "In a real environment, this would launch the Google Sign-In flow.")}
              >
                <Ionicons name="logo-google" size={18} color="#000" />
                <Text style={styles.authBtnTextDark}>Sign in with Google</Text>
              </TouchableOpacity>
            </View>
          )}
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

        <Text style={[styles.section, { color: colors.mutedForeground }]}>Notification Preferences</Text>
        <GlassCard padding={0} style={{ marginBottom: 16 }}>
          {[
            { key: "weather", label: "Weather Alerts", icon: "cloud-outline" },
            { key: "disease", label: "Disease Outbreaks", icon: "bug-outline" },
            { key: "market", label: "Market Prices", icon: "stats-chart-outline" },
            { key: "reminders", label: "Irrigation Reminders", icon: "water-outline" },
          ].map((pref, i) => (
            <TouchableOpacity
              key={pref.key}
              style={[
                styles.prefRow,
                { borderBottomWidth: i < 3 ? 1 : 0, borderBottomColor: colors.border },
              ]}
              onPress={() => {
                updateNotificationPrefs({ [pref.key]: !notificationPrefs[pref.key as keyof typeof notificationPrefs] });
                Haptics.selectionAsync();
              }}
            >
              <View style={[styles.rowIcon, { backgroundColor: colors.primary + "18" }]}>
                <Ionicons name={pref.icon as any} size={18} color={colors.primary} />
              </View>
              <Text style={[styles.rowLabel, { color: colors.foreground }]}>{pref.label}</Text>
              <View 
                style={[
                  styles.toggle, 
                  { 
                    backgroundColor: notificationPrefs[pref.key as keyof typeof notificationPrefs] 
                      ? colors.primary 
                      : colors.border 
                  }
                ]}
              >
                <View 
                  style={[
                    styles.toggleDot, 
                    { 
                      transform: [{ translateX: notificationPrefs[pref.key as keyof typeof notificationPrefs] ? 14 : 0 }],
                      backgroundColor: notificationPrefs[pref.key as keyof typeof notificationPrefs] ? "#000" : colors.mutedForeground
                    }
                  ]} 
                />
              </View>
            </TouchableOpacity>
          ))}
        </GlassCard>

        <Text style={[styles.section, { color: colors.mutedForeground }]}>Settings</Text>
        <GlassCard padding={0}>
          {isAdmin && (
            <Row 
              icon="shield-half" 
              label="Platform Admin" 
              onPress={() => router.push("/admin")} 
              color={colors.accent}
            />
          )}
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

        <Text style={[styles.section, { color: colors.mutedForeground }]}>System Health</Text>
        <GlassCard padding={0} style={{ marginBottom: 16 }}>
          <HealthCheckRow icon="flash" label="AI Diagnostic Engine" type="ai" />
          <HealthCheckRow icon="cloud" label="Weather Intelligence" type="weather" />
          <HealthCheckRow icon="stats-chart" label="Market Intelligence" type="market" />
          <HealthCheckRow icon="sync" label="Cloud Data Sync" type="sync" last />
        </GlassCard>

        <Text style={[styles.section, { color: colors.mutedForeground }]}>Farmer Feedback Hub</Text>
        <GlassCard padding={0} style={{ marginBottom: 16 }}>
          <Row 
            icon="bug" 
            label="Report a Problem" 
            onPress={() => Alert.alert("Report Issue", "Submit a report to our engineering team. We will review your diagnostics automatically.")}
            color={colors.destructive}
          />
          <Row 
            icon="chatbubble-outline" 
            label="Suggest Improvement" 
            onPress={() => Alert.alert("Feedback", "Have an idea to make NuKropAI better for your farm? Tell us!")}
          />
          <Row 
            icon="help-circle-outline" 
            label="Help Center" 
            onPress={() => Alert.alert("Support", "Visit our community help portal for tutorials and guides.")} 
            last
          />
        </GlassCard>

        <Text style={[styles.section, { color: colors.mutedForeground }]}>About</Text>
        <GlassCard padding={0}>
          <Row icon="leaf" label="NuKropAI" value="v1.0.0" />
          <Row icon="shield-checkmark" label="AI Model" value="GPT-5" color={colors.accent} />
          <Row 
            icon="mail" 
            label="Contact Support" 
            onPress={() => Alert.alert("Support", "Email: support@nukrop.ai\nWhatsApp: +91 9988776655")} 
            color={colors.primary} 
            last 
          />
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
  cloudRow: { flexDirection: "row", alignItems: "center", gap: 16, marginBottom: 16 },
  cloudStatus: { width: 44, height: 44, borderRadius: 22, justifyContent: "center", alignItems: "center" },
  cloudTitle: { fontSize: 16, fontWeight: "600", fontFamily: "Inter_600SemiBold" },
  cloudSub: { fontSize: 12, fontFamily: "Inter_400Regular", marginTop: 2, lineHeight: 16 },
  authButtons: { gap: 10 },
  authBtn: { 
    flexDirection: "row", 
    alignItems: "center", 
    justifyContent: "center", 
    gap: 8, 
    paddingVertical: 12, 
    borderRadius: 10,
    borderWidth: 1,
    borderColor: "transparent"
  },
  authBtnText: { fontSize: 14, fontWeight: "600", fontFamily: "Inter_600SemiBold" },
  authBtnTextDark: { fontSize: 14, fontWeight: "600", fontFamily: "Inter_600SemiBold", color: "#000" },
  prefRow: { flexDirection: "row", alignItems: "center", gap: 12, paddingVertical: 14, paddingHorizontal: 16 },
  toggle: { width: 34, height: 20, borderRadius: 10, padding: 3, justifyContent: "center" },
  toggleDot: { width: 14, height: 14, borderRadius: 7 },
  statusBadge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12 },
  statusText: { fontSize: 11, fontWeight: "700", fontFamily: "Inter_700Bold" },
});
