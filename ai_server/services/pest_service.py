"""Pest detection service — parses diagnosis text for pest indicators."""

import logging

logger = logging.getLogger("nukropai.pest")


PEST_DATABASE = {
    "aphid": {
        "organic": "Neem oil spray (5ml/L) every 5 days; introduce ladybugs",
        "chemical": "Imidacloprid 17.8% SL @ 0.5 ml/L water",
        "severity": "medium",
    },
    "whitefly": {
        "organic": "Yellow sticky traps; neem-based soap spray",
        "chemical": "Thiamethoxam 25% WG @ 0.3 g/L water",
        "severity": "medium",
    },
    "caterpillar": {
        "organic": "Bacillus thuringiensis (Bt) spray; hand-picking at night",
        "chemical": "Chlorpyrifos 20% EC @ 2 ml/L water",
        "severity": "high",
    },
    "borer": {
        "organic": "Pheromone traps; Trichoderma-based biocontrol",
        "chemical": "Cartap hydrochloride 50% SP @ 1 g/L water",
        "severity": "high",
    },
    "mite": {
        "organic": "Sulphur dust (25 kg/ha); neem oil weekly",
        "chemical": "Dicofol 18.5% EC @ 2 ml/L water",
        "severity": "medium",
    },
    "thrips": {
        "organic": "Blue sticky traps; spinosad-based spray",
        "chemical": "Fipronil 5% SC @ 1.5 ml/L water",
        "severity": "medium",
    },
    "locust": {
        "organic": "Green muscle (Metarhizium) biological spray",
        "chemical": "Malathion 96% ULV aerial application (coordinate with agriculture dept)",
        "severity": "critical",
    },
}


class PestService:

    def analyze(self, diagnosis_text: str) -> dict:
        """
        Scan the model's diagnosis for pest mentions and return
        treatment recommendations from the pest database.
        """
        lower = diagnosis_text.lower()

        detected_pests = []
        for pest_name in PEST_DATABASE:
            if pest_name in lower:
                detected_pests.append(pest_name)

        if not detected_pests:
            # Check generic indicators
            pest_detected = any(
                kw in lower for kw in [
                    "pest", "insect", "bug", "infestation", "larvae", "eggs",
                    "damage", "feeding", "holes in leaves",
                ]
            )
            if pest_detected:
                return {
                    "pest_detected": True,
                    "pests_identified": ["unidentified pest"],
                    "severity": "unknown",
                    "organic_solution": "Apply neem oil spray (5ml/L) as a broad-spectrum organic control",
                    "chemical_solution": "Consult local agriculture officer for targeted pesticide",
                    "action_required": True,
                }
            return {
                "pest_detected": False,
                "pests_identified": [],
                "severity": "none",
                "organic_solution": "No pest control required at this time",
                "chemical_solution": None,
                "action_required": False,
            }

        # Use the most severe detected pest for primary recommendation
        severity_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        primary_pest = max(
            detected_pests,
            key=lambda p: severity_order.get(PEST_DATABASE[p]["severity"], 0),
        )
        info = PEST_DATABASE[primary_pest]

        return {
            "pest_detected": True,
            "pests_identified": detected_pests,
            "primary_pest": primary_pest,
            "severity": info["severity"],
            "organic_solution": info["organic"],
            "chemical_solution": info["chemical"],
            "action_required": info["severity"] in ("high", "critical"),
        }


pest_service = PestService()
