"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.WeatherController = void 0;
const weather_service_1 = require("../services/weather.service");
class WeatherController {
    static async getWeather(req, res) {
        try {
            const { lat, lng } = req.query;
            if (!lat || !lng) {
                return res.status(400).json({ error: 'Latitude and longitude required' });
            }
            const weather = await weather_service_1.WeatherService.getWeather(parseFloat(lat), parseFloat(lng));
            res.json(weather);
        }
        catch (error) {
            console.error('Weather Controller Error:', error);
            res.status(500).json({ error: 'Failed to fetch weather' });
        }
    }
}
exports.WeatherController = WeatherController;
