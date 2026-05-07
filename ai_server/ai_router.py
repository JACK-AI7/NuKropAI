"""
AIRouter — maps user questions to the most suitable model in the registry.
Implements keyword scoring with fallback to the default multimodal model.
"""

from config import DEFAULT_MODEL


# Keyword-to-model routing map (ordered by priority)
ROUTING_RULES = [
    # Pest & disease
    (["pest", "insect", "bug", "aphid", "whitefly", "caterpillar", "borer"], "qwen_vl"),
    # Soil & nutrients
    (["soil", "ph", "nutrient", "nitrogen", "phosphorus", "potassium", "npk", "deficiency"], "qwen_vl"),
    # Leaf / visual analysis
    (["leaf", "spot", "yellow", "brown", "blight", "rust", "wilt", "fungus", "mold"], "qwen_vl"),
    # Fruit & produce
    (["fruit", "vegetable", "tomato", "potato", "rice", "wheat", "maize", "cotton"], "qwen_vl"),
    # Treatment & chemicals
    (["treatment", "chemical", "spray", "pesticide", "fungicide", "herbicide", "organic"], "qwen_vl"),
    # Fertilizer
    (["fertilizer", "fertilise", "compost", "manure", "urea", "dag"], "qwen_vl"),
    # Irrigation & water
    (["irrigation", "water", "drip", "drought", "moisture", "watering"], "qwen_vl"),
    # Chatbot / general advice
    (["chat", "advice", "help", "what", "how", "why", "when", "should"], "qwen_vl"),
]


class AIRouter:
    """Route queries to the best-fit model based on keyword scoring."""

    def choose_model(self, question: str) -> str:
        q = question.lower()

        best_model = DEFAULT_MODEL
        best_score = 0

        for keywords, model_name in ROUTING_RULES:
            score = sum(1 for kw in keywords if kw in q)
            if score > best_score:
                best_score = score
                best_model = model_name

        return best_model

    def build_system_prompt(self, question: str) -> str:
        """Return a domain-specific system prompt for the question."""
        q = question.lower()

        if any(kw in q for kw in ["pest", "insect", "bug"]):
            return (
                "You are an expert agricultural entomologist. "
                "Identify pests from image descriptions, assess damage severity, "
                "and recommend organic and chemical treatment options."
            )

        if any(kw in q for kw in ["soil", "nutrient", "deficiency"]):
            return (
                "You are a soil scientist specializing in tropical agriculture. "
                "Analyze soil conditions and crop symptoms, then recommend "
                "precise NPK ratios and amendments."
            )

        if any(kw in q for kw in ["disease", "blight", "rust", "spot", "wilt"]):
            return (
                "You are a plant pathologist. Diagnose crop diseases from visual "
                "symptoms and images, and provide evidence-based treatment protocols."
            )

        return (
            "You are NuKrop, an expert AI agricultural advisor helping Indian farmers. "
            "Provide practical, actionable guidance in simple language. "
            "Always consider local farming conditions, limited resources, and "
            "organic alternatives where possible."
        )


ai_router = AIRouter()
