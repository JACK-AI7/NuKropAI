import React, { createContext, useContext, useState, useEffect, useCallback, useRef, type ReactNode } from "react";
import { AppState, type AppStateStatus } from "react-native";
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

interface GlobalState {
  farmerName: string;
  farmLocation: string;
  language: Language;
  scanHistory: ScanRecord[];
  chatHistory: ChatMessage[];
  insights: AIInsight[];
  // Location (GPS or default Hyderabad)
  lat: number;
  lon: number;
  locationCity: string;
  setFarmerName: (name: string) => void;
  setFarmLocation: (location: string) => void;
  setLanguage: (lang: Language) => void;
  addScanRecord: (record: ScanRecord) => void;
  addChatMessage: (msg: ChatMessage) => void;
  clearChatHistory: () => void;
  setLocation: (lat: number, lon: number, city: string) => void;
}

const AppContext = createContext<GlobalState | null>(null);

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

// Default to Hyderabad, Telangana (central farming region in south India)
const DEFAULT_LAT = 17.385;
const DEFAULT_LON = 78.486;
const DEFAULT_CITY = "Hyderabad";

export function AppProvider({ children }: { children: ReactNode }) {
  const [farmerName, setFarmerNameState] = useState("Rajesh Kumar");
  const [farmLocation, setFarmLocationState] = useState("Telangana, India");
  const [language, setLanguageState] = useState<Language>("en");
  const [scanHistory, setScanHistory] = useState<ScanRecord[]>([]);
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [insights] = useState<AIInsight[]>(DEFAULT_INSIGHTS);
  const [lat, setLatState] = useState(DEFAULT_LAT);
  const [lon, setLonState] = useState(DEFAULT_LON);
  const [locationCity, setLocationCityState] = useState(DEFAULT_CITY);

  useEffect(() => {
    const load = async () => {
      try {
        const saved = await AsyncStorage.getItem("nukropai_state");
        if (saved) {
          const state = JSON.parse(saved) as Partial<
            GlobalState & { scanHistory: ScanRecord[]; chatHistory: ChatMessage[] }
          >;
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

  // Persist state when relevant fields change (debounced)
  const saveState = useCallback(async () => {
    try {
      const stateToSave = {
        farmerName,
        farmLocation,
        language,
        scanHistory,
        chatHistory,
      };
      await AsyncStorage.setItem("nukropai_state", JSON.stringify(stateToSave));
    } catch (_) {}
  }, [farmerName, farmLocation, language, scanHistory, chatHistory]);

  useEffect(() => {
    const timer = setTimeout(saveState, 1000);
    return () => clearTimeout(timer);
  }, [saveState]);

  // Also save when app goes to background
  useEffect(() => {
    const sub = AppState.addEventListener("change", (next: AppStateStatus) => {
      if (next !== "active") {
        saveState();
      }
    });
    return () => sub.remove();
  }, [saveState]);

  const setFarmerName = (name: string) => {
    setFarmerNameState(name);
  };

  const setFarmLocation = (location: string) => {
    setFarmLocationState(location);
  };

  const setLanguage = (lang: Language) => {
    setLanguageState(lang);
  };

  const addScanRecord = (record: ScanRecord) => {
    setScanHistory((prev) => [record, ...prev].slice(0, 50));
  };

  const addChatMessage = (msg: ChatMessage) => {
    setChatHistory((prev) => [...prev, msg].slice(-100));
  };

  const clearChatHistory = () => {
    setChatHistory([]);
  };

  const setLocation = useCallback((newLat: number, newLon: number, city: string) => {
    setLatState(newLat);
    setLonState(newLon);
    setLocationCityState(city);
  }, []);

  return (
    <AppContext.Provider
      value={{
        farmerName,
        farmLocation,
        language,
        scanHistory,
        chatHistory,
        insights,
        lat,
        lon,
        locationCity,
        setFarmerName,
        setFarmLocation,
        setLanguage,
        addScanRecord,
        addChatMessage,
        clearChatHistory,
        setLocation,
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
