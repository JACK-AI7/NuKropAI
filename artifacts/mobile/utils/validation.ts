export interface ValidationRecord {
  recordId: string;
  aiDiagnosis: string;
  expertDiagnosis: string;
  isCorrect: boolean;
  expertId: string;
  comments: string;
  timestamp: string;
}

export async function validateAIDiagnosis(
  recordId: string, 
  aiDiagnosis: string, 
  expertDiagnosis: string, 
  expertId: string,
  comments: string
): Promise<ValidationRecord> {
  const isCorrect = aiDiagnosis === expertDiagnosis;
  
  const record: ValidationRecord = {
    recordId,
    aiDiagnosis,
    expertDiagnosis,
    isCorrect,
    expertId,
    comments,
    timestamp: new Date().toISOString()
  };
  
  console.log(`[VALIDATION] Record ${recordId} validated by ${expertId}. Match: ${isCorrect}`);
  
  // In a real system, this updates the ML training dataset and triggers model evaluation
  return record;
}

export interface TreatmentApproval {
  recommendationId: string;
  status: "approved" | "rejected" | "modified";
  approverId: string;
  modifiedTreatment?: string;
  notes: string;
}

export async function approveTreatment(approval: TreatmentApproval) {
  console.log(`[APPROVAL] Treatment ${approval.recommendationId} ${approval.status} by ${approval.approverId}`);
  // Logic to notify farmer and log to audit trail
}
