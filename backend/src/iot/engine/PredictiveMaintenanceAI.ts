/**
 * Predictive Maintenance SRE Module
 * Analyzes historical telemetry arrays to detect bearing wear or impeller blockages.
 */
export class PredictiveMaintenanceAI {
    
    /**
     * Calculates moving averages over a 30-day time series to detect abnormal current creep.
     * @param historicalAmperage Array of daily average amperages over the last 30 days
     * @returns True if a warning should be issued to the farmer
     */
    static analyzeBearingWear(historicalAmperage: number[]): { hasWarning: boolean, message: string } {
        if (historicalAmperage.length < 10) {
            return { hasWarning: false, message: 'Insufficient data' };
        }

        // Simple Linear Regression slope detection for "Amperage Creep"
        const n = historicalAmperage.length;
        let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;
        
        for (let i = 0; i < n; i++) {
            sumX += i;
            sumY += historicalAmperage[i];
            sumXY += (i * historicalAmperage[i]);
            sumX2 += (i * i);
        }

        const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
        
        // If current is climbing by more than 0.05A per day on average, bearings might be failing
        if (slope > 0.05) {
            return {
                hasWarning: true,
                message: `PREDICTIVE WARNING: Amperage draw has steadily increased by ${(slope * 30).toFixed(2)}A this month. Schedule bearing inspection.`
            };
        }

        return { hasWarning: false, message: 'Motor health optimal' };
    }
}
