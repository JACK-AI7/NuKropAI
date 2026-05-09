import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { useColors } from "@/hooks/useColors";

interface MessageBubbleProps {
  role: "user" | "assistant";
  content: string;
  timestamp: number;
}

function fmt(ts: number) {
  return new Date(ts).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

export function MessageBubble({ role, content, timestamp }: MessageBubbleProps) {
  const colors = useColors();
  const isUser = role === "user";

  return (
    <View style={[styles.wrapper, isUser ? styles.userWrapper : styles.aiWrapper]}>
      {!isUser && (
        <View
          style={[
            styles.avatar,
            { backgroundColor: colors.primary + "20", borderColor: colors.primary + "40" },
          ]}
        >
          <Text style={{ fontSize: 10, fontFamily: "Inter_700Bold", color: colors.primary }}>AI</Text>
        </View>
      )}
      <View
        style={[
          styles.bubble,
          isUser
            ? {
                backgroundColor: colors.primary,
                borderRadius: 18,
                borderBottomRightRadius: 4,
              }
            : {
                backgroundColor: colors.card,
                borderRadius: 18,
                borderBottomLeftRadius: 4,
                borderWidth: 1,
                borderColor: colors.border,
              },
        ]}
      >
        <Text style={[styles.text, { color: isUser ? "#000" : colors.foreground }]}>{content}</Text>
        <Text style={[styles.time, { color: isUser ? "#00000055" : colors.mutedForeground }]}>
          {fmt(timestamp)}
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  wrapper: {
    flexDirection: "row",
    marginVertical: 3,
    paddingHorizontal: 16,
    gap: 8,
    alignItems: "flex-end",
  },
  userWrapper: { justifyContent: "flex-end" },
  aiWrapper: { justifyContent: "flex-start" },
  avatar: {
    width: 28,
    height: 28,
    borderRadius: 14,
    justifyContent: "center",
    alignItems: "center",
    borderWidth: 1,
  },
  bubble: {
    maxWidth: "76%",
    paddingHorizontal: 14,
    paddingVertical: 10,
    gap: 4,
  },
  text: {
    fontSize: 14,
    fontFamily: "Inter_400Regular",
    lineHeight: 20,
  },
  time: {
    fontSize: 10,
    fontFamily: "Inter_400Regular",
    alignSelf: "flex-end",
  },
});
