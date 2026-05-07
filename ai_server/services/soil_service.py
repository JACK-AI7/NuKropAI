"""Soil analysis service — parses diagnosis text for soil indicators."""

import logging
import re

logger = logging.getLogger("nukropai.soil")


class SoilService:

    # Simple keyword → nutrient level mapping
    DEFICIENCY_PATTERNS = {
        "nitrogen": ["yellowing", "yellow leaves", "pale green", "stunted"],
        "phosphorus": ["purple leaves", "dark green", "red stem", "delayed maturity"],
        "potassium": ["brown edges", "leaf scorch", "weak stems", "wilting"],
        "iron": ["interveinal chlorosis", "yellow between veins", "new leaves yellow"],
        "magnesium": ["older leaves yellow", "green veins", "magnesium"],
    }

    def analyze(self, diagnosis_text: str) -> dict:
        """
        Parse model diagnosis output and extract soil health indicators.
        Returns nutrient status, pH estimate, and recommendations.
        """
        lower = diagnosis_text.lower()

        detected_deficiencies = []
        for nutrient, keywords in self.DEFICIENCY_PATTERNS.items():
            if any(kw in lower for kw in keywords):
                detected_deficiencies.append(nutrient)

        # Estimate soil quality from language
        quality = "moderate"
        if "poor soil" in lower or "depleted" in lower or "exhausted" in lower:
            quality = "poor"
        elif "healthy soil" in lower or "good fertility" in lower or "rich" in lower:
            quality = "good"

        recommendations = []
        if "nitrogen" in detected_deficiencies:
            recommendations.append("Apply urea (46-0-0) at 20 kg/acre or incorporate legume cover crop")
        if "phosphorus" in detected_deficiencies:
            recommendations.append("Apply DAP (18-46-0) at 25 kg/acre before planting")
        if "potassium" in detected_deficiencies:
            recommendations.append("Apply MOP (0-0-60) at 15 kg/acre or wood ash mulch")
        if "iron" in detected_deficiencies:
            recommendations.append("Foliar spray ferrous sulfate (0.5%) twice weekly")
        if not recommendations:
            recommendations.append("Maintain balanced NPK schedule; test soil pH annually")

        return {
            "soil_quality": quality,
            "detected_deficiencies": detected_deficiencies,
            "nitrogen": "low" if "nitrogen" in detected_deficiencies else "adequate",
            "phosphorus": "low" if "phosphorus" in detected_deficiencies else "adequate",
            "potassium": "low" if "potassium" in detected_deficiencies else "adequate",
            "recommendations": recommendations,
        }


soil_service = SoilService()
