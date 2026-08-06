package com.example

import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*
import java.util.concurrent.atomic.AtomicBoolean

data class TickerItem(
    val commodity: String,
    val modalPrice: Double,
    val prevPrice: Double,  // previous poll price for delta
    val market: String,
    val state: String,
    val arrivalDate: String
) {
    val delta: Double get() = modalPrice - prevPrice
    val isUp: Boolean get() = delta > 0
    val isDown: Boolean get() = delta < 0
    val changePercent: Double get() = if (prevPrice > 0) (delta / prevPrice) * 100 else 0.0
}

/**
 * Production-grade live price ticker service.
 * Polls MandiApiService for a basket of major commodities every 3 minutes.
 * Calculates price deltas between polls for directional indicators.
 */
object PriceTickerService {

    private val scope = CoroutineScope(Dispatchers.IO + SupervisorJob())

    private val TRACKED_BASKET = listOf(
        "Maharashtra" to "Tomato",
        "Maharashtra" to "Onion",
        "Punjab"      to "Wheat",
        "Gujarat"     to "Cotton",
        "Uttar Pradesh" to "Potato",
        "Karnataka"   to "Rice",
        "Rajasthan"   to "Mustard"
    )

    private val _tickerItems = MutableStateFlow<List<TickerItem>>(emptyList())
    val tickerItems: StateFlow<List<TickerItem>> = _tickerItems.asStateFlow()

    private val _isLoading = MutableStateFlow(true)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    private val isStarted = AtomicBoolean(false)

    fun start() {
        if (!isStarted.compareAndSet(false, true)) return

        scope.launch {
            while (isActive) {
                val prevPriceMap = _tickerItems.value.associate { it.commodity to it.modalPrice }
                val fetched = mutableListOf<TickerItem>()

                // Stagger requests to avoid hammering the API
                TRACKED_BASKET.forEach { (state, commodity) ->
                    try {
                        val flow = MandiApiService.watchLiveMandiPrices(state, commodity)
                        val snapshot = flow.first { it !is MandiState.Loading }
                        if (snapshot is MandiState.Success && snapshot.records.isNotEmpty()) {
                            val topRecord = snapshot.records.maxByOrNull { it.modalPrice }!!
                            fetched.add(
                                TickerItem(
                                    commodity = topRecord.commodity.replaceFirstChar { it.uppercase() },
                                    modalPrice = topRecord.modalPrice,
                                    prevPrice = prevPriceMap[topRecord.commodity.replaceFirstChar { it.uppercase() }]
                                        ?: topRecord.modalPrice,
                                    market = topRecord.market,
                                    state = topRecord.state,
                                    arrivalDate = topRecord.arrivalDate
                                )
                            )
                        }
                    } catch (_: Exception) { /* skip failed commodity */ }
                    delay(500L) // 500ms stagger between requests
                }

                if (fetched.isNotEmpty()) {
                    _tickerItems.value = fetched
                    _isLoading.value = false
                }

                delay(3 * 60 * 1000L) // Refresh every 3 minutes
            }
        }
    }

    fun stop() {
        scope.cancel()
    }
}
