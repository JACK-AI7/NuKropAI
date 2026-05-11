import { db } from "./firebase";
import { collection, addDoc, serverTimestamp } from "firebase/firestore";

export interface AuditLog {
  action: string;
  userId: string;
  role: string;
  resource: string;
  details: string;
  timestamp: any;
}

export async function logAuditAction(
  userId: string,
  role: string,
  action: string,
  resource: string,
  details: string
) {
  try {
    const log: AuditLog = {
      action,
      userId,
      role,
      resource,
      details,
      timestamp: serverTimestamp(),
    };
    
    // In a real enterprise app, this would go to a dedicated 'audit_logs' collection
    // with strict security rules (only readable by enterprise admins)
    console.log(`[AUDIT] User: ${userId} (${role}) | Action: ${action} | Resource: ${resource}`);
    
    // Attempt firestore log if db is available
    if (db) {
      await addDoc(collection(db, "audit_logs"), log);
    }
  } catch (err) {
    console.error("Audit log failed:", err);
  }
}

export const SecurityActions = {
  FARM_BOUNDARY_UPDATE: "FARM_BOUNDARY_UPDATE",
  DATA_EXPORT_PDF: "DATA_EXPORT_PDF",
  ROLE_CHANGE: "ROLE_CHANGE",
  COOPERATIVE_ACCESS: "COOPERATIVE_ACCESS",
  OUTBREAK_REPORT_VERIFY: "OUTBREAK_REPORT_VERIFY"
};
