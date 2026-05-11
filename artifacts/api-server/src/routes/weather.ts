import type { Request, Response } from "express";
import { Router } from "express";

const weatherRouter = Router();

const WEATHER_CODES: Record<number, { condition: string; icon: string }> = {
  0: { condition: "Clear Sky", icon: "sunny" },
  1: { condition: "Mainly Clear", icon: "partly-sunny" },
  2: { condition: "Partly Cloudy", icon: "partly-sunny" },
  3: { condition: "Overcast", icon: "cloudy" },
  45: { condition: "Foggy", icon: "cloud" },
  48: { condition: "Icy Fog", icon: "cloud" },
  51: { condition: "Light Drizzle", icon: "rainy" },
  53: { condition: "Drizzle", icon: "rainy" },
  55: { condition: "Heavy Drizzle", icon: "rainy" },
  61: { condition: "Light Rain", icon: "rainy" },
  63: { condition: "Moderate Rain", icon: "rainy" },
  65: { condition: "Heavy Rain", icon: "thunderstorm" },
  71: { condition: "Light Snow", icon: "snow" },
  73: { condition: "Snow", icon: "snow" },
  75: { condition: "Heavy Snow", icon: "snow" },
  77: { condition: "Snow Grains", icon: "snow" },
  80: { condition: "Rain Showers", icon: "rainy" },
  81: { condition: "Rain Showers", icon: "rainy" },
  82: { condition: "Heavy Showers", icon: "thunderstorm" },
  85: { condition: "Snow Showers", icon: "snow" },
  86: { condition: "Heavy Snow Showers", icon: "snow" },
  95: { condition: "Thunderstorm", icon: "thunderstorm" },
  96: { condition: "Thunderstorm + Hail", icon: "thunderstorm" },
  99: { condition: "Thunderstorm + Hail", icon: "thunderstorm" },
};

function codeToInfo(code: number): { condition: string; icon: string } {
  const exact = WEATHER_CODES[code];
  if (exact) return exact;
  if (code >= 71 && code <= 77) return { condition: "Snow", icon: "snow" };
  if (code >= 80 && code <= 82) return { condition: "Rain Showers", icon: "rainy" };
  return { condition: "Cloudy", icon: "partly-sunny" };
}

function buildFarmingTip(
  code: number,
  humidity: number,
  uv: number,
  windSpeed: number,
  temp: number,
  rainPct: number,
): string {
  if (code === 95 || code === 96 || code === 99)
    return "Thunderstorm conditions. Stay indoors, secure farm equipment, and inspect crops after the storm passes.";
  if (rainPct > 75)
    return "Heavy rain expected. Harvest ready crops immediately, clear drainage channels, and avoid pesticide/fertilizer application today.";
  if (rainPct > 45)
    return `Moderate rain likely (${rainPct}% chance). Delay spraying and irrigation. Check bund integrity in paddy fields.`;
  if (humidity > 82)
    return `High humidity (${humidity}%) — prime conditions for fungal diseases. Inspect tomato/potato/chilli crops for blight and mildew. Apply preventive fungicide.`;
  if (uv > 9)
    return "Extreme UV. Avoid field work between 11 AM – 3 PM. Irrigate at dawn only. Use UV-protective cover for sensitive seedlings.";
  if (uv > 7)
    return "High UV index. Apply pesticides early morning before 9 AM or after 5 PM to prevent photo-degradation and leaf burn.";
  if (windSpeed > 28)
    return `Strong winds (${windSpeed} km/h). Postpone all spray operations — chemical drift will reduce efficacy and may harm neighbouring crops.`;
  if (temp > 40)
    return `Extreme heat (${temp}°C). Increase irrigation to twice daily, mulch soil to retain moisture, and provide shade netting for nurseries.`;
  if (temp > 36)
    return `High temperature (${temp}°C). Irrigate early morning, monitor for heat stress and wilting in cotton and chilli crops.`;
  if (code === 0 || code === 1)
    return "Clear, sunny conditions — excellent window for harvesting, pesticide spraying, and soil preparation work.";
  if (rainPct < 15 && humidity < 45 && temp > 28)
    return "Dry conditions. Monitor soil moisture closely — schedule irrigation if the field has not been watered in the last 2 days.";
  return "Moderate conditions. Good day for crop monitoring, weeding, fertilizer application, and routine farm maintenance.";
}

interface OpenMeteoResponse {
  current: {
    temperature_2m: number;
    relative_humidity_2m: number;
    apparent_temperature: number;
    weather_code: number;
    wind_speed_10m: number;
    uv_index: number;
    precipitation: number;
    cloud_cover: number;
    surface_pressure: number;
  };
  daily: {
    time: string[];
    weather_code: number[];
    temperature_2m_max: number[];
    temperature_2m_min: number[];
    sunrise: string[];
    sunset: string[];
    uv_index_max: number[];
    precipitation_sum: number[];
    wind_speed_10m_max: number[];
    precipitation_probability_max: number[];
  };
  hourly: {
    time: string[];
    temperature_2m: number[];
    precipitation_probability: number[];
    weather_code: number[];
    wind_speed_10m: number[];
  };
}

weatherRouter.get("/weather", async (req: Request, res: Response) => {
  const { lat, lon } = req.query as { lat?: string; lon?: string };

  const latitude = parseFloat(lat ?? "17.385");
  const longitude = parseFloat(lon ?? "78.486");

  if (isNaN(latitude) || isNaN(longitude)) {
    res.status(400).json({ error: "Invalid coordinates" });
    return;
  }

  const params = new URLSearchParams({
    latitude: latitude.toFixed(4),
    longitude: longitude.toFixed(4),
    current:
      "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,uv_index,precipitation,cloud_cover,surface_pressure",
    daily:
      "weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_sum,wind_speed_10m_max,precipitation_probability_max",
    hourly: "temperature_2m,precipitation_probability,weather_code,wind_speed_10m",
    timezone: "auto",
    forecast_days: "7",
    wind_speed_unit: "kmh",
  });

  try {
    const weatherRes = await fetch(`https://api.open-meteo.com/v1/forecast?${params.toString()}`, {
      signal: AbortSignal.timeout(8000),
    });

    if (!weatherRes.ok) throw new Error(`Open-Meteo ${weatherRes.status}`);

    const data = (await weatherRes.json()) as OpenMeteoResponse;
    const c = data.current;
    const d = data.daily;
    const h = data.hourly;

    const code = c.weather_code;
    const info = codeToInfo(code);
    const humidity = c.relative_humidity_2m;
    const uv = parseFloat((c.uv_index ?? 0).toFixed(1));
    const windSpeed = Math.round(c.wind_speed_10m);
    const temp = Math.round(c.temperature_2m);
    const rainPct = d.precipitation_probability_max[0] ?? 0;

    const forecast = d.time.map((date, i) => ({
      date,
      maxTemp: Math.round(d.temperature_2m_max[i] ?? 0),
      minTemp: Math.round(d.temperature_2m_min[i] ?? 0),
      condition: codeToInfo(d.weather_code[i] ?? 0).condition,
      icon: codeToInfo(d.weather_code[i] ?? 0).icon,
      precipitationMm: parseFloat((d.precipitation_sum[i] ?? 0).toFixed(1)),
      precipitationPct: d.precipitation_probability_max[i] ?? 0,
      uvMax: parseFloat((d.uv_index_max[i] ?? 0).toFixed(1)),
    }));

    const nowHour = new Date().getHours();
    const hourly = h.time.slice(nowHour, nowHour + 8).map((t, i) => {
      const idx = nowHour + i;
      const d = new Date(t);
      const label = i === 0 ? "Now" : d.toLocaleTimeString("en-IN", { hour: "numeric", hour12: true });
      return {
        time: label,
        temp: Math.round(h.temperature_2m[idx] ?? temp),
        precipPct: h.precipitation_probability[idx] ?? 0,
        icon: codeToInfo(h.weather_code[idx] ?? code).icon,
      };
    });

    res.json({
      latitude,
      longitude,
      current: {
        temp,
        feelsLike: Math.round(c.apparent_temperature),
        humidity,
        windSpeed,
        uvIndex: uv,
        precipitation: parseFloat((c.precipitation ?? 0).toFixed(1)),
        cloudCover: c.cloud_cover,
        pressure: Math.round(c.surface_pressure),
        condition: info.condition,
        icon: info.icon,
        rainChance: rainPct,
      },
      forecast,
      hourly,
      farmingTip: buildFarmingTip(code, humidity, uv, windSpeed, temp, rainPct),
      sunrise: d.sunrise[0] ?? "",
      sunset: d.sunset[0] ?? "",
      updatedAt: new Date().toISOString(),
    });
  } catch (err) {
    req.log.error({ err }, "Weather fetch failed");
    res.status(503).json({ error: "Weather data temporarily unavailable" });
  }
});

export default weatherRouter;
