import colors from "@/constants/colors";

/**
 * Returns the design tokens for the dark colour palette.
 * This app is dark-mode-only — Appearance.setColorScheme("dark") is called at
 * startup but React Native Web's useColorScheme() may still reflect the OS
 * preference. Hardcoding dark here keeps every surface consistent.
 */
export function useColors() {
  return { ...colors.dark, radius: colors.radius };
}
