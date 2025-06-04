import SwiftUI

struct ActivityFeedView: View {
    @EnvironmentObject var viewModel: AppViewModel
    @State private var feedItems: [FeedItem] = []
    @State private var newMessage: String = ""
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
                        guard let token = viewModel.authToken else { return }
                        if let item = try? await api.addFeedComment(feedItemId: targetItemId, text: newMessage, authToken: token) {
                            feedItems.insert(item, at: 0)
                            newMessage = ""
                        }
                    }
                }
                Button("Encourage") {
                    Task {
                        guard let token = viewModel.authToken else { return }
                        if let item = try? await api.addFeedEncouragement(feedItemId: targetItemId, text: newMessage, authToken: token) {
                            feedItems.insert(item, at: 0)
                            newMessage = ""
                        }
                    }
                }
            }
            .padding()
        }
        .onAppear {
            Task {
                guard let token = viewModel.authToken else { return }
                if let items = try? await api.fetchFeed(authToken: token) {
                    feedItems = items
                }
            }
        }
    }
}

#Preview {
    ActivityFeedView()
}

