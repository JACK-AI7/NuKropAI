import React, { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { 
  onAuthStateChanged, 
  signOut, 
  User,
  GoogleAuthProvider,
  signInWithCredential
} from "firebase/auth";
import { auth } from "@/utils/firebase";

interface AuthState {
  user: User | null;
  role: "farmer" | "advisor" | "enterprise" | "admin";
  isAdmin: boolean;
  loading: boolean;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [role, setRole] = useState<"farmer" | "advisor" | "enterprise" | "admin">("farmer");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
      setUser(firebaseUser);
      if (firebaseUser) {
        try {
          const { doc, getDoc } = await import("firebase/firestore");
          const { db } = await import("@/utils/firebase");
          const snap = await getDoc(doc(db, "users", firebaseUser.uid));
          if (snap.exists()) {
            const data = snap.data();
            setRole(data.role || "farmer");
          }
        } catch (e) {
          console.error("Role fetch error:", e);
        }
      } else {
        setRole("farmer");
      }
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  const logout = async () => {
    try {
      await signOut(auth);
    } catch (error) {
      console.error("Logout error:", error);
    }
  };

  return (
    <AuthContext.Provider value={{ user, role, isAdmin: role === "admin", loading, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
