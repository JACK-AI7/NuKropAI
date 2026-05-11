export interface TreatmentProduct {
  name: string;
  type: "Fungicide" | "Insecticide" | "Herbicide" | "Organic" | "Nutrient";
  activeIngredient: string;
  dosage: string;
  timing: string;
  safety: string;
}

export interface DiseaseTreatment {
  disease: string;
  products: TreatmentProduct[];
  advice: string;
}

const TREATMENT_DATABASE: Record<string, DiseaseTreatment> = {
  "Early Blight (Alternaria solani)": {
    disease: "Early Blight",
    products: [
      {
        name: "Mancozeb 75% WP",
        type: "Fungicide",
        activeIngredient: "Mancozeb",
        dosage: "600-800g per acre",
        timing: "Spray at first sign of symptoms, repeat every 7-10 days",
        safety: "Wear protective clothing. Do not spray during high winds.",
      },
      {
        name: "Amistar Top",
        type: "Fungicide",
        activeIngredient: "Azoxystrobin + Difenoconazole",
        dosage: "200ml per acre",
        timing: "Preventive or early curative spray",
        safety: "Maintain 15-day gap before harvest.",
      },
      {
        name: "Neem Oil (Organic)",
        type: "Organic",
        activeIngredient: "Azadirachtin",
        dosage: "5ml per liter water",
        timing: "Evening spray for organic control",
        safety: "Non-toxic to bees after drying.",
      }
    ],
    advice: "Remove infected lower leaves and ensure proper plant spacing to reduce humidity."
  },
  "Late Blight (Phytophthora infestans)": {
    disease: "Late Blight",
    products: [
      {
        name: "Ridomil Gold",
        type: "Fungicide",
        activeIngredient: "Metalaxyl-M + Mancozeb",
        dosage: "500g per acre",
        timing: "Emergency curative spray during high humidity",
        safety: "Highly effective, use only when necessary to prevent resistance.",
      }
    ],
    advice: "Monitor weather; high humidity and cool nights favor rapid spread."
  },
  "Leaf Spot": {
    disease: "Leaf Spot",
    products: [
      {
        name: "Copper Oxychloride 50% WP",
        type: "Fungicide",
        activeIngredient: "Copper",
        dosage: "3g per liter water",
        timing: "Protective spray during rainy season",
        safety: "Wash hands thoroughly after use.",
      }
    ],
    advice: "Improve drainage and avoid overhead irrigation."
  }
};

export function getTreatmentsForDisease(diseaseName: string): DiseaseTreatment | null {
  // Try exact match or partial match
  const entry = TREATMENT_DATABASE[diseaseName];
  if (entry) return entry;

  // Partial match fallback
  for (const key in TREATMENT_DATABASE) {
    if (diseaseName.toLowerCase().includes(key.toLowerCase()) || key.toLowerCase().includes(diseaseName.toLowerCase())) {
      return TREATMENT_DATABASE[key];
    }
  }

  return null;
}
