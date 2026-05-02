import axios from 'axios';

export class WeatherService {
  static async getWeather(lat: number, lon: number) {
    try {
      const response = await axios.get(
        `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m`
      );
      
      const current = response.data.current_weather;
      const hourly = response.data.hourly;
      let humidity: number | null = null;
      if (hourly?.time && Array.isArray(hourly.time) && Array.isArray(hourly.relative_humidity_2m)) {
        const idx = hourly.time.indexOf(current.time);
        if (idx >= 0) {
          humidity = hourly.relative_humidity_2m[idx];
        }
      }

      return {
        temp: current.temperature,
        windSpeed: current.windspeed,
        humidity,
        weatherCode: current.weathercode, // WMO Weather interpretation codes
        time: current.time,
        unit: 'celsius'
      };
    } catch (error) {
      console.error('Weather Fetch Error:', error);
      throw new Error('Failed to fetch weather data');
    }
  }
}
