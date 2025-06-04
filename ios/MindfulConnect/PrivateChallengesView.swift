import SwiftUI

struct PrivateChallengesView: View {
    let isPremium: Bool
    @State private var challenges: [Challenge] = []

    var body: some View {
        Group {
            if isPremium {
                List(challenges, id: \.id) { challenge in
                    VStack(alignment: .leading) {
                        Text(challenge.name)
                            .font(.headline)
                        if let minutes = challenge.targetMinutes {
                            Text("Target: \(minutes) min")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                    }
                }
                .onAppear {
                    Task {
                        if let items = try? await MockAPIClient.shared.fetchPrivateChallenges(for: 1) {
                            challenges = items
                        }
                    }
                }
            } else {
                Text("Premium required to manage private challenges.")
                    .padding()
            }
        }
    }
}

#Preview {
    PrivateChallengesView(isPremium: true)
}

