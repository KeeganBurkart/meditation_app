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
        _ = api.fetchConsistency(authToken: authToken)
            .sink(receiveCompletion: { _ in }, receiveValue: { resp in
                consistency = resp.points
            })
        _ = api.fetchMoodCorrelation(authToken: authToken)
            .sink(receiveCompletion: { _ in }, receiveValue: { resp in
                mood = resp.points
            })
        _ = api.fetchTimeOfDay(authToken: authToken)
            .sink(receiveCompletion: { _ in }, receiveValue: { resp in
                timeOfDay = resp.points
            })
        _ = api.fetchLocationFrequency(authToken: authToken)
            .sink(receiveCompletion: { _ in }, receiveValue: { resp in
                locations = resp.points
            })
    }
}

#Preview {
    AnalyticsGraphsView(authToken: "token")
}
