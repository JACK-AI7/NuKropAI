import { Ionicons } from "@expo/vector-icons";
import * as Haptics from "expo-haptics";
import React, { useCallback, useRef, useState } from "react";
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

const LANG_LABELS: Record<Language, string> = { en: "EN", hi: "HI", te: "TE" };

const WELCOME: ChatMessage = {
  id: "welcome",
  role: "assistant",
  content:
    "Namaste! I am NuKropAI, your intelligent farming assistant. Ask me anything about crop diseases, pest management, fertilizers, weather decisions, or government schemes.",
  timestamp: Date.now() - 120000,
};

export default function ChatScreen() {
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const { language, setLanguage, chatHistory, addChatMessage } = useApp();
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const listRef = useRef<FlatList>(null);
  const bottomPad = Platform.OS === "web" ? 34 : insets.bottom;

  const allMessages: ChatMessage[] = [WELCOME, ...chatHistory];
  const reversed = [...allMessages].reverse();

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

    try {
      const history = chatHistory
        .slice(-10)
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
      addChatMessage({
        id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
        role: "assistant",
        content: data.reply,
        timestamp: Date.now(),
      });
    } catch (_) {
      addChatMessage({
        id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
        role: "assistant",
        content:
          "I'm having trouble connecting. Please check your internet connection and try again.",
        timestamp: Date.now(),
      });
    } finally {
      setIsLoading(false);
    }
  }, [input, isLoading, language, chatHistory, addChatMessage]);

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
        <Text style={[styles.langTitle, { color: colors.mutedForeground }]}>Language:</Text>
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

      <FlatList
        ref={listRef}
        data={reversed}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <MessageBubble role={item.role} content={item.content} timestamp={item.timestamp} />
        )}
        inverted={true}
        contentContainerStyle={styles.msgList}
        ListHeaderComponent={
          isLoading ? (
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
        scrollEnabled={true}
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
              borderColor: colors.border,
            },
          ]}
          value={input}
          onChangeText={setInput}
          placeholder={
            language === "hi"
              ? "अपना प्रश्न पूछें..."
              : language === "te"
              ? "మీ ప్రశ్న అడగండి..."
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
            { backgroundColor: input.trim() ? colors.primary : colors.border },
          ]}
          onPress={send}
          disabled={!input.trim() || isLoading}
          activeOpacity={0.8}
        >
          <Ionicons name="send" size={17} color={input.trim() ? "#000" : colors.mutedForeground} />
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
    gap: 8,
    paddingHorizontal: 16,
    paddingBottom: 12,
    borderBottomWidth: 1,
  },
  langTitle: { fontSize: 13, fontFamily: "Inter_400Regular" },
  langBtn: {
    paddingHorizontal: 12,
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
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  typingText: { fontSize: 13, fontFamily: "Inter_400Regular", fontStyle: "italic" },
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
    borderWidth: 1,
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
