import SwiftUI

struct ActivityFeedView: View {
    @State private var feedItems: [FeedItem] = []
    @State private var newMessage: String = ""
    @State private var targetUserId: Int = 0

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
                        if let item = try? await MockAPIClient.shared.sendComment(newMessage, from: 1, to: targetUserId) {
                            feedItems.insert(item, at: 0)
                            newMessage = ""
                        }
                    }
                }
                Button("Encourage") {
                    Task {
                        if let item = try? await MockAPIClient.shared.sendEncouragement(newMessage, from: 1, to: targetUserId) {
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
                if let items = try? await MockAPIClient.shared.fetchFeed() {
                    feedItems = items
                }
            }
        }
    }
}

#Preview {
    ActivityFeedView()
}

