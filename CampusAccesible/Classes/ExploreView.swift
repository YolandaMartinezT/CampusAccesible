// ExploreView.swift
// CampusAccesible

import SwiftUI

struct ExploreView: View {
    @Environment(CampusDataService.self) private var dataService

    private var buildingsByCategory: [(category: String, buildings: [Building])] {
        let visible = dataService.buildings.values.filter { $0.show }
        let grouped = Dictionary(grouping: visible, by: \.category)
        return grouped
            .map { (category: $0.key, buildings: $0.value.sorted { $0.name < $1.name }) }
            .sorted { $0.category < $1.category }
    }

    var body: some View {
        NavigationStack {
            List {
                ForEach(buildingsByCategory, id: \.category) { group in
                    Section(group.category) {
                        ForEach(group.buildings) { building in
                            NavigationLink(value: building) {
                                BuildingListRow(building: building)
                            }
                            .accessibilityLabel(building.name)
                        }
                    }
                }
            }
            .navigationTitle("Explora")
            .navigationDestination(for: Building.self) { building in
                BuildingDetailView(building: building)
            }
        }
    }
}

private struct BuildingListRow: View {
    let building: Building

    var body: some View {
        HStack(spacing: 12) {
            Image(building.imageName)
                .resizable()
                .scaledToFill()
                .frame(width: 44, height: 44)
                .clipShape(.circle)
            Text(building.name)
                .font(.body)
        }
    }
}

#Preview {
    ExploreView()
        .environment(CampusDataService())
}
