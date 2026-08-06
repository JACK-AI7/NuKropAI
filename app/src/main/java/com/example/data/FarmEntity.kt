package com.example.data

import androidx.room.Entity
import androidx.room.PrimaryKey
import androidx.room.ForeignKey

@Entity(tableName = "farms")
data class FarmEntity(
    @PrimaryKey val id: String,
    val name: String,
    val geojsonBoundary: String, // Stored as GeoJSON string for offline map rendering
    val totalAcreage: Double,
    val isSynced: Boolean = false
)

@Entity(
    tableName = "zones",
    foreignKeys = [
        ForeignKey(
            entity = FarmEntity::class,
            parentColumns = ["id"],
            childColumns = ["farmId"],
            onDelete = ForeignKey.CASCADE
        )
    ]
)
data class ZoneEntity(
    @PrimaryKey val id: String,
    val farmId: String,
    val name: String,
    val geojsonBoundary: String,
    val cropType: String,
    val plantingDate: Long?, // Epoch timestamp
    val expectedHarvestDate: Long?,
    val isSynced: Boolean = false
)
