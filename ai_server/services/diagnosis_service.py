"""Diagnosis service — builds detailed agricultural analysis prompts."""

import logging

logger = logging.getLogger("nukropai.diagnosis")


class DiagnosisService:

    def build_prompt(self, user_question: str) -> str:
        """
        Build a detailed, structured prompt for crop image analysis.
        Combines the user question with structured output requirements.
        """
        base = (
            "Please analyze this agricultural image carefully.\n\n"
            "Provide a structured diagnosis covering:\n"
            "1. 🌿 Crop/Plant identification (species and variety if visible)\n"
            "2. 🦠 Disease or condition (name, causal agent, severity: mild/moderate/severe)\n"
            "3. 🐛 Pest presence (name, damage type, infestation level)\n"
            "4. 🌍 Soil symptoms (color, texture, moisture indicators)\n"
            "5. 💊 Nutrient deficiency signs (N, P, K, Mg, Fe, etc.)\n"
            "6. 🌿 Organic treatment options (biological/natural methods)\n"
            "7. ⚗️ Chemical treatment options (specific product names and dosage)\n"
            "8. ⏰ Urgency level (immediate/within 1 week/routine monitoring)\n"
            "9. 🌾 Yield impact estimate (low/medium/high risk)\n"
        )

        if user_question and user_question.strip():
            base += f"\n\nFarmer's specific question: {user_question.strip()}\n"
            base += "Please address this question directly in your response."

        return base

    def parse_response(self, raw_text: str) -> dict:
        """
        Extract structured fields from the model's free-text response.
        Returns a dict with best-effort parsed values.
        """
        result = {
            "raw": raw_text,
            "crop_identified": None,
            "disease": None,
            "severity": None,
            "urgency": None,
        }

        lower = raw_text.lower()

        # Urgency extraction
        if "immediate" in lower or "urgent" in lower:
            result["urgency"] = "immediate"
        elif "within" in lower and "week" in lower:
            result["urgency"] = "within_1_week"
        else:
            result["urgency"] = "routine"

        # Severity extraction
        if "severe" in lower:
            result["severity"] = "severe"
        elif "moderate" in lower:
            result["severity"] = "moderate"
        elif "mild" in lower:
            result["severity"] = "mild"

        return result


diagnosis_service = DiagnosisService()
