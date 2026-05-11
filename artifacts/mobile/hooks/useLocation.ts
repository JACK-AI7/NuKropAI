import * as Location from "expo-location";
import { useEffect } from "react";
import { Platform } from "react-native";
import { useApp } from "@/contexts/AppContext";

/**
 * Initializes the user's location from GPS (with permission request).
 * Falls back silently to default Hyderabad coordinates if permission is denied
 * or the device is on web.
 *
 * Call this hook once from the home screen. It writes lat/lon/city into
 * AppContext via setLocation so every other hook can read up-to-date
 * coordinates.
 */
export function useLocation(): void {
  const { setLocation } = useApp();

  useEffect(() => {
    let cancelled = false;

    const init = async () => {
      try {
        if (Platform.OS === "web") return;

        const { status } = await Location.requestForegroundPermissionsAsync();
        if (status !== "granted" || cancelled) return;

        const loc = await Location.getCurrentPositionAsync({
          accuracy: Location.Accuracy.Balanced,
          timeInterval: 0,
          distanceInterval: 0,
        });

        if (cancelled) return;

        const { latitude, longitude } = loc.coords;

        const reverseGeo = await Location.reverseGeocodeAsync({ latitude, longitude });
        const geo = reverseGeo[0];
        const city =
          geo?.city ??
          geo?.district ??
          geo?.subregion ??
          geo?.region ??
          "Your Location";

        if (!cancelled) {
          setLocation(latitude, longitude, city);
        }
      } catch (_) {
        // Keep default Hyderabad coordinates
      }
    };

    init();
    return () => {
      cancelled = true;
    };
  }, [setLocation]);
}
