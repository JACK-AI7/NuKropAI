import React from "react";
import { StyleSheet, View, Text, Platform } from "react-native";
import MapView, { Polygon, Marker, Circle, PROVIDER_GOOGLE } from "react-native-maps";
import { useColors } from "@/hooks/useColors";
import type { Farm } from "@/contexts/AppContext";

interface FarmMapProps {
  farm: Farm;
  overlayType: "none" | "ndvi" | "outbreak" | "rainfall";
}

export function FarmMap({ farm, overlayType }: FarmMapProps) {
  const colors = useColors();

  // Mock NDVI overlay points
  const ndviPoints = [
    { lat: farm.lat + 0.0005, lon: farm.lon + 0.0005, value: 0.8 },
    { lat: farm.lat - 0.0005, lon: farm.lon - 0.0005, value: 0.4 },
    { lat: farm.lat + 0.0008, lon: farm.lon - 0.0002, value: 0.9 },
  ];

  return (
    <View style={styles.container}>
      <MapView
        provider={PROVIDER_GOOGLE}
        style={styles.map}
        initialRegion={{
          latitude: farm.lat,
          longitude: farm.lon,
          latitudeDelta: 0.005,
          longitudeDelta: 0.005,
        }}
        mapType="satellite"
      >
        {/* Farm Boundary */}
        {farm.boundaries && farm.boundaries.length > 0 && (
          <Polygon
            coordinates={farm.boundaries.map(p => ({ latitude: p.lat, longitude: p.lon }))}
            fillColor="rgba(34, 197, 94, 0.2)"
            strokeColor="#22C55E"
            strokeWidth={2}
          />
        )}

        {/* Center Marker */}
        <Marker coordinate={{ latitude: farm.lat, longitude: farm.lon }}>
          <View style={[styles.marker, { backgroundColor: colors.primary }]}>
            <Text style={styles.markerText}>{farm.name[0]}</Text>
          </View>
        </Marker>

        {/* NDVI Overlay Visualization */}
        {overlayType === "ndvi" && ndviPoints.map((p, i) => (
          <Circle
            key={`ndvi-${i}`}
            center={{ latitude: p.lat, longitude: p.lon }}
            radius={20}
            fillColor={p.value > 0.6 ? "rgba(34, 197, 94, 0.4)" : "rgba(245, 158, 11, 0.4)"}
            strokeWidth={0}
          />
        ))}

        {/* Outbreak Overlay */}
        {overlayType === "outbreak" && (
          <Circle
            center={{ latitude: farm.lat + 0.001, longitude: farm.lon + 0.001 }}
            radius={100}
            fillColor="rgba(239, 68, 68, 0.3)"
            strokeColor="#EF4444"
            strokeWidth={1}
          />
        )}

        {/* Rainfall Overlay */}
        {overlayType === "rainfall" && (
          <Circle
            center={{ latitude: farm.lat - 0.001, longitude: farm.lon - 0.001 }}
            radius={150}
            fillColor="rgba(59, 130, 246, 0.3)"
            strokeColor="#3B82F6"
            strokeWidth={1}
          />
        )}
      </MapView>

      <View style={[styles.legend, { backgroundColor: "rgba(0,0,0,0.7)" }]}>
        <Text style={styles.legendTitle}>Map Layers Active</Text>
        <View style={styles.legendRow}>
          <View style={[styles.legendDot, { backgroundColor: "#22C55E" }]} />
          <Text style={styles.legendText}>Farm boundary</Text>
        </View>
        {overlayType !== "none" && (
          <View style={styles.legendRow}>
            <View style={[styles.legendDot, { backgroundColor: overlayType === "outbreak" ? "#EF4444" : "#F59E0B" }]} />
            <Text style={styles.legendText}>{overlayType.toUpperCase()} Overlay</Text>
          </View>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    height: 300,
    borderRadius: 20,
    overflow: "hidden",
    marginTop: 12,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.1)",
  },
  map: {
    ...StyleSheet.absoluteFillObject,
  },
  marker: {
    width: 24,
    height: 24,
    borderRadius: 12,
    justifyContent: "center",
    alignItems: "center",
    borderWidth: 2,
    borderColor: "#fff",
  },
  markerText: {
    color: "#000",
    fontSize: 12,
    fontWeight: "800",
  },
  legend: {
    position: "absolute",
    bottom: 12,
    right: 12,
    padding: 10,
    borderRadius: 12,
    gap: 4,
  },
  legendTitle: {
    fontSize: 10,
    fontWeight: "700",
    color: "#fff",
    marginBottom: 2,
  },
  legendRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
  },
  legendDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
  },
  legendText: {
    fontSize: 9,
    color: "#ccc",
  },
});
