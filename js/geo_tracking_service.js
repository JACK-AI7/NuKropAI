/**
 * ============================================================================
 * RAPIDO-STYLE LIVE LOCATION TRACKING & REAL-STREET ROUTING SERVICE
 * ============================================================================
 * 
 * Tech Stack:
 * - Database: Supabase (PostgreSQL with PostGIS extension & RPC)
 * - Real-Time: Supabase Realtime (Broadcast / Presence channels)
 * - Routing: OSRM (Open Source Routing Machine) / OpenStreetMap GeoJSON
 * - Frontend: Leaflet.js / OpenStreetMap tile rendering with smooth interpolation
 * 
 * Coordinate Convention:
 * - All spatial logic, PostGIS RPCs, and GeoJSON use standard [longitude, latitude].
 * - Leaflet conversion to [lat, lon] is handled strictly at the map render boundary.
 */

(function (global) {
  'use strict';

  class GeoTrackingService {
    /**
     * @param {Object} config
     * @param {Object} config.supabaseClient - Initialized Supabase JS client
     * @param {string} [config.osrmBaseUrl]   - Base URL for OSRM routing server
     * @param {string} [config.channelName]   - Supabase Realtime channel name
     */
    constructor(config = {}) {
      if (!config.supabaseClient) {
        throw new Error('[GeoTrackingService] A valid Supabase client instance is required.');
      }
      this.supabase = config.supabaseClient;
      this.osrmBaseUrl = config.osrmBaseUrl || 'https://router.project-osrm.org';
      this.defaultChannelName = config.channelName || 'driver-tracking';
      this.activeChannels = new Map();
      this.broadcastIntervals = new Map();
    }

    // ========================================================================
    // 1. POSTGIS SPATIAL QUERIES (RPC)
    // ========================================================================

    /**
     * Queries nearest active drivers within radius using PostGIS ST_DWithin & ST_Distance.
     * 
     * @param {number} userLon - User's longitude in degrees (-180 to 180)
     * @param {number} userLat - User's latitude in degrees (-90 to 90)
     * @param {number} [radiusMeters=5000] - Search radius in meters
     * @param {number} [maxDrivers=15] - Maximum drivers to return
     * @returns {Promise<Array<{driver_id: string, lon: number, lat: number, heading: number, speed_kmh: number, distance_meters: number}>>}
     */
    async getNearestDrivers(userLon, userLat, radiusMeters = 5000, maxDrivers = 15) {
      if (typeof userLon !== 'number' || typeof userLat !== 'number') {
        throw new Error('[GeoTrackingService] Invalid coordinates. userLon and userLat must be numbers.');
      }

      const { data, error } = await this.supabase.rpc('get_nearest_drivers', {
        user_lon: userLon,
        user_lat: userLat,
        radius_meters: radiusMeters,
        max_drivers: maxDrivers
      });

      if (error) {
        console.error('[GeoTrackingService] Error querying nearest drivers:', error);
        throw error;
      }

      return data || [];
    }

    /**
     * Upserts driver location into the PostGIS driver_locations table.
     * 
     * @param {Object} params
     * @param {string} params.driverId
     * @param {number} params.lon
     * @param {number} params.lat
     * @param {number} [params.heading=0]
     * @param {number} [params.speedKmh=0]
     */
    async recordDriverLocation({ driverId, lon, lat, heading = 0, speedKmh = 0 }) {
      const { error } = await this.supabase.rpc('upsert_driver_location', {
        p_driver_id: driverId,
        p_lon: lon,
        p_lat: lat,
        p_heading: heading,
        p_speed_kmh: speedKmh
      });

      if (error) {
        console.warn('[GeoTrackingService] DB telemetry upsert failed (continuing broadcast):', error.message);
      }
    }

    // ========================================================================
    // 2. REAL-TIME LOCATION TRACKING (SUPABASE REALTIME BROADCAST & PRESENCE)
    // ========================================================================

    /**
     * Driver Side: Streams GPS changes via WebSocket broadcast and manages presence.
     * Prevents heavy database polling by decoupling high-frequency WebSocket
     * streaming from throttled database persistence.
     * 
     * @param {Object} options
     * @param {string} options.driverId - Unique driver identifier
     * @param {Function} options.getCoordinates - Async or sync callback returning { lon, lat, heading, speed }
     * @param {number} [options.intervalMs=2500] - Broadcast cadence in milliseconds
     * @param {string} [options.channelName] - Optional override channel name
     * @param {boolean} [options.persistToDb=true] - Whether to periodically sync to PostGIS table
     * @returns {Object} Broadcast controller with stop() method
     */
    startDriverBroadcast({
      driverId,
      getCoordinates,
      intervalMs = 2500,
      channelName = this.defaultChannelName,
      persistToDb = true
    }) {
      if (!driverId || typeof getCoordinates !== 'function') {
        throw new Error('[GeoTrackingService] driverId and getCoordinates function are required.');
      }

      // Clean up any existing broadcaster for this driver
      this.stopDriverBroadcast(driverId);

      const channel = this.supabase.channel(channelName, {
        config: {
          broadcast: { self: false },
          presence: { key: driverId }
        }
      });

      let dbSyncCounter = 0;

      channel.subscribe(async (status) => {
        if (status === 'SUBSCRIBED') {
          // Track driver presence state
          await channel.track({
            driver_id: driverId,
            status: 'ONLINE',
            online_at: new Date().toISOString()
          });

          // Begin high-frequency broadcast loop
          const intervalId = setInterval(async () => {
            try {
              const coords = await getCoordinates();
              if (!coords || typeof coords.lon !== 'number' || typeof coords.lat !== 'number') return;

              const payload = {
                driver_id: driverId,
                lon: coords.lon,
                lat: coords.lat,
                heading: coords.heading || 0,
                speed_kmh: coords.speed || 0,
                timestamp: Date.now()
              };

              // Stream instantaneously over WebSocket broadcast
              await channel.send({
                type: 'broadcast',
                event: 'driver-location',
                payload: payload
              });

              // Throttled persistence: save to PostGIS table every 4 broadcast cycles (~10s)
              dbSyncCounter++;
              if (persistToDb && dbSyncCounter % 4 === 0) {
                this.recordDriverLocation({
                  driverId,
                  lon: coords.lon,
                  lat: coords.lat,
                  heading: coords.heading || 0,
                  speedKmh: coords.speed || 0
                });
              }
            } catch (err) {
              console.warn('[GeoTrackingService] Broadcast loop error:', err);
            }
          }, intervalMs);

          this.broadcastIntervals.set(driverId, intervalId);
        }
      });

      this.activeChannels.set(`broadcaster:${driverId}`, channel);

      return {
        stop: () => this.stopDriverBroadcast(driverId)
      };
    }

    /**
     * Stops driver location broadcast and cleans up channel.
     * 
     * @param {string} driverId
     */
    stopDriverBroadcast(driverId) {
      if (this.broadcastIntervals.has(driverId)) {
        clearInterval(this.broadcastIntervals.get(driverId));
        this.broadcastIntervals.delete(driverId);
      }

      const key = `broadcaster:${driverId}`;
      if (this.activeChannels.has(key)) {
        const channel = this.activeChannels.get(key);
        channel.untrack().catch(() => {});
        this.supabase.removeChannel(channel);
        this.activeChannels.delete(key);
      }
    }

    /**
     * Client Side: Subscribes to real-time driver updates via WebSocket broadcast.
     * 
     * @param {Object} options
     * @param {string} [options.driverId] - Optional driver ID filter (null = listen to all nearby drivers)
     * @param {string} [options.channelName] - Optional override channel name
     * @param {Function} options.onLocationUpdate - Callback triggered with { driver_id, lon, lat, heading, speed_kmh, timestamp }
     * @param {Function} [options.onPresenceChange] - Callback triggered when drivers join or leave
     * @returns {Object} Subscription controller with unsubscribe() method
     */
    subscribeToDriverTracking({
      driverId = null,
      channelName = this.defaultChannelName,
      onLocationUpdate,
      onPresenceChange = null
    }) {
      if (typeof onLocationUpdate !== 'function') {
        throw new Error('[GeoTrackingService] onLocationUpdate callback is required.');
      }

      const subKey = `subscriber:${driverId || 'all'}:${Date.now()}`;
      const channel = this.supabase.channel(channelName);

      channel
        .on('broadcast', { event: 'driver-location' }, ({ payload }) => {
          if (!payload) return;
          if (driverId && payload.driver_id !== driverId) return;
          onLocationUpdate(payload);
        });

      if (typeof onPresenceChange === 'function') {
        channel
          .on('presence', { event: 'sync' }, () => {
            const state = channel.presenceState();
            onPresenceChange({ event: 'sync', state });
          })
          .on('presence', { event: 'join' }, ({ key, newPresences }) => {
            onPresenceChange({ event: 'join', key, presences: newPresences });
          })
          .on('presence', { event: 'leave' }, ({ key, leftPresences }) => {
            onPresenceChange({ event: 'leave', key, presences: leftPresences });
          });
      }

      channel.subscribe();
      this.activeChannels.set(subKey, channel);

      return {
        unsubscribe: () => {
          this.supabase.removeChannel(channel);
          this.activeChannels.delete(subKey);
        }
      };
    }

    // ========================================================================
    // 3. "REAL STREETS" PATH ROUTING & DISTANCE MATRIX (OSM / OSRM)
    // ========================================================================

    /**
     * Calculates an authentic on-road route between two points using OSRM.
     * Coordinates MUST be provided in standard [longitude, latitude] order.
     * 
     * @param {Array<number>} startLonLat - [lon, lat] of origin (Driver position)
     * @param {Array<number>} endLonLat   - [lon, lat] of destination (Pickup / Dropoff)
     * @param {Object} [options]
     * @param {string} [options.profile='driving'] - 'driving' | 'bike' | 'walking'
     * @param {boolean} [options.steps=true] - Return turn-by-turn steps
     * @returns {Promise<{
     *   coordinates: Array<[number, number]>,
     *   distanceMeters: number,
     *   distanceKm: number,
     *   durationSeconds: number,
     *   durationMinutes: number,
     *   etaFormatted: string,
     *   steps: Array<Object>
     * }>}
     */
    async fetchStreetRoute(startLonLat, endLonLat, options = {}) {
      if (!Array.isArray(startLonLat) || !Array.isArray(endLonLat) ||
          startLonLat.length < 2 || endLonLat.length < 2) {
        throw new Error('[GeoTrackingService] Coordinates must be valid [lon, lat] arrays.');
      }

      const [startLon, startLat] = startLonLat;
      const [endLon, endLat] = endLonLat;
      const profile = options.profile || 'driving';
      const steps = options.steps !== false ? 'true' : 'false';

      // Format strictly as {lon},{lat};{lon},{lat}
      const coordsString = `${startLon},${startLat};${endLon},${endLat}`;
      const url = `${this.osrmBaseUrl}/route/v1/${profile}/${coordsString}?overview=full&geometries=geojson&steps=${steps}`;

      try {
        const response = await fetch(url, { method: 'GET' });
        if (!response.ok) {
          throw new Error(`OSRM HTTP error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        if (data.code !== 'Ok' || !data.routes || data.routes.length === 0) {
          throw new Error(`OSRM routing failed with code: ${data.code || 'NO_ROUTE'}`);
        }

        const primaryRoute = data.routes[0];
        const distanceMeters = primaryRoute.distance;
        const durationSeconds = primaryRoute.duration;
        const coordinates = primaryRoute.geometry.coordinates; // Standard GeoJSON [ [lon, lat], ... ]

        const distanceKm = Math.round((distanceMeters / 1000) * 10) / 10;
        const durationMinutes = Math.max(1, Math.round(durationSeconds / 60));

        let etaFormatted = `${durationMinutes} mins`;
        if (durationMinutes >= 60) {
          const hrs = Math.floor(durationMinutes / 60);
          const mins = durationMinutes % 60;
          etaFormatted = `${hrs} hr ${mins} mins`;
        }

        const maneuverSteps = (primaryRoute.legs && primaryRoute.legs[0] && primaryRoute.legs[0].steps)
          ? primaryRoute.legs[0].steps.map(s => ({
              instruction: s.maneuver ? `${s.maneuver.type || ''} ${s.maneuver.modifier || ''}`.trim() : '',
              streetName: s.name || '',
              distanceMeters: s.distance,
              durationSeconds: s.duration
            }))
          : [];

        return {
          coordinates: coordinates,
          distanceMeters: distanceMeters,
          distanceKm: distanceKm,
          durationSeconds: durationSeconds,
          durationMinutes: durationMinutes,
          etaFormatted: etaFormatted,
          steps: maneuverSteps
        };
      } catch (err) {
        console.warn('[GeoTrackingService] OSRM routing request failed, falling back to geodesic line:', err.message);
        return this._getGeodesicFallbackRoute(startLonLat, endLonLat);
      }
    }

    /**
     * Fallback straight-line route if OSRM public server is unavailable.
     * @private
     */
    _getGeodesicFallbackRoute(startLonLat, endLonLat) {
      const [lon1, lat1] = startLonLat;
      const [lon2, lat2] = endLonLat;

      const dLat = (lat2 - lat1) * Math.PI / 180;
      const dLon = (lon2 - lon1) * Math.PI / 180;
      const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                Math.sin(dLon/2) * Math.sin(dLon/2);
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
      const distanceKm = Math.round(6371 * c * 10) / 10;
      const durationMinutes = Math.max(1, Math.round(distanceKm * 2.2));

      return {
        coordinates: [startLonLat, endLonLat],
        distanceMeters: distanceKm * 1000,
        distanceKm: distanceKm,
        durationSeconds: durationMinutes * 60,
        durationMinutes: durationMinutes,
        etaFormatted: `${durationMinutes} mins`,
        steps: []
      };
    }

    // ========================================================================
    // 4. FRONTEND MAP RENDERING & SMOOTH VEHICLE INTERPOLATION (LEAFLET / OSM)
    // ========================================================================

    /**
     * Initializes a real-time Rapido-style route and animated vehicle renderer on Leaflet.
     * 
     * @param {Object} options
     * @param {Object} options.map - Leaflet map instance (L.Map)
     * @param {string} [options.vehicleIconUrl] - URL to vehicle icon/PNG
     * @param {number} [options.iconWidth=48] - Vehicle icon width
     * @param {number} [options.iconHeight=48] - Vehicle icon height
     * @param {string} [options.routeColor='#16A34A'] - Route line color (Rapido green / neon)
     * @returns {Object} Renderer controller
     */
    createRealtimeRouteRenderer({
      map,
      vehicleIconUrl = 'images/trucks/tata_ace.png',
      iconWidth = 48,
      iconHeight = 48,
      routeColor = '#16A34A'
    }) {
      if (!map || typeof map.addLayer !== 'function') {
        throw new Error('[GeoTrackingService] A valid Leaflet map instance is required.');
      }

      let routeGlowLayer = null;
      let routeLineLayer = null;
      let driverMarker = null;
      let currentMarkerCoords = null; // [lat, lon]
      let animationFrameId = null;

      /**
       * Creates or updates a custom rotating Leaflet DivIcon
       */
      const createVehicleIcon = (iconUrl, heading = 0) => {
        return L.divIcon({
          className: 'rapido-live-driver-icon',
          html: `
            <div style="width:${iconWidth}px;height:${iconHeight}px;display:flex;align-items:center;justify-content:center;transform:rotate(${heading}deg);transition:transform 0.3s cubic-bezier(0.16,1,0.3,1);filter:drop-shadow(0 4px 10px rgba(0,0,0,0.35));">
              <img src="${iconUrl}" style="width:100%;height:100%;object-fit:contain;pointer-events:none;" alt="Driver" />
            </div>
          `,
          iconSize: [iconWidth, iconHeight],
          iconAnchor: [iconWidth / 2, iconHeight / 2]
        });
      };

      return {
        /**
         * Renders the OSRM GeoJSON path onto OpenStreetMap with dual neon layers.
         * Accepts standard GeoJSON coordinates in [lon, lat] format.
         * 
         * @param {Array<[number, number]>} geoJsonCoordinates - Array of [lon, lat]
         * @param {boolean} [fitBounds=true] - Auto-zoom/pan to encompass the route
         */
        renderRoute: (geoJsonCoordinates, fitBounds = true) => {
          if (!Array.isArray(geoJsonCoordinates) || geoJsonCoordinates.length === 0) return;

          // Convert standard GeoJSON [lon, lat] to Leaflet's [lat, lon]
          const latLngs = geoJsonCoordinates.map(pt => [pt[1], pt[0]]);

          // Remove prior route layers if present
          if (routeGlowLayer) map.removeLayer(routeGlowLayer);
          if (routeLineLayer) map.removeLayer(routeLineLayer);

          // Outer dark casing / glow for high contrast over OSM streets
          routeGlowLayer = L.polyline(latLngs, {
            color: '#0F172A',
            weight: 7,
            opacity: 0.6,
            lineCap: 'round',
            lineJoin: 'round'
          }).addTo(map);

          // Inner high-visibility active route line
          routeLineLayer = L.polyline(latLngs, {
            color: routeColor,
            weight: 4.5,
            opacity: 0.95,
            lineCap: 'round',
            lineJoin: 'round'
          }).addTo(map);

          if (fitBounds) {
            map.fitBounds(routeLineLayer.getBounds(), { padding: [40, 40] });
          }
        },

        /**
         * Smoothly updates driver vehicle marker with interpolated position & heading.
         * 
         * @param {Object} telemetry
         * @param {number} telemetry.lon - Driver longitude
         * @param {number} telemetry.lat - Driver latitude
         * @param {number} [telemetry.heading=0] - Heading/bearing in degrees
         * @param {string} [telemetry.iconUrl] - Optional updated vehicle icon URL
         * @param {number} [animationDurationMs=1200] - Duration of smooth transition
         */
        updateDriverPosition: (telemetry, animationDurationMs = 1200) => {
          const targetLat = telemetry.lat;
          const targetLon = telemetry.lon;
          const heading = telemetry.heading || 0;
          const iconUrl = telemetry.iconUrl || vehicleIconUrl;

          // Initial marker creation
          if (!driverMarker) {
            driverMarker = L.marker([targetLat, targetLon], {
              icon: createVehicleIcon(iconUrl, heading),
              zIndexOffset: 1000
            }).addTo(map);
            currentMarkerCoords = [targetLat, targetLon];
            return;
          }

          // Smooth coordinate tweening via requestAnimationFrame
          if (animationFrameId) cancelAnimationFrame(animationFrameId);

          const startLat = currentMarkerCoords[0];
          const startLon = currentMarkerCoords[1];
          const startTime = performance.now();

          const animateStep = (now) => {
            const elapsed = now - startTime;
            const progress = Math.min(elapsed / animationDurationMs, 1.0);

            // Ease-out cubic formula for natural deceleration
            const ease = 1 - Math.pow(1 - progress, 3);
            const currentLat = startLat + (targetLat - startLat) * ease;
            const currentLon = startLon + (targetLon - startLon) * ease;

            driverMarker.setLatLng([currentLat, currentLon]);
            currentMarkerCoords = [currentLat, currentLon];

            if (progress < 1.0) {
              animationFrameId = requestAnimationFrame(animateStep);
            } else {
              animationFrameId = null;
              currentMarkerCoords = [targetLat, targetLon];
            }
          };

          // Update rotation & icon
          driverMarker.setIcon(createVehicleIcon(iconUrl, heading));
          animationFrameId = requestAnimationFrame(animateStep);
        },

        /**
         * Destroys all route layers and driver marker from the map.
         */
        destroy: () => {
          if (animationFrameId) cancelAnimationFrame(animationFrameId);
          if (routeGlowLayer) map.removeLayer(routeGlowLayer);
          if (routeLineLayer) map.removeLayer(routeLineLayer);
          if (driverMarker) map.removeLayer(driverMarker);
        }
      };
    }
  }

  // Export as UMD / Global
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = GeoTrackingService;
  } else {
    global.GeoTrackingService = GeoTrackingService;
  }
})(typeof window !== 'undefined' ? window : this);
