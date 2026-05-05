"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.WeatherService = void 0;
const axios_1 = __importDefault(require("axios"));
const axiosInstance = axios_1.default.create({
    timeout: 10000,
    headers: {
        'User-Agent': 'NuKropAI/1.0',
    },
});
class WeatherService {
    static async getWeather(lat, lon) {
        try {
            const response = await axiosInstance.get(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m`, { timeout: 10000 });
            const current = response.data.current_weather;
            const hourly = response.data.hourly;
            let humidity = null;
            if (hourly?.time && Array.isArray(hourly.time) && Array.isArray(hourly.relative_humidity_2m)) {
                let idx = hourly.time.indexOf(current.time);
                if (idx < 0)
                    idx = hourly.relative_humidity_2m.length - 1;
                if (idx >= 0) {
                    humidity = hourly.relative_humidity_2m[idx];
                }
            }
            return {
                temp: current.temperature,
                windSpeed: current.windspeed,
                humidity,
                weatherCode: current.weathercode,
                time: current.time,
                unit: 'celsius'
            };
        }
        catch (error) {
            console.error('Weather Fetch Error:', error.message);
            throw new Error('Failed to fetch weather data: ' + (error.code || 'network error'));
        }
    }
}
exports.WeatherService = WeatherService;
