import axios from 'axios';
import { redisClient } from '../config/db';

export class MandiSyncService {
    private readonly API_KEYS = [
        "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b",
        "579b464db66ec23bdd0000011c7fae98f0294e7769efce5b804245cc",
        "579b464db66ec23bdd000001f6e0ad50e20d4fbb6c5a17de5e50abcc"
    ];
    private keyIndex = 0;
    private readonly BASE_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070";

    /**
     * Fetches Mandi Rates from Redis (Instant). If missing, queries Gov API and caches.
     */
    async getMandiRates(state: string, commodity: string): Promise<any[]> {
        const cacheKey = `mandi_rates:${state.toLowerCase()}:${commodity.toLowerCase()}`;
        
        // 1. Check Redis Cache
        const cachedData = await redisClient.get(cacheKey);
        if (cachedData) {
            console.log(`[MandiSyncService] ⚡ CACHE HIT: Served ${state}-${commodity} instantly from Redis.`);
            return JSON.parse(cachedData);
        }

        console.log(`[MandiSyncService] 🐌 CACHE MISS: Fetching ${state}-${commodity} from Gov API...`);

        // 2. Fetch from Government API
        let attempt = 0;
        let lastError = "";

        while (attempt < this.API_KEYS.length) {
            const apiKey = this.API_KEYS[(this.keyIndex + attempt) % this.API_KEYS.length];
            
            try {
                const response = await axios.get(this.BASE_URL, {
                    params: {
                        'api-key': apiKey,
                        'format': 'json',
                        'limit': 50, // Only fetch 50 for speed
                        'filters[state]': state,
                        'filters[commodity]': commodity
                    },
                    timeout: 10000
                });

                if (response.data && response.data.records) {
                    const parsedRecords = response.data.records.map((r: any) => ({
                        state: r.state || "",
                        district: r.district || "",
                        market: r.market || "",
                        commodity: r.commodity || "",
                        variety: r.variety || "",
                        minPrice: r.min_price ? parseFloat(r.min_price) : parseFloat(r.modal_price || "0"),
                        maxPrice: r.max_price ? parseFloat(r.max_price) : parseFloat(r.modal_price || "0"),
                        modalPrice: parseFloat(r.modal_price || "0"),
                        arrivalDate: r.arrival_date || ""
                    }));

                    // 3. Save to Redis with a 15-minute expiration
                    await redisClient.set(cacheKey, JSON.stringify(parsedRecords), {
                        EX: 900 // 15 mins
                    });

                    // Update rolling key index on success
                    this.keyIndex = (this.keyIndex + attempt) % this.API_KEYS.length;
                    return parsedRecords;
                }

            } catch (error: any) {
                lastError = error.message;
                if (error.response?.status === 429) {
                    // Rate limit hit on this key, advance key index
                    this.keyIndex = (this.keyIndex + 1) % this.API_KEYS.length;
                }
                attempt++;
            }
        }

        throw new Error(`Failed to fetch Mandi rates after trying all keys. Last error: ${lastError}`);
    }
}

export const mandiSyncService = new MandiSyncService();
