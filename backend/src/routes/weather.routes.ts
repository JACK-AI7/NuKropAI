import { Router } from 'express';
import { WeatherController } from '../controllers/weather.controller';

const router = Router();

// GET /api/weather?lat=...&lng=...
router.get('/', WeatherController.getWeather);

export default router;
