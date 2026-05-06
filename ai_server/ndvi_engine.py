import numpy as np

class NDVIEngine:
    def get_ndvi(self, lat, lon):
        """Simulate NDVI (Normalized Difference Vegetation Index)"""
        # NDVI > 0.6 is healthy vegetation, < 0.2 is stress/soil
        return round(0.3 + np.random.rand() * 0.5, 2)

    def analyze_field(self, lat, lon):
        ndvi = self.get_ndvi(lat, lon)
        return {
            "ndvi": ndvi,
            "moisture_stress": "Low" if ndvi > 0.5 else "Medium",
            "biomass_index": round(0.5 + ndvi * 0.3, 2),
            "prediction": "Optimal harvest in 12 days" if ndvi > 0.7 else "Continue monitoring"
        }

ndvi_engine = NDVIEngine()
