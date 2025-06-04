import SwiftUI

struct BadgeListView: View {
    @State private var badges: [Badge] = []

    var body: some View {
        List(badges, id: \.name) { badge in
            HStack {
                Image(systemName: "star.fill")
                    .foregroundColor(.yellow)
                VStack(alignment: .leading) {
                    Text(badge.name)
                    Text(badge.awardedAt, style: .date)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
        }
        .onAppear {
            Task {
                if let items = try? await MockAPIClient.shared.fetchBadges(for: 1) {
                    badges = items
                }
            }
        }
    }
}

#Preview {
    BadgeListView()
}

