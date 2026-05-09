import React, { createContext, useContext, useState, useEffect, type ReactNode } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";

export type Language = "en" | "hi" | "te";

export interface ScanRecord {
  id: string;
  imageUri: string;
  disease: string;
  confidence: number;
  severity: "low" | "medium" | "high";
  timestamp: number;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: number;
}

export interface AIInsight {
  id: string;
  type: "warning" | "tip" | "danger" | "success";
  title: string;
  message: string;
  timestamp: number;
  crop?: string;
}

interface AppState {
  farmerName: string;
  farmLocation: string;
  language: Language;
  scanHistory: ScanRecord[];
  chatHistory: ChatMessage[];
  insights: AIInsight[];
  setFarmerName: (name: string) => void;
  setFarmLocation: (location: string) => void;
  setLanguage: (lang: Language) => void;
  addScanRecord: (record: ScanRecord) => void;
  addChatMessage: (msg: ChatMessage) => void;
  clearChatHistory: () => void;
}

const AppContext = createContext<AppState | null>(null);

const DEFAULT_INSIGHTS: AIInsight[] = [
  {
    id: "1",
    type: "warning",
    title: "Early Blight Risk",
    message: "High humidity detected. Check tomato and potato crops for early blight symptoms.",
    timestamp: Date.now() - 3600000,
    crop: "Tomato",
  },
  {
    id: "2",
    type: "tip",
    title: "Optimal Irrigation Window",
    message: "Early morning irrigation recommended. Soil moisture at 42% — within optimal range.",
    timestamp: Date.now() - 7200000,
    crop: "Wheat",
  },
  {
    id: "3",
    type: "danger",
    title: "Heavy Rain Alert",
    message: "Heavy rainfall expected in 48 hours. Harvest ready crops and treat drainage paths.",
    timestamp: Date.now() - 1800000,
  },
];

export function AppProvider({ children }: { children: ReactNode }) {
  const [farmerName, setFarmerNameState] = useState("Rajesh Kumar");
  const [farmLocation, setFarmLocationState] = useState("Telangana, India");
  const [language, setLanguageState] = useState<Language>("en");
  const [scanHistory, setScanHistory] = useState<ScanRecord[]>([]);
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [insights] = useState<AIInsight[]>(DEFAULT_INSIGHTS);

  useEffect(() => {
    const load = async () => {
      try {
        const saved = await AsyncStorage.getItem("nukropai_state");
        if (saved) {
          const state = JSON.parse(saved) as Partial<AppState & { scanHistory: ScanRecord[]; chatHistory: ChatMessage[] }>;
          if (state.farmerName) setFarmerNameState(state.farmerName);
          if (state.farmLocation) setFarmLocationState(state.farmLocation);
          if (state.language) setLanguageState(state.language);
          if (state.scanHistory) setScanHistory(state.scanHistory);
          if (state.chatHistory) setChatHistory(state.chatHistory);
        }
      } catch (_) {}
    };
    load();
  }, []);

  const saveState = async (updates: Record<string, unknown>) => {
    try {
      const current = await AsyncStorage.getItem("nukropai_state");
      const state = current ? (JSON.parse(current) as Record<string, unknown>) : {};
      await AsyncStorage.setItem("nukropai_state", JSON.stringify({ ...state, ...updates }));
    } catch (_) {}
  };

  const setFarmerName = (name: string) => {
    setFarmerNameState(name);
    saveState({ farmerName: name });
  };

  const setFarmLocation = (location: string) => {
    setFarmLocationState(location);
    saveState({ farmLocation: location });
  };

  const setLanguage = (lang: Language) => {
    setLanguageState(lang);
    saveState({ language: lang });
  };

  const addScanRecord = (record: ScanRecord) => {
    setScanHistory((prev) => {
      const next = [record, ...prev].slice(0, 50);
      saveState({ scanHistory: next });
      return next;
    });
  };

  const addChatMessage = (msg: ChatMessage) => {
    setChatHistory((prev) => {
      const next = [...prev, msg].slice(-100);
      saveState({ chatHistory: next });
      return next;
    });
  };

  const clearChatHistory = () => {
    setChatHistory([]);
    saveState({ chatHistory: [] });
  };

  return (
    <AppContext.Provider
      value={{
        farmerName,
        farmLocation,
        language,
        scanHistory,
        chatHistory,
        insights,
        setFarmerName,
        setFarmLocation,
        setLanguage,
        addScanRecord,
        addChatMessage,
        clearChatHistory,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useApp must be used within AppProvider");
  return ctx;
}
