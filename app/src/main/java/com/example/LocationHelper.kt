package com.example

import android.annotation.SuppressLint
import android.content.Context
import android.location.Geocoder
import android.location.Location
import com.google.android.gms.location.LocationServices
import kotlinx.coroutines.tasks.await
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlin.coroutines.resume
import java.util.Locale

object LocationHelper {
    @SuppressLint("MissingPermission")
    suspend fun getCurrentLocationStateAndMandi(context: Context): Pair<String, String>? {
        return try {
            val fusedLocationClient = LocationServices.getFusedLocationProviderClient(context)
            val location: Location? = fusedLocationClient.lastLocation.await()

            if (location != null) {
                val geocoder = Geocoder(context, Locale.getDefault())
                if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
                    return suspendCancellableCoroutine { cont ->
                        geocoder.getFromLocation(location.latitude, location.longitude, 1, object : Geocoder.GeocodeListener {
                            override fun onGeocode(addresses: MutableList<android.location.Address>) {
                                if (addresses.isNotEmpty()) {
                                    val address = addresses[0]
                                    val state = address.adminArea ?: ""
                                    val city = address.locality ?: address.subAdminArea ?: ""
                                    cont.resume(Pair(state, city))
                                } else {
                                    cont.resume(null)
                                }
                            }
                            override fun onError(errorMessage: String?) {
                                cont.resume(null)
                            }
                        })
                    }
                } else {
                    @Suppress("DEPRECATION")
                    val addresses = geocoder.getFromLocation(location.latitude, location.longitude, 1)
                    if (!addresses.isNullOrEmpty()) {
                        val address = addresses[0]
                        val state = address.adminArea ?: ""
                        val city = address.locality ?: address.subAdminArea ?: ""
                        Pair(state, city)
                    } else {
                        null
                    }
                }
            } else {
                null
            }
        } catch (e: Exception) {
            e.printStackTrace()
            null
        }
    }
    @SuppressLint("MissingPermission")
    suspend fun getCurrentLocationCoords(context: Context): Pair<Double, Double>? {
        return try {
            val fusedLocationClient = LocationServices.getFusedLocationProviderClient(context)
            val location: Location? = fusedLocationClient.lastLocation.await()
            if (location != null) Pair(location.latitude, location.longitude) else null
        } catch (e: Exception) {
            e.printStackTrace()
            null
        }
    }
}
