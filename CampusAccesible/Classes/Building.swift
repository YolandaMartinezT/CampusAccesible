// Building.swift
// CampusAccesible

import Foundation

struct Building: Identifiable, Hashable {
    let id: String
    let name: String
    let imageName: String
    /// nil means the building has no elevator information
    let hasElevator: Bool?
    let schedule: String
    let bathrooms: [Bathroom]
    let floors: [FloorInfo]
    let category: String
    let coordIndices: [Int]
    let show: Bool
}

struct Bathroom: Identifiable, Hashable {
    let id: String
    let name: String
    let isAccessible: Bool
}

struct FloorInfo: Identifiable, Hashable {
    let id: Int           // parse index — unique even when floor numbers repeat
    let floorNumber: Int  // actual floor number used for sorting and grouping
    let description: String

    var displayName: String {
        switch floorNumber {
        case ..<0:  return floorNumber == -1 ? "Sótano" : "Sótano \(abs(floorNumber))"
        case 0:     return "Planta Baja"
        default:    return "Piso \(floorNumber)"
        }
    }
}
