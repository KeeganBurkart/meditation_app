import Foundation

public protocol Networking {
    func fetchFeed() async throws -> [FeedItem]
    func sendComment(_ text: String, from userId: Int, to targetUserId: Int) async throws -> FeedItem
    func sendEncouragement(_ text: String, from userId: Int, to targetUserId: Int) async throws -> FeedItem
    func fetchBadges(for userId: Int) async throws -> [Badge]
    func fetchPrivateChallenges(for userId: Int) async throws -> [Challenge]
    func fetchAd() async throws -> Ad
}

public final class MockAPIClient: Networking {
    public static let shared = MockAPIClient()

    private let decoder: JSONDecoder

    public init() {
        decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
    }

    private func loadJSON<T: Decodable>(_ name: String) -> T {
#if SWIFT_PACKAGE
        let bundle = Bundle.module
#else
        let bundle = Bundle(for: MockAPIClient.self)
#endif
        guard let url = bundle.url(forResource: name, withExtension: "json") else {
            fatalError("Missing mock data \(name).json")
        }
        let data = try! Data(contentsOf: url)
        return try! decoder.decode(T.self, from: data)
    }

    public func fetchFeed() async throws -> [FeedItem] {
        loadJSON("feed")
    }

    public func sendComment(_ text: String, from userId: Int, to targetUserId: Int) async throws -> FeedItem {
        FeedItem(id: Int.random(in: 100...999), userId: userId, itemType: "comment", message: text, timestamp: Date(), targetUserId: targetUserId)
    }

    public func sendEncouragement(_ text: String, from userId: Int, to targetUserId: Int) async throws -> FeedItem {
        FeedItem(id: Int.random(in: 100...999), userId: userId, itemType: "encouragement", message: text, timestamp: Date(), targetUserId: targetUserId)
    }

    public func fetchBadges(for userId: Int) async throws -> [Badge] {
        loadJSON("badges")
    }

    public func fetchPrivateChallenges(for userId: Int) async throws -> [Challenge] {
        loadJSON("private_challenges")
    }

    public func fetchAd() async throws -> Ad {
        loadJSON("ad")
    }
}
