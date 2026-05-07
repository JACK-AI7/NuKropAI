import axios from 'axios';

const axiosInstance = axios.create({
  timeout: 10000,
  headers: {
    'User-Agent': 'NuKropAI/1.0',
  },
});

interface CachedWeather {
  timestamp: number;
  data: any;
}

const weatherCache = new Map<string, CachedWeather>();
const CACHE_DURATION_MS = 30 * 60 * 1000; // 30 minutes

export class WeatherService {
  static async getWeather(lat: number, lon: number) {
    try {
      // Create a grid key: ~11km resolution by rounding to 1 decimal place
      const gridKey = `${lat.toFixed(1)}_${lon.toFixed(1)}`;
      const cached = weatherCache.get(gridKey);
      
      if (cached && Date.now() - cached.timestamp < CACHE_DURATION_MS) {
        return cached.data;
      }

      const response = await axiosInstance.get(
        `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m&daily=temperature_2m_max,precipitation_probability_max&timezone=auto`,
        { timeout: 10000 }
      );
      
      const current = response.data.current_weather;
      const hourly = response.data.hourly;
      let humidity: number | null = null;
      if (hourly?.time && Array.isArray(hourly.time) && Array.isArray(hourly.relative_humidity_2m)) {
        let idx = hourly.time.indexOf(current.time);
        if (idx < 0) idx = hourly.relative_humidity_2m.length - 1;
        if (idx >= 0) {
          humidity = hourly.relative_humidity_2m[idx];
        }
      }

      let smartAlert = null;
      const daily = response.data.daily;
      if (daily) {
        const maxTemp = daily.temperature_2m_max?.[0];
        const rainProb = daily.precipitation_probability_max?.[0];
        
        if (rainProb !== undefined && rainProb > 60) {
          smartAlert = `High rain chance (${rainProb}%). Delay foliar sprays or fertilizer application.`;
        } else if (maxTemp !== undefined && maxTemp > 35) {
          smartAlert = `Extreme heat expected (${maxTemp}°C). Ensure adequate irrigation and avoid midday pesticide application.`;
        } else if (maxTemp !== undefined && maxTemp < 10) {
          smartAlert = `Cold stress risk. Monitor sensitive crops.`;
        } else {
          smartAlert = `Optimal farming weather. Good time for scheduled field activities.`;
        }
      }

      const weatherData = {
        temp: current.temperature,
        windSpeed: current.windspeed,
        humidity,
        weatherCode: current.weathercode,
        time: current.time,
        unit: 'celsius',
        smartAlert
      };

      // Save to cache
      weatherCache.set(gridKey, { timestamp: Date.now(), data: weatherData });

      return weatherData;
    } catch (error: any) {
      console.error('Weather Fetch Error:', error.message);
      throw new Error('Failed to fetch weather data: ' + (error.code || 'network error'));
    }
  }
}
