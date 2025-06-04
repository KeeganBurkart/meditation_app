import SwiftUI

struct PrivateChallengesView: View {
    @EnvironmentObject var viewModel: AppViewModel
    @State private var challenges: [Challenge] = []
    @State private var isLoading = false
    @State private var errorMessage: String?

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
                        isLoading = true
                        do {
                            challenges = try await MockAPIClient.shared.fetchPrivateChallenges(for: 1)
                        } catch {
                            errorMessage = error.localizedDescription
                        }
                        isLoading = false
                    }
                }
                .overlay {
                    if isLoading { ProgressView() }
                }
                .alert("Error", isPresented: Binding(get: { errorMessage != nil }, set: { _ in errorMessage = nil })) {
                    Button("OK", role: .cancel) {}
                } message: {
                    Text(errorMessage ?? "")
                }
            } else {
                Text("Premium required to manage private challenges.")
                    .padding()
            }
        }
    }
}

#Preview {
    PrivateChallengesView()
}

