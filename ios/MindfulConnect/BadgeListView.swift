import SwiftUI

struct BadgeListView: View {
    @EnvironmentObject var viewModel: AppViewModel
    @State private var badges: [Badge] = []
    private let api = APIClient()

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
                guard let token = viewModel.authToken else { return }
                if let items = try? await api.fetchBadges(authToken: token) {
                    badges = items
                }
            }
        }
    }
}

#Preview {
    BadgeListView()
}

