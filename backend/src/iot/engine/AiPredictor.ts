/**
 * AI Evapotranspiration and Water Requirement Predictor
 */
export class AiPredictor {
    /**
     * Calculates the estimated duration to run the pump based on soil moisture and ETc
     */
    static calculateIrrigationDuration(currentMoisture: number, cropType: string, temperature: number): number {
        // Extremely simplified ETc (Crop Evapotranspiration) model
        let targetMoisture = 60; // Usually field capacity
        if (cropType === 'cotton') targetMoisture = 55;
        if (cropType === 'rice') targetMoisture = 80;

        const deficit = targetMoisture - currentMoisture;
        if (deficit <= 0) return 0; // No irrigation needed

        // Assume a standard 5 HP pump outputs 500 liters/min.
        // Assume 1% moisture increase requires 50 liters for a standard 1 acre plot.
        const requiredLiters = deficit * 50; 

        // Adjust for temperature (higher temp = more evaporation during spray)
        const evaporationFactor = temperature > 35 ? 1.2 : 1.0;
        
        const totalLiters = requiredLiters * evaporationFactor;
        const durationMinutes = totalLiters / 500;

        console.log(`[AiPredictor] Crop=${cropType}, Moisture=${currentMoisture}%. Required Liters=${totalLiters}. Pumping Time=${durationMinutes.toFixed(1)} mins`);
        
        return Math.ceil(durationMinutes);
    }
}
