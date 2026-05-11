import { Ionicons } from "@expo/vector-icons";
import * as Haptics from "expo-haptics";
import React, { useCallback, useEffect, useRef, useState } from "react";
import {
  ActivityIndicator,
  Alert,
  FlatList,
  Platform,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";
import { KeyboardAvoidingView } from "react-native-keyboard-controller";
import Animated, {
  useAnimatedStyle,
  useSharedValue,
  withRepeat,
  withSequence,
  withTiming,
} from "react-native-reanimated";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { useColors } from "@/hooks/useColors";
import { useApp, type ChatMessage, type Language } from "@/contexts/AppContext";
import { useAuth } from "@/contexts/AuthContext";
import { MessageBubble } from "@/components/MessageBubble";
import { VoiceWaveform } from "@/components/VoiceWaveform";
import { request } from "@/utils/api";
import { logEvent } from "@/utils/analytics";

const LANG_LABELS: Record<Language, string> = { en: "EN", hi: "हि", te: "తె" };

const WELCOME: ChatMessage = {
  id: "welcome",
  role: "assistant",
  content:
    "Namaste! I am NuKropAI, your intelligent farming assistant. Ask me anything about crop diseases, pest management, fertilizers, weather decisions, or government schemes.",
  timestamp: Date.now() - 120000,
};

function RecordingPulse({ color }: { color: string }) {
  const scale = useSharedValue(1);
  useEffect(() => {
    scale.value = withRepeat(
      withSequence(
        withTiming(1.35, { duration: 600 }),
        withTiming(1, { duration: 600 })
      ),
      -1,
      false
    );
  }, [scale]);
  const s = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    opacity: 2 - scale.value,
  }));
  return (
    <Animated.View
      style={[
        {
          position: "absolute",
          width: 42,
          height: 42,
          borderRadius: 21,
          backgroundColor: color + "30",
        },
        s,
      ]}
    />
  );
}

export default function ChatScreen() {
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const { user } = useAuth();
  const { 
    language, 
    setLanguage, 
    chatHistory, 
    addChatMessage,
    farmerName,
    farmLocation,
    cropsGrown,
    scanHistory
  } = useApp();
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [streaming, setStreaming] = useState<{ id: string; content: string; timestamp: number } | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const typingInterval = useRef<ReturnType<typeof setInterval> | null>(null);
  const recordingRef = useRef<{ stopAndUnloadAsync: () => Promise<unknown>; getURI: () => string | null } | null>(null);
  const bottomPad = Platform.OS === "web" ? 34 : insets.bottom;

  const allMessages: ChatMessage[] = [WELCOME, ...chatHistory];
  const reversed = [...allMessages].reverse();
  const listData: ChatMessage[] = streaming
    ? [{ id: streaming.id, role: "assistant", content: streaming.content, timestamp: streaming.timestamp }, ...reversed]
    : reversed;

  useEffect(() => {
    return () => {
      if (typingInterval.current) clearInterval(typingInterval.current);
    };
  }, []);

  const typewriterReveal = useCallback(
    (id: string, text: string, ts: number) => {
      addChatMessage({ id, role: "assistant", content: text, timestamp: ts });
    },
    [addChatMessage]
  );

  const send = useCallback(
    async (overrideText?: string) => {
      const text = (overrideText ?? input).trim();
      if (!text || isLoading) return;
      if (!overrideText) setInput("");
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);

      const userMsg: ChatMessage = {
        id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
        role: "user",
        content: text,
        timestamp: Date.now(),
      };
      addChatMessage(userMsg);
      setIsLoading(true);

      const aiId = (Date.now() + 1).toString() + Math.random().toString(36).substr(2, 9);
      const aiTs = Date.now();
      const controller = new AbortController();

      try {
        const history = chatHistory
          .slice(-12)
          .map((m) => ({ role: m.role, content: m.content }));
        
        // Context Enrichment
        const userContext = {
          farmerName,
          location: farmLocation,
          crops: cropsGrown,
          recentDiseases: scanHistory.slice(0, 5).map(s => s.disease),
          language,
        };

        const base = process.env["EXPO_PUBLIC_DOMAIN"]
          ? `https://${process.env["EXPO_PUBLIC_DOMAIN"]}`
          : "";

        const res = await fetch(`${base}/api/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ 
            message: text, 
            language, 
            history, 
            stream: true,
            context: userContext // Added context for personalization
          }),
          signal: controller.signal,
        });

        if (!res.ok) throw new Error("Connection failed");

        // Use streaming if available, else fallback to JSON
        const reader = res.body?.getReader();
        if (!reader) {
          const data = (await res.json()) as { reply: string };
          addChatMessage({ id: aiId, role: "assistant", content: data.reply, timestamp: aiTs });
          setIsLoading(false);
          return;
        }

        const decoder = new TextDecoder();
        let accumulated = "";
        setStreaming({ id: aiId, content: "", timestamp: aiTs });

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split("\n");

          for (const line of lines) {
            if (line.startsWith("data: ")) {
              try {
                const data = JSON.parse(line.slice(6));
                if (data.content) {
                  accumulated += data.content;
                  setStreaming({ id: aiId, content: accumulated, timestamp: aiTs });
                }
                if (data.done) break;
              } catch (e) {
                // Ignore parse errors for incomplete JSON
              }
            }
          }
        }

        addChatMessage({ id: aiId, role: "assistant", content: accumulated, timestamp: aiTs });
        setStreaming(null);

        // Log analytics
        logEvent(user?.uid, "chat", { messageLength: text.length, language });
      } catch (err: any) {
        if (err.name === "AbortError") return;
        typewriterReveal(
          aiId,
          "I'm having trouble connecting right now. Please check your internet connection and try again.",
          aiTs
        );
      } finally {
        setIsLoading(false);
        setStreaming(null);
      }
    },
    [input, isLoading, language, chatHistory, addChatMessage, typewriterReveal]
  );

  const startRecording = useCallback(async () => {
    if (Platform.OS === "web") {
      Alert.alert("Voice input is not available in the browser preview. Use the Expo Go app on your phone.");
      return;
    }
    try {
      const { Audio } = await import("expo-av");
      const perm = await Audio.requestPermissionsAsync();
      if (!perm.granted) {
        Alert.alert(
          "Microphone Required",
          "Please allow microphone access to use voice input for AI Chat."
        );
        return;
      }
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });
      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );
      recordingRef.current = recording;
      setIsRecording(true);
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    } catch (_) {
      Alert.alert("Microphone Error", "Could not initialize recording. Please try again.");
    }
  }, []);

  const stopRecording = useCallback(async () => {
    if (!recordingRef.current) return;
    setIsRecording(false);
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    try {
      await recordingRef.current.stopAndUnloadAsync();
      const uri = recordingRef.current.getURI();
      recordingRef.current = null;
      if (!uri) return;
      setIsTranscribing(true);
      const formData = new FormData();
      formData.append("audio", {
        uri,
        type: "audio/m4a",
        name: "recording.m4a",
      } as unknown as Blob);
      
      const data = await request<{ text: string }>("/api/voice", {
        method: "POST",
        body: formData,
      });
      if (data.text?.trim()) {
        setInput((prev) => (prev ? `${prev} ${data.text}` : data.text));
        Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      }
    } catch (_) {
      Alert.alert("Transcription failed", "Please try again.");
    } finally {
      setIsTranscribing(false);
    }
  }, []);

  const isStreamingCurrent = streaming !== null;

  return (
    <KeyboardAvoidingView
      behavior="padding"
      keyboardVerticalOffset={0}
      style={[styles.container, { backgroundColor: colors.background }]}
    >
      <View
        style={[
          styles.langBar,
          {
            backgroundColor: colors.card,
            borderBottomColor: colors.border,
            paddingTop: Platform.OS === "web" ? 67 : insets.top + 8,
          },
        ]}
      >
        <View style={styles.langLeft}>
          <Ionicons name="globe" size={16} color={colors.mutedForeground} />
          <Text style={[styles.langTitle, { color: colors.mutedForeground }]}>Language</Text>
        </View>
        <View style={styles.langBtns}>
          {(["en", "hi", "te"] as Language[]).map((lang) => (
            <TouchableOpacity
              key={lang}
              onPress={() => setLanguage(lang)}
              style={[
                styles.langBtn,
                {
                  backgroundColor: language === lang ? colors.primary : "transparent",
                  borderColor: language === lang ? colors.primary : colors.border,
                },
              ]}
            >
              <Text
                style={[
                  styles.langBtnText,
                  { color: language === lang ? "#000" : colors.foreground },
                ]}
              >
                {LANG_LABELS[lang]}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      <FlatList
        data={listData}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => {
          const isCurrentlyStreaming = streaming?.id === item.id;
          return (
            <View>
              <MessageBubble role={item.role} content={item.content} timestamp={item.timestamp} />
              {isCurrentlyStreaming && item.content.length > 0 && (
                <Text style={[styles.cursor, { color: colors.accent }]}>▌</Text>
              )}
            </View>
          );
        }}
        inverted={true}
        contentContainerStyle={styles.msgList}
        ListHeaderComponent={
          isLoading && !isStreamingCurrent ? (
            <View style={styles.typing}>
              <ActivityIndicator size="small" color={colors.primary} />
              <Text style={[styles.typingText, { color: colors.mutedForeground }]}>
                NuKropAI is thinking...
              </Text>
            </View>
          ) : null
        }
        keyboardShouldPersistTaps="handled"
        keyboardDismissMode="interactive"
        showsVerticalScrollIndicator={false}
      />

      <View
        style={[
          styles.inputBar,
          {
            backgroundColor: colors.card,
            borderTopColor: colors.border,
            paddingBottom: bottomPad + 6,
          },
        ]}
      >
        {isRecording ? (
          <View style={styles.recordingRow}>
            <View style={[styles.recDot, { backgroundColor: "#FF453A" }]} />
            <VoiceWaveform isRecording={isRecording} color="#FF453A" />
            <Text style={[styles.recLabel, { color: "#FF453A" }]}>Recording…</Text>
          </View>
        ) : isTranscribing ? (
          <View style={styles.recordingRow}>
            <ActivityIndicator size="small" color={colors.accent} />
            <Text style={[styles.recLabel, { color: colors.accent }]}>Transcribing…</Text>
          </View>
        ) : (
          <TextInput
            style={[
              styles.input,
              {
                backgroundColor: colors.background,
                color: colors.foreground,
                borderColor: input.trim() ? colors.primary + "80" : colors.border,
              },
            ]}
            value={input}
            onChangeText={setInput}
            placeholder={
              language === "hi"
                ? "फसल के बारे में पूछें..."
                : language === "te"
                ? "పంట గురించి అడగండి..."
                : "Ask about crops, diseases, fertilizers..."
            }
            placeholderTextColor={colors.mutedForeground}
            multiline
            maxLength={500}
            returnKeyType="send"
            blurOnSubmit={false}
            onSubmitEditing={() => send()}
          />
        )}

        <View style={styles.btnGroup}>
          <TouchableOpacity
            style={[
              styles.micBtn,
              {
                backgroundColor: isRecording
                  ? "#FF453A"
                  : isTranscribing
                  ? colors.card
                  : colors.background,
                borderColor: isRecording ? "#FF453A" : colors.border,
              },
            ]}
            onPressIn={startRecording}
            onPressOut={stopRecording}
            disabled={isLoading || isTranscribing}
            activeOpacity={0.85}
          >
            {isRecording && <RecordingPulse color="#FF453A" />}
            {isTranscribing ? (
              <ActivityIndicator size="small" color={colors.accent} />
            ) : (
              <Ionicons
                name={isRecording ? "stop" : "mic"}
                size={17}
                color={isRecording ? "#fff" : colors.mutedForeground}
              />
            )}
          </TouchableOpacity>

          <TouchableOpacity
            style={[
              styles.sendBtn,
              {
                backgroundColor: input.trim() && !isLoading && !isRecording
                  ? colors.primary
                  : colors.border,
              },
            ]}
            onPress={() => send()}
            disabled={!input.trim() || isLoading || isRecording}
            activeOpacity={0.85}
          >
            {isLoading ? (
              <ActivityIndicator size="small" color={colors.mutedForeground} />
            ) : (
              <Ionicons
                name="send"
                size={16}
                color={input.trim() && !isRecording ? "#000" : colors.mutedForeground}
              />
            )}
          </TouchableOpacity>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  langBar: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 16,
    paddingBottom: 12,
    borderBottomWidth: 1,
  },
  langLeft: { flexDirection: "row", alignItems: "center", gap: 6 },
  langTitle: { fontSize: 13, fontFamily: "Inter_400Regular" },
  langBtns: { flexDirection: "row", gap: 6 },
  langBtn: {
    paddingHorizontal: 14,
    paddingVertical: 6,
    borderRadius: 20,
    borderWidth: 1,
  },
  langBtnText: { fontSize: 13, fontWeight: "600", fontFamily: "Inter_600SemiBold" },
  msgList: { paddingTop: 12, paddingBottom: 8 },
  typing: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    paddingHorizontal: 20,
    paddingVertical: 8,
  },
  typingText: { fontSize: 13, fontFamily: "Inter_400Regular", fontStyle: "italic" },
  cursor: { marginLeft: 64, marginTop: -4, fontSize: 16, lineHeight: 20 },
  inputBar: {
    flexDirection: "row",
    alignItems: "flex-end",
    gap: 8,
    paddingHorizontal: 12,
    paddingTop: 10,
    borderTopWidth: 1,
  },
  recordingRow: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
    paddingLeft: 4,
    paddingVertical: 6,
  },
  recDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  recLabel: { fontSize: 13, fontFamily: "Inter_500Medium" },
  input: {
    flex: 1,
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderRadius: 22,
    borderWidth: 1.5,
    fontSize: 14,
    fontFamily: "Inter_400Regular",
    maxHeight: 100,
  },
  btnGroup: { flexDirection: "row", gap: 6 },
  micBtn: {
    width: 42,
    height: 42,
    borderRadius: 21,
    justifyContent: "center",
    alignItems: "center",
    borderWidth: 1,
  },
  sendBtn: {
    width: 42,
    height: 42,
    borderRadius: 21,
    justifyContent: "center",
    alignItems: "center",
  },
});
