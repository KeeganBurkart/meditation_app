import SwiftUI
import Charts

struct AnalyticsGraphsView: View {
    @State private var consistency: [DateValuePoint] = []
    @State private var mood: [MoodCorrelationPoint] = []
    @State private var timeOfDay: [HourValuePoint] = []
    @State private var locations: [StringValuePoint] = []

    let api = APIClient()
    let authToken: String

    var body: some View {
        ScrollView {
            VStack(spacing: 32) {
                if !consistency.isEmpty {
                    Chart(consistency, id: \.dateStr) { point in
                        LineMark(
                            x: .value("Date", point.dateStr),
                            y: .value("Sessions", point.value)
                        )
                    }
                    .frame(height: 200)
                    .chartXAxisLabel("Date")
                    .chartYAxisLabel("Sessions")
                }

                if !mood.isEmpty {
                    Chart(mood, id: \.moodBefore) { point in
                        PointMark(
                            x: .value("Before", point.moodBefore),
                            y: .value("After", point.moodAfter)
                        )
                    }
                    .frame(height: 200)
                    .chartXAxisLabel("Mood Before")
                    .chartYAxisLabel("Mood After")
                }

                if !timeOfDay.isEmpty {
                    Chart(timeOfDay, id: \.hour) { point in
                        BarMark(
                            x: .value("Hour", point.hour),
                            y: .value("Sessions", point.value)
                        )
                    }
                    .frame(height: 200)
                }

                if !locations.isEmpty {
                    Chart(locations, id: \.name) { point in
                        BarMark(
                            x: .value("Location", point.name),
                            y: .value("Sessions", point.value)
                        )
                    }
                    .frame(height: 200)
                }
            }
            .padding()
        }
        .navigationTitle("Analytics")
        .onAppear {
            loadData()
        }
    }

    private func loadData() {
        Task {
            if let resp = try? await api.fetchConsistency(authToken: authToken) {
                consistency = resp.points
            }
            if let resp = try? await api.fetchMoodCorrelation(authToken: authToken) {
                mood = resp.points
            }
            if let resp = try? await api.fetchTimeOfDay(authToken: authToken) {
                timeOfDay = resp.points
            }
            if let resp = try? await api.fetchLocationFrequency(authToken: authToken) {
                locations = resp.points
            }
        }
    }
}

#Preview {
    AnalyticsGraphsView(authToken: "token")
}
