// ContentView.swift
// CampusAccesible

import SwiftUI

struct ContentView: View {
    @State private var dataService = CampusDataService()
    @State private var selectedTab = "ruta"

    var body: some View {
        TabView(selection: $selectedTab) {
            Tab("Explora", systemImage: "building.2", value: "explora") {
                ExploreView()
            }
            Tab("Ruta", systemImage: "map", value: "ruta") {
                RouteView()
            }
            Tab("Créditos", systemImage: "info.circle", value: "creditos") {
                CreditsView()
            }
        }
        .environment(dataService)
        .tabBarMinimizeBehavior(.onScrollDown)
    }
}

#Preview {
    ContentView()
}
