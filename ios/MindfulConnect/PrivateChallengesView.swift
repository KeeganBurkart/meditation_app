import SwiftUI

struct PrivateChallengesView: View {
    @EnvironmentObject var viewModel: AppViewModel
    @State private var challenges: [Challenge] = []
    @State private var isPremium: Bool = false
    private let api = APIClient()

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
            } else {
                Text("Premium required to manage private challenges.")
                    .padding()
            }
        }
        .onAppear {
            Task {
                guard let token = viewModel.authToken else { return }
                if let sub = try? await api.getSubscription(authToken: token) {
                    isPremium = sub.tier.lowercased() == "premium"
                    if isPremium {
                        if let items = try? await api.fetchPrivateChallenges(authToken: token) {
                            challenges = items
                        }
                    }
                }
            }
        }
    }
}

#Preview {
    PrivateChallengesView()
}

