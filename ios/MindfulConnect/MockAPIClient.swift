import Foundation
import Combine

/// Provides mocked API responses for development and previews.
public struct MockAPIClient {
    public init() {}

    public func socialLogin(_ request: SocialLoginRequest) -> AnyPublisher<SocialLoginResponse, Error> {
        let profile = UserProfile(
            id: UUID(),
            name: "Demo User",
            email: "demo@example.com",
            visibility: "public"
        )
        let response = SocialLoginResponse(user: profile, authToken: "mock-token")
        return Just(response)
            .setFailureType(to: Error.self)
            .eraseToAnyPublisher()
    }

    public func updateProfileVisibility(_ request: ProfileVisibilityRequest, authToken: String) -> AnyPublisher<ProfileVisibilityResponse, Error> {
        let profile = UserProfile(
            id: UUID(),
            name: "Demo User",
            email: "demo@example.com",
            visibility: request.visibility
        )
        let response = ProfileVisibilityResponse(user: profile)
        return Just(response)
            .setFailureType(to: Error.self)
            .eraseToAnyPublisher()
    }

    public func fetchMeditationTypes(authToken: String) -> AnyPublisher<[MeditationType], Error> {
        let types = [
            MeditationType(id: UUID(), name: "Breathing"),
            MeditationType(id: UUID(), name: "Walking")
        ]
        return Just(types)
            .setFailureType(to: Error.self)
            .eraseToAnyPublisher()
    }

    public func createMeditationType(_ request: CreateMeditationTypeRequest, authToken: String) -> AnyPublisher<MeditationType, Error> {
        let type = MeditationType(id: UUID(), name: request.name)
        return Just(type)
            .setFailureType(to: Error.self)
            .eraseToAnyPublisher()
    }

    public func updateMeditationType(id: UUID, request: UpdateMeditationTypeRequest, authToken: String) -> AnyPublisher<MeditationType, Error> {
        let type = MeditationType(id: id, name: request.name)
        return Just(type)
            .setFailureType(to: Error.self)
            .eraseToAnyPublisher()
    }

    public func deleteMeditationType(id: UUID, authToken: String) -> AnyPublisher<Void, Error> {
        return Just(())
            .setFailureType(to: Error.self)
            .eraseToAnyPublisher()
    }
}
