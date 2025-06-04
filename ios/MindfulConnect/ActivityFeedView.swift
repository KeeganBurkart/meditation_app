import SwiftUI

struct ActivityFeedView: View {
    @EnvironmentObject var viewModel: AppViewModel
    @State private var feedItems: [FeedItem] = []
    @State private var newMessage: String = ""
    @State private var targetUserId: Int = 0
    @State private var isLoading = false
    @State private var errorMessage: String?
    @State private var targetItemId: Int = 0
    private let api = APIClient()

    var body: some View {
        VStack {
            List(feedItems, id: \.id) { item in
                VStack(alignment: .leading) {
                    Text(item.message)
                        .font(.body)
                    if let target = item.targetUserId {
                        Text("-> User \(target)")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }
            }
            HStack {
                TextField("Say something", text: $newMessage)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                Button("Comment") {
                    Task {
                        isLoading = true
                        do {
                            let item = try await MockAPIClient.shared.sendComment(newMessage, from: 1, to: targetUserId)
                            feedItems.insert(item, at: 0)
                            newMessage = ""
                        } catch {
                            errorMessage = error.localizedDescription
                        }
                        isLoading = false
                    }
                }
                Button("Encourage") {
                    Task {
                        isLoading = true
                        do {
                            let item = try await MockAPIClient.shared.sendEncouragement(newMessage, from: 1, to: targetUserId)
                            feedItems.insert(item, at: 0)
                            newMessage = ""
                        } catch {
                            errorMessage = error.localizedDescription
                        }
                        isLoading = false
                    }
                }
            }
            .padding()
        }
        .onAppear {
            Task {
                isLoading = true
                do {
                    let items = try await MockAPIClient.shared.fetchFeed()
                    feedItems = items
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
    }
}

#Preview {
    ActivityFeedView()
}

