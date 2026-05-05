import axios from 'axios';

const axiosInstance = axios.create({
  timeout: 10000,
  headers: {
    'User-Agent': 'NuKropAI/1.0',
  },
});

export class WeatherService {
  static async getWeather(lat: number, lon: number) {
    try {
      const response = await axiosInstance.get(
        `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m`,
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

      return {
        temp: current.temperature,
        windSpeed: current.windspeed,
        humidity,
        weatherCode: current.weathercode,
        time: current.time,
        unit: 'celsius'
      };
    } catch (error: any) {
      console.error('Weather Fetch Error:', error.message);
      throw new Error('Failed to fetch weather data: ' + (error.code || 'network error'));
    }
  }
}
