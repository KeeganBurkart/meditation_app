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

public struct SocialLoginRequest: Codable {
    public let provider: String
    public let token: String
}

public struct UserProfile: Codable {
    public let id: UUID
    public let name: String
    public let email: String
    public let visibility: String
}

public struct SocialLoginResponse: Codable {
    public let user: UserProfile
    public let authToken: String
}

public struct ProfileVisibilityRequest: Codable {
    public let visibility: String
}

public struct ProfileVisibilityResponse: Codable {
    public let user: UserProfile
}

public struct MeditationType: Codable, Identifiable {
    public let id: UUID
    public let name: String
}

public struct CreateMeditationTypeRequest: Codable {
    public let name: String
}

public struct UpdateMeditationTypeRequest: Codable {
    public let name: String
}
