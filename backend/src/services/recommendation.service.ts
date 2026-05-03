import fs from 'fs';
import path from 'path';

function normalizeKey(s: string): string {
  return s
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '')
    .trim();
}

export class RecommendationService {
  private static cachedData: any = null;

  private static getData() {
    if (this.cachedData) return this.cachedData;
    try {
      const filePath = path.join(process.cwd(), 'data', 'crops.json');
      this.cachedData = JSON.parse(fs.readFileSync(filePath, 'utf8'));
      return this.cachedData;
    } catch (e) {
      console.error('Error reading crops data:', e);
      return { crops: {}, soil: {} };
    }
  }

  static getRecommendation(label: string, lat?: number, lng?: number, weather?: any) {
    const data = this.getData();
    let recommendation: any = null;

    // Try to find in crops database
    for (const cropKey in data.crops) {
      const diseases = data.crops[cropKey].diseases;
      if (diseases[label]) {
        recommendation = { ...diseases[label] };
        break;
      }
    }

    if (!recommendation) {
      throw new Error(`No recommendation data found for label: ${label}`);
    }

    // Weather-aware intelligence (only when values exist)
    if (weather) {
      const hum = weather.humidity;
      if (hum != null && Number(hum) > 80) {
        recommendation.treatment += " | ⚠️ HIGH FUNGAL RISK: Avoid overhead irrigation. Apply fungicide preventively.";
      }
      const temp = weather.temp;
      if (temp != null && Number(temp) > 35) {
        recommendation.treatment += " | 🌡️ HEAT STRESS: Increase irrigation frequency. Apply anti-transpirant if available.";
      }
      if (temp != null && Number(temp) < 15) {
        recommendation.treatment += " | ❄️ LOW TEMP: Delay fertilizer application. Use light irrigation.";
      }
    }

    return recommendation;
  }

  /** Match AI plant + disease text to a crops.json disease key (e.g. Rice_Blast). */
  static findMatchingDiseaseKey(plantName: string, diseaseName: string): string | null {
    const data = this.getData();
    const pNorm = normalizeKey(plantName || '');
    const dNorm = normalizeKey(diseaseName || '');
    if (!dNorm) return null;

    const tryCrop = (cropKey: string): string | null => {
      const crop = data.crops[cropKey];
      if (!crop?.diseases) return null;
      for (const diseaseKey of Object.keys(crop.diseases)) {
        const entry = crop.diseases[diseaseKey];
        const nameNorm = normalizeKey(entry?.name || '');
        const keyNorm = normalizeKey(diseaseKey.replace(/_/g, ' '));
        if (
          (dNorm && nameNorm && (nameNorm.includes(dNorm) || dNorm.includes(nameNorm))) ||
          (dNorm && keyNorm && (keyNorm.includes(dNorm) || dNorm.includes(keyNorm)))
        ) {
          return diseaseKey;
        }
      }
      return null;
    };

    if (pNorm) {
      for (const cropKey of Object.keys(data.crops)) {
        const crop = data.crops[cropKey];
        const cropNameNorm = normalizeKey(crop?.name || cropKey);
        if (cropNameNorm.includes(pNorm) || pNorm.includes(cropNameNorm)) {
          const hit = tryCrop(cropKey);
          if (hit) return hit;
        }
      }
    }

    for (const cropKey of Object.keys(data.crops)) {
      const hit = tryCrop(cropKey);
      if (hit) return hit;
    }

    return null;
  }

  static getSoilInsights(type: string, lat?: number, lng?: number) {
    const data = this.getData();
    let insights = data.soil[type];

    if (!insights) {
      throw new Error(`No soil insight data found for type: ${type}`);
    }

    insights = { ...insights };

    return insights;
  }
}
