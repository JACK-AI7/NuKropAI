class FertilizerService:

    def recommend(self, crop_name):

        return {
            "crop": crop_name,
            "fertilizer": "NPK 19-19-19",
            "frequency": "Every 15 days"
        }


fertilizer_service = FertilizerService()
