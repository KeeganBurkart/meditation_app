import Foundation

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
