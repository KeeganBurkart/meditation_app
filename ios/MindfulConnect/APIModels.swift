import Foundation

public struct FeedItem: Codable {
    public let id: Int
    public let userId: Int
    public let itemType: String
    public let message: String
    public let timestamp: Date
    public let targetUserId: Int?
}

public struct Badge: Codable {
    public let name: String
    public let awardedAt: Date
}

public struct Challenge: Codable {
    public let id: Int
    public let name: String
    public let createdBy: Int
    public let isPrivate: Bool
    public let targetMinutes: Int?
    public let startDate: String?
    public let endDate: String?
}

public struct Ad: Codable {
    public let id: Int
    public let text: String
}
