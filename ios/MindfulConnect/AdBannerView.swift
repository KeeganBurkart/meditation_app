import SwiftUI

struct AdBannerView: View {
    let isPremium: Bool
    @State private var ad: Ad?
    private let api = APIClient()

    var body: some View {
        Group {
            if isPremium {
                EmptyView()
            } else {
                if let ad = ad {
                    Text(ad.text)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color.yellow.opacity(0.2))
                        .cornerRadius(8)
                } else {
                    Color.clear
                        .onAppear {
                            Task {
                                ad = try? await api.fetchAd()
                            }
                        }
                }
            }
        }
    }
}

#Preview {
    AdBannerView(isPremium: false)
}

