"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = require("express");
const weather_controller_1 = require("../controllers/weather.controller");
const router = (0, express_1.Router)();
// GET /api/weather?lat=...&lng=...
router.get('/', weather_controller_1.WeatherController.getWeather);
exports.default = router;
