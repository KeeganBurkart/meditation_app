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

import Combine

/// Handles communication with the backend API for authentication,
/// profile settings and custom meditation types.
public struct APIClient {
    public var baseURL: URL
    public var session: URLSession

    public init(baseURL: URL = URL(string: "http://localhost:8000")!,
                session: URLSession = .shared) {
        self.baseURL = baseURL
        self.session = session
    }

    private func requestData(_ endpoint: String,
                             method: String = "GET",
                             body: Data? = nil,
                             authToken: String? = nil) -> AnyPublisher<Data, Error> {
        var urlRequest = URLRequest(url: baseURL.appendingPathComponent(endpoint))
        urlRequest.httpMethod = method
        urlRequest.httpBody = body
        urlRequest.setValue("application/json", forHTTPHeaderField: "Content-Type")
        if let token = authToken {
            urlRequest.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }

        return session.dataTaskPublisher(for: urlRequest)
            .map(\.data)
            .mapError { $0 as Error }
            .eraseToAnyPublisher()
    }

    private func request<T: Decodable>(_ endpoint: String,
                                       method: String = "GET",
                                       body: Data? = nil,
                                       authToken: String? = nil) -> AnyPublisher<T, Error> {
        requestData(endpoint, method: method, body: body, authToken: authToken)
            .decode(type: T.self, decoder: JSONDecoder())
            .eraseToAnyPublisher()
    }

    // MARK: - Social Login
    public func socialLogin(_ requestBody: SocialLoginRequest) -> AnyPublisher<SocialLoginResponse, Error> {
        let data = try? JSONEncoder().encode(requestBody)
        return request("auth/social", method: "POST", body: data)
    }

    // MARK: - Profile Visibility
    public func updateProfileVisibility(_ requestBody: ProfileVisibilityRequest,
                                        authToken: String) -> AnyPublisher<ProfileVisibilityResponse, Error> {
        let data = try? JSONEncoder().encode(requestBody)
        return request("profile/visibility", method: "PATCH", body: data, authToken: authToken)
    }

    // MARK: - Custom Meditation Types
    public func fetchMeditationTypes(authToken: String) -> AnyPublisher<[MeditationType], Error> {
        request("meditation_types", authToken: authToken)
    }

    public func createMeditationType(_ requestBody: CreateMeditationTypeRequest,
                                     authToken: String) -> AnyPublisher<MeditationType, Error> {
        let data = try? JSONEncoder().encode(requestBody)
        return request("meditation_types", method: "POST", body: data, authToken: authToken)
    }

    public func updateMeditationType(id: UUID,
                                     requestBody: UpdateMeditationTypeRequest,
                                     authToken: String) -> AnyPublisher<MeditationType, Error> {
        let data = try? JSONEncoder().encode(requestBody)
        let endpoint = "meditation_types/\(id.uuidString)"
        return request(endpoint, method: "PUT", body: data, authToken: authToken)
    }

    public func deleteMeditationType(id: UUID, authToken: String) -> AnyPublisher<Void, Error> {
        let endpoint = "meditation_types/\(id.uuidString)"
        return requestData(endpoint, method: "DELETE", authToken: authToken)
            .map { _ in () }
            .eraseToAnyPublisher()
    }
}
