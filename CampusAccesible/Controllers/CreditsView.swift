// CreditsView.swift
// CampusAccesible

import SwiftUI

struct CreditsView: View {
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 24) {
                    Image("logo")
                        .resizable()
                        .scaledToFit()
                        .frame(height: 80)
                        .accessibilityLabel("ExploraTec logo")

                    VStack(alignment: .leading, spacing: 4) {
                        Text("ExploraTec")
                            .font(.largeTitle.bold())
                        Text("Departamento de accesibilidad — Tec de Monterrey")
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                    }

                    Divider()
                    Text("ExploraTec fue desarrollado originalmente por estudiantes del Tecnológico de Monterrey durante el semestre enero – mayo de 2018, como parte del curso Desarrollo de Aplicaciones para Dispositivos Móviles, asesorados por la maestra Yolanda Martínez Treviño. En 2026, la aplicación fue rediseñada completamente en SwiftUI con soporte para iOS 26.")
                    
                    Divider()
                    VStack(alignment: .leading, spacing: 16) {
                        Text("Equipo de Desarrollo")
                            .font(.headline)

                        CreditRow(name: "Joao Gabriel Moura De Almeida", role: "Desarrollo iOS")
                        CreditRow(name: "Luis Villarreal", role: "Desarrollo iOS")
                        CreditRow(name: "Arturo González", role: "Desarrollo iOS")
                        CreditRow(name: "Louis Loewen", role: "Rediseño SwiftUI · iOS 26")
                    }
                    
                    Divider()

                    Text("ExploraTec se distribuye como está de manera gratuita, se prohíbe su distribución y uso con fines de lucro.")
                    
                    Divider()

                    VStack(alignment: .leading, spacing: 8) {
                        Text("Tecnologías")
                            .font(.headline)
                        Text("SwiftUI · MapKit · GameplayKit")
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                    }
                }
                .padding()
                .frame(maxWidth: .infinity, alignment: .leading)
            }
            .navigationTitle("Créditos")
        }
    }
}

private struct CreditRow: View {
    let name: String
    let role: String

    var body: some View {
        VStack(alignment: .leading, spacing: 2) {
            Text(name)
                .font(.body)
            Text(role)
                .font(.caption)
                .foregroundStyle(.secondary)
        }
        .accessibilityElement(children: .combine)
    }
}

#Preview {
    CreditsView()
}
