import { Request, Response } from 'express';
import { WeatherService } from '../services/weather.service';

export class WeatherController {
  static async getWeather(req: Request, res: Response) {
    try {
      const { lat, lng } = req.query;
      if (!lat || !lng) {
        return res.status(400).json({ error: 'Latitude and longitude required' });
      }

      const weather = await WeatherService.getWeather(parseFloat(lat as string), parseFloat(lng as string));
      res.json(weather);
    } catch (error) {
      console.error('Weather Controller Error:', error);
      res.status(500).json({ error: 'Failed to fetch weather' });
    }
  }
}
