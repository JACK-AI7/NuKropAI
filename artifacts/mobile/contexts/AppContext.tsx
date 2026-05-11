import React, { createContext, useContext, useState, useEffect, useCallback, useRef, type ReactNode } from "react";
import { AppState, type AppStateStatus } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { doc, getDoc, setDoc, onSnapshot } from "firebase/firestore";
import { db } from "@/utils/firebase";
import { useAuth } from "./AuthContext";
import { logAuditAction, SecurityActions } from "@/utils/security";

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

export interface Farm {
  id: string;
  name: string;
  location: string;
  lat: number;
  lon: number;
  area: number;
  crops: string[];
  boundaries: { lat: number; lon: number }[];
  soilHealth: {
    npk: { n: number; p: number; k: number };
    ph: number;
    moisture: number;
  };
  ndvi: {
    score: number; // 0-1
    trend: "up" | "down" | "stable";
    lastUpdated: string;
  };
}

interface GlobalState {
  farmerName: string;
  locationCity: string;
  farms: Farm[];
  activeFarmId: string;
  userRole: "farmer" | "advisor" | "enterprise";
  advisorStats?: {
    assignedFarms: number;
    activeOutbreaks: number;
    pendingRecommendations: number;
  };
  groups: {
    id: string;
    name: string;
    memberCount: number;
    description: string;
    district: string;
    alerts: AIInsight[];
  }[];
  language: Language;
  scanHistory: ScanRecord[];
  chatHistory: ChatMessage[];
  insights: AIInsight[];
  notificationPrefs: {
    weather: boolean;
    disease: boolean;
    market: boolean;
    reminders: boolean;
  };
  hasSeenOnboarding: boolean;
  setFarmerName: (name: string) => void;
  setLanguage: (lang: Language) => void;
  setHasSeenOnboarding: (val: boolean) => void;
  updateNotificationPrefs: (prefs: Partial<GlobalState["notificationPrefs"]>) => void;
  addScanRecord: (record: ScanRecord) => void;
  addChatMessage: (msg: ChatMessage) => void;
  clearChatHistory: () => void;
  setLocation: (lat: number, lon: number, city: string) => void;
  addFarm: (farm: Farm) => void;
  setActiveFarmId: (id: string) => void;
  setUserRole: (role: "farmer" | "advisor" | "enterprise") => void;
}

const AppContext = createContext<GlobalState | null>(null);

const DEFAULT_FARM: Farm = {
  id: "f1",
  name: "Main Farm",
  location: "Hyderabad, Telangana",
  lat: 17.385,
  lon: 78.486,
  area: 2.5,
  crops: ["Rice", "Cotton"],
  boundaries: [
    { lat: 17.385, lon: 78.486 },
    { lat: 17.386, lon: 78.486 },
    { lat: 17.386, lon: 78.487 },
    { lat: 17.385, lon: 78.487 },
  ],
  soilHealth: {
    npk: { n: 45, p: 32, k: 40 },
    ph: 6.8,
    moisture: 65
  },
  ndvi: {
    score: 0.72,
    trend: "up",
    lastUpdated: new Date().toISOString()
  }
};

export function AppProvider({ children }: { children: ReactNode }) {
  const { user } = useAuth();
  const [farmerName, setFarmerNameState] = useState("Rajesh Kumar");
  const [language, setLanguageState] = useState<Language>("en");
  const [hasSeenOnboarding, setHasSeenOnboardingState] = useState(false);
  const [farms, setFarmsState] = useState<Farm[]>([DEFAULT_FARM]);
  const [activeFarmId, setActiveFarmIdState] = useState("f1");
  const [userRole, setUserRoleState] = useState<GlobalState["userRole"]>("farmer");
  const [advisorStats, setAdvisorStats] = useState<GlobalState["advisorStats"]>({
    assignedFarms: 124,
    activeOutbreaks: 3,
    pendingRecommendations: 8
  });
  const [groups, setGroupsState] = useState<GlobalState["groups"]>([]);
  const [notificationPrefs, setNotificationPrefsState] = useState({
    weather: true,
    disease: true,
    market: true,
    reminders: true,
  });
  const [scanHistory, setScanHistory] = useState<ScanRecord[]>([]);
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [insights, setInsights] = useState<AIInsight[]>([]);
  const [locationCity, setLocationCityState] = useState("Hyderabad");

  const isCloudSyncing = useRef(false);

  const activeFarm = farms.find(f => f.id === activeFarmId) || farms[0];

  useEffect(() => {
    const load = async () => {
      try {
        const saved = await AsyncStorage.getItem("nukropai_state_v3");
        if (saved) {
          const state = JSON.parse(saved);
          if (state.farmerName) setFarmerNameState(state.farmerName);
          if (state.farms) setFarmsState(state.farms);
          if (state.activeFarmId) setActiveFarmIdState(state.activeFarmId);
          if (state.language) setLanguageState(state.language);
          if (state.userRole) setUserRoleState(state.userRole);
          if (state.notificationPrefs) setNotificationPrefsState(state.notificationPrefs);
          if (state.scanHistory) setScanHistory(state.scanHistory);
          if (state.chatHistory) setChatHistory(state.chatHistory);
          if (state.insights) setInsights(state.insights);
          if (state.hasSeenOnboarding !== undefined) setHasSeenOnboardingState(state.hasSeenOnboarding);
        }
      } catch (_) {}
    };
    load();
  }, []);

  useEffect(() => {
    if (!user) return;
    const userDocRef = doc(db, "users", user.uid);
    const syncInitial = async () => {
      try {
        const snap = await getDoc(userDocRef);
        if (snap.exists()) {
          const data = snap.data();
          if (data.farmerName) setFarmerNameState(data.farmerName);
          if (data.farms) setFarmsState(data.farms);
          if (data.activeFarmId) setActiveFarmIdState(data.activeFarmId);
          if (data.language) setLanguageState(data.language);
          if (data.userRole) setUserRoleState(data.userRole);
          if (data.notificationPrefs) setNotificationPrefsState(data.notificationPrefs);
          if (data.scanHistory) setScanHistory(data.scanHistory);
          if (data.chatHistory) setChatHistory(data.chatHistory);
          if (state.insights) setInsights(state.insights);
          if (data.hasSeenOnboarding !== undefined) setHasSeenOnboardingState(data.hasSeenOnboarding);
        }
      } catch (err) { console.error("Sync error:", err); }
    };
    syncInitial();
    const unsub = onSnapshot(userDocRef, (snap) => {
      if (snap.exists() && !isCloudSyncing.current) {
        const data = snap.data();
        setFarmerNameState(data.farmerName || farmerName);
        setFarmsState(data.farms || farms);
        setActiveFarmIdState(data.activeFarmId || activeFarmId);
        setLanguageState(data.language || language);
        setUserRoleState(data.userRole || userRole);
        setNotificationPrefsState(data.notificationPrefs || notificationPrefs);
        setScanHistory(data.scanHistory || scanHistory);
        setChatHistory(data.chatHistory || chatHistory);
        setInsights(data.insights || insights);
      }
    });
    return () => unsub();
  }, [user]);

  const syncTimer = useRef<NodeJS.Timeout | null>(null);

  const saveState = useCallback(async () => {
    if (syncTimer.current) clearTimeout(syncTimer.current);
    
    syncTimer.current = setTimeout(async () => {
      try {
        const stateToSave = {
          farmerName,
          farms,
          activeFarmId,
          language,
          userRole,
          notificationPrefs,
          scanHistory,
          chatHistory,
          insights,
          hasSeenOnboarding,
          lastUserId: user?.uid,
          updatedAt: Date.now()
        };
        
        await AsyncStorage.setItem("nukropai_state_v3", JSON.stringify(stateToSave));
        
        // Only sync to cloud if app is active and user is logged in
        if (user && !isCloudSyncing.current && AppState.currentState === "active") {
          isCloudSyncing.current = true;
          const userDocRef = doc(db, "users", user.uid);
          await setDoc(userDocRef, stateToSave, { merge: true });
          setTimeout(() => { isCloudSyncing.current = false; }, 1000);
        }
      } catch (err) {
        console.error("[AppContext] Local/Cloud sync failed:", err);
        isCloudSyncing.current = false;
      }
    }, 2500); // 2.5s throttle
  }, [farmerName, farms, activeFarmId, language, userRole, notificationPrefs, scanHistory, chatHistory, insights, user]);

  useEffect(() => {
    saveState();
    return () => {
      if (syncTimer.current) clearTimeout(syncTimer.current);
    };
  }, [saveState]);

  const setFarmerName = (name: string) => setFarmerNameState(name);
  const setLanguage = (lang: Language) => {
    setLanguageState(lang);
    saveState();
  };
  const setHasSeenOnboarding = (val: boolean) => {
    setHasSeenOnboardingState(val);
    saveState();
  };
  const updateNotificationPrefs = (prefs: Partial<GlobalState["notificationPrefs"]>) => setNotificationPrefsState(p => ({ ...p, ...prefs }));
  const addScanRecord = (record: ScanRecord) => setScanHistory(p => [record, ...p].slice(0, 50));
  const addChatMessage = (msg: ChatMessage) => setChatHistory(p => [...p, msg].slice(-100));
  const clearChatHistory = () => setChatHistory([]);
  const setLocation = (lat: number, lon: number, city: string) => setLocationCityState(city);
  const addFarm = (farm: Farm) => setFarmsState(p => [...p, farm]);
  const setActiveFarmId = (id: string) => setActiveFarmIdState(id);

  return (
    <AppContext.Provider
      value={{
        farmerName,
        locationCity,
        farms,
        activeFarmId,
        userRole,
        advisorStats,
        groups,
        language,
        scanHistory,
        chatHistory,
        insights,
        notificationPrefs,
        hasSeenOnboarding,
        setFarmerName,
        setLanguage,
        setHasSeenOnboarding,
        updateNotificationPrefs,
        addScanRecord,
        addChatMessage,
        clearChatHistory,
        setLocation,
        addFarm,
        setActiveFarmId,
        setUserRole: (role: "farmer" | "advisor" | "enterprise") => {
          if (user) {
            logAuditAction(user.uid, userRole, SecurityActions.ROLE_CHANGE, "user_account", `Role changed to ${role}`);
          }
          setUserRoleState(role);
        }
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
