import { Ionicons } from "@expo/vector-icons";
import * as Haptics from "expo-haptics";
import React, { useCallback, useEffect, useRef, useState } from "react";
import {
  ActivityIndicator,
  FlatList,
  Platform,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";
import { KeyboardAvoidingView } from "react-native-keyboard-controller";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { useColors } from "@/hooks/useColors";
import { useApp, type ChatMessage, type Language } from "@/contexts/AppContext";
import { MessageBubble } from "@/components/MessageBubble";

const LANG_LABELS: Record<Language, string> = { en: "EN", hi: "हि", te: "తె" };

const WELCOME: ChatMessage = {
  id: "welcome",
  role: "assistant",
  content:
    "Namaste! I am NuKropAI, your intelligent farming assistant. Ask me anything about crop diseases, pest management, fertilizers, weather decisions, or government schemes.",
  timestamp: Date.now() - 120000,
};

interface StreamingMessage {
  id: string;
  content: string;
  timestamp: number;
}

export default function ChatScreen() {
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const { language, setLanguage, chatHistory, addChatMessage } = useApp();
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [streaming, setStreaming] = useState<StreamingMessage | null>(null);
  const typingInterval = useRef<ReturnType<typeof setInterval> | null>(null);
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
    (id: string, fullText: string, ts: number) => {
      let i = 0;
      if (typingInterval.current) clearInterval(typingInterval.current);
      setStreaming({ id, content: "", timestamp: ts });

      typingInterval.current = setInterval(() => {
        i += 2;
        const displayed = fullText.slice(0, i);
        setStreaming({ id, content: displayed, timestamp: ts });
        if (i >= fullText.length) {
          clearInterval(typingInterval.current!);
          typingInterval.current = null;
          setStreaming(null);
          addChatMessage({ id, role: "assistant", content: fullText, timestamp: ts });
        }
      }, 16);
    },
    [addChatMessage]
  );

  const send = useCallback(async () => {
    const text = input.trim();
    if (!text || isLoading) return;
    setInput("");
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

    try {
      const history = chatHistory
        .slice(-12)
        .map((m) => ({ role: m.role, content: m.content }));
      const base = process.env["EXPO_PUBLIC_DOMAIN"]
        ? `https://${process.env["EXPO_PUBLIC_DOMAIN"]}`
        : "";

      const res = await fetch(`${base}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, language, history }),
      });

      const data = (await res.json()) as { reply: string };
      setIsLoading(false);
      typewriterReveal(aiId, data.reply, aiTs);
    } catch (_) {
      setIsLoading(false);
      const errMsg =
        "I'm having trouble connecting right now. Please check your internet connection and try again.";
      typewriterReveal(aiId, errMsg, aiTs);
    }
  }, [input, isLoading, language, chatHistory, addChatMessage, typewriterReveal]);

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
                <View style={[styles.cursor, { marginLeft: 64, marginTop: -2 }]}>
                  <Text style={{ color: colors.accent, fontSize: 16, lineHeight: 20 }}>▌</Text>
                </View>
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
          onSubmitEditing={send}
        />
        <TouchableOpacity
          style={[
            styles.sendBtn,
            {
              backgroundColor: input.trim() && !isLoading ? colors.primary : colors.border,
            },
          ]}
          onPress={send}
          disabled={!input.trim() || isLoading}
          activeOpacity={0.85}
        >
          {isLoading ? (
            <ActivityIndicator size="small" color={colors.mutedForeground} />
          ) : (
            <Ionicons name="send" size={16} color={input.trim() ? "#000" : colors.mutedForeground} />
          )}
        </TouchableOpacity>
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
  cursor: {},
  inputBar: {
    flexDirection: "row",
    alignItems: "flex-end",
    gap: 10,
    paddingHorizontal: 16,
    paddingTop: 12,
    borderTopWidth: 1,
  },
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
  sendBtn: {
    width: 42,
    height: 42,
    borderRadius: 21,
    justifyContent: "center",
    alignItems: "center",
  },
});
