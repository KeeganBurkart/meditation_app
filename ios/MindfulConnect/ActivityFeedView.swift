import SwiftUI

struct ActivityFeedView: View {
    @EnvironmentObject var viewModel: AppViewModel
    @State private var feedItems: [FeedItem] = []
    @State private var newMessage: String = ""
    @State private var isLoading = false
    @State private var errorMessage: String?
    private let api = APIClient()

    var body: some View {
        VStack {
            List(feedItems, id: \.id) { item in
                VStack(alignment: .leading, spacing: 8) {
                    Text("\(item.userDisplayName): \(item.message)")
                        .font(.body)
                    if let target = item.targetUserId {
                        Text("-> User \(target)")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    HStack {
                        Button("Comment") {
                            Task { await postComment(for: item) }
                        }
                        Button("Encourage") {
                            Task { await postEncouragement(for: item) }
                        }
                    }
                }
            }
            TextField("Say something", text: $newMessage)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()
        }
        .onAppear {
            Task { await loadFeed() }
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

    private func loadFeed() async {
        guard let token = viewModel.authToken else { return }
        isLoading = true
        do {
            feedItems = try await api.fetchFeed(authToken: token)
        } catch {
            errorMessage = error.localizedDescription
        }
        isLoading = false
    }

    private func postComment(for item: FeedItem) async {
        guard !newMessage.isEmpty, let token = viewModel.authToken else { return }
        isLoading = true
        do {
            _ = try await api.addFeedComment(feedItemId: item.id, text: newMessage, authToken: token)
            newMessage = ""
            feedItems = try await api.fetchFeed(authToken: token)
        } catch {
            errorMessage = error.localizedDescription
        }
        isLoading = false
    }

    private func postEncouragement(for item: FeedItem) async {
        guard !newMessage.isEmpty, let token = viewModel.authToken else { return }
        isLoading = true
        do {
            _ = try await api.addFeedEncouragement(feedItemId: item.id, text: newMessage, authToken: token)
            newMessage = ""
            feedItems = try await api.fetchFeed(authToken: token)
        } catch {
            errorMessage = error.localizedDescription
        }
        isLoading = false
    }
}

#Preview {
    ActivityFeedView()
}

