import Foundation
import Combine

// MARK: - Async Mock API used by preview-only social features

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

    public func fetchFeed() async throws -> [FeedItem] { loadJSON("feed") }

    public func sendComment(_ text: String, from userId: Int, to targetUserId: Int) async throws -> FeedItem {
        FeedItem(id: Int.random(in: 100...999), userId: userId, itemType: "comment", message: text, timestamp: Date(), targetUserId: targetUserId)
    }

    public func sendEncouragement(_ text: String, from userId: Int, to targetUserId: Int) async throws -> FeedItem {
        FeedItem(id: Int.random(in: 100...999), userId: userId, itemType: "encouragement", message: text, timestamp: Date(), targetUserId: targetUserId)
    }

    public func fetchBadges(for userId: Int) async throws -> [Badge] { loadJSON("badges") }

    public func fetchPrivateChallenges(for userId: Int) async throws -> [Challenge] { loadJSON("private_challenges") }

    public func fetchAd() async throws -> Ad { loadJSON("ad") }
}

// MARK: - Real API client used by the app

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
        return request("auth/social-login", method: "POST", body: data)
    }

    // MARK: - Profile Visibility
    public func updateProfileVisibility(_ requestBody: ProfileVisibilityRequest,
                                        authToken: String) -> AnyPublisher<Void, Error> {
        let data = try? JSONEncoder().encode(requestBody)
        return requestData("users/me/profile-visibility", method: "PUT", body: data, authToken: authToken)
            .map { _ in () }
            .eraseToAnyPublisher()
    }

    // MARK: - Custom Meditation Types
    public func fetchMeditationTypes(authToken: String) -> AnyPublisher<[MeditationType], Error> {
        request("users/me/custom-meditation-types", authToken: authToken)
    }

    public func createMeditationType(_ requestBody: CreateMeditationTypeRequest,
                                     authToken: String) -> AnyPublisher<MeditationType, Error> {
        let data = try? JSONEncoder().encode(requestBody)
        return request("users/me/custom-meditation-types", method: "POST", body: data, authToken: authToken)
    }

    public func updateMeditationType(id: String,
                                     requestBody: UpdateMeditationTypeRequest,
                                     authToken: String) -> AnyPublisher<Void, Error> {
        let data = try? JSONEncoder().encode(requestBody)
        let endpoint = "users/me/custom-meditation-types/\(id)"
        return requestData(endpoint, method: "PUT", body: data, authToken: authToken)
            .map { _ in () }
            .eraseToAnyPublisher()
    }

    public func deleteMeditationType(id: String, authToken: String) -> AnyPublisher<Void, Error> {
        let endpoint = "users/me/custom-meditation-types/\(id)"
        return requestData(endpoint, method: "DELETE", authToken: authToken)
            .map { _ in () }
            .eraseToAnyPublisher()
    }


    // MARK: - Analytics

    public func fetchConsistency(authToken: String) -> AnyPublisher<ConsistencyDataResponse, Error> {
        request("analytics/me/consistency", authToken: authToken)
    }

    public func fetchMoodCorrelation(authToken: String) -> AnyPublisher<MoodCorrelationResponse, Error> {
        request("analytics/me/mood-correlation", authToken: authToken)
    }

    public func fetchTimeOfDay(authToken: String) -> AnyPublisher<TimeOfDayResponse, Error> {
        request("analytics/me/time-of-day", authToken: authToken)
    }

    public func fetchLocationFrequency(authToken: String) -> AnyPublisher<LocationFrequencyResponse, Error> {
        request("analytics/me/location-frequency", authToken: authToken)

    // MARK: - Activity Feed
    public func fetchFeed(authToken: String) async throws -> [FeedItem] {
        var request = URLRequest(url: baseURL.appendingPathComponent("feed"))
        request.setValue("Bearer \(authToken)", forHTTPHeaderField: "Authorization")
        let (data, _) = try await session.data(for: request)
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        return try decoder.decode([FeedItem].self, from: data)
    }

    public func addFeedComment(feedItemId: Int, text: String, authToken: String) async throws -> FeedInteractionResponse {
        let endpoint = "feed/\(feedItemId)/comment"
        var request = URLRequest(url: baseURL.appendingPathComponent(endpoint))
        request.httpMethod = "POST"
        let body = CommentInput(feedItemId: feedItemId, text: text)
        request.httpBody = try JSONEncoder().encode(body)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer \(authToken)", forHTTPHeaderField: "Authorization")
        let (data, _) = try await session.data(for: request)
        return try JSONDecoder().decode(FeedInteractionResponse.self, from: data)
    }

    public func addFeedEncouragement(feedItemId: Int, text: String, authToken: String) async throws -> FeedInteractionResponse {
        let endpoint = "feed/\(feedItemId)/encourage"
        var request = URLRequest(url: baseURL.appendingPathComponent(endpoint))
        request.httpMethod = "POST"
        let body = EncouragementInput(feedItemId: feedItemId, text: text)
        request.httpBody = try JSONEncoder().encode(body)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer \(authToken)", forHTTPHeaderField: "Authorization")
        let (data, _) = try await session.data(for: request)
        return try JSONDecoder().decode(FeedInteractionResponse.self, from: data)
    }

    // MARK: - Badges
    public func fetchBadges(authToken: String) async throws -> [Badge] {
        var request = URLRequest(url: baseURL.appendingPathComponent("users/me/badges"))
        request.setValue("Bearer \(authToken)", forHTTPHeaderField: "Authorization")
        let (data, _) = try await session.data(for: request)
        return try JSONDecoder().decode([Badge].self, from: data)
    }

    // MARK: - Private Challenges
    public func fetchPrivateChallenges(authToken: String) async throws -> [Challenge] {
        var request = URLRequest(url: baseURL.appendingPathComponent("users/me/private-challenges"))
        request.setValue("Bearer \(authToken)", forHTTPHeaderField: "Authorization")
        let (data, _) = try await session.data(for: request)
        return try JSONDecoder().decode([Challenge].self, from: data)
    }

    public func createPrivateChallenge(_ input: ChallengeInput, authToken: String) async throws -> Challenge {
        var request = URLRequest(url: baseURL.appendingPathComponent("users/me/private-challenges"))
        request.httpMethod = "POST"
        request.httpBody = try JSONEncoder().encode(input)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer \(authToken)", forHTTPHeaderField: "Authorization")
        let (data, _) = try await session.data(for: request)
        return try JSONDecoder().decode(Challenge.self, from: data)
    }

    public func updatePrivateChallenge(id: Int, input: ChallengeInput, authToken: String) async throws {
        let endpoint = "users/me/private-challenges/\(id)"
        var request = URLRequest(url: baseURL.appendingPathComponent(endpoint))
        request.httpMethod = "PUT"
        request.httpBody = try JSONEncoder().encode(input)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer \(authToken)", forHTTPHeaderField: "Authorization")
        _ = try await session.data(for: request)
    }

    public func deletePrivateChallenge(id: Int, authToken: String) async throws {
        let endpoint = "users/me/private-challenges/\(id)"
        var request = URLRequest(url: baseURL.appendingPathComponent(endpoint))
        request.httpMethod = "DELETE"
        request.setValue("Bearer \(authToken)", forHTTPHeaderField: "Authorization")
        _ = try await session.data(for: request)
    }

    // MARK: - Ads
    public func fetchAd() async throws -> Ad {
        let endpoint = "ads/random"
        let url = baseURL.appendingPathComponent(endpoint)
        let (data, response) = try await session.data(from: url)
        if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 204 {
            throw URLError(.badServerResponse)
        }
        return try JSONDecoder().decode(Ad.self, from: data)
    }

    // MARK: - Subscription
    public func getSubscription(authToken: String) async throws -> Subscription {
        var request = URLRequest(url: baseURL.appendingPathComponent("subscriptions/me"))
        request.setValue("Bearer \(authToken)", forHTTPHeaderField: "Authorization")
        let (data, _) = try await session.data(for: request)
        return try JSONDecoder().decode(Subscription.self, from: data)
    }

    // MARK: - Session Photo
    public func uploadSessionPhoto(sessionId: Int, photoData: Data, filename: String, authToken: String) async throws {
        let endpoint = "sessions/\(sessionId)/photo"
        var request = URLRequest(url: baseURL.appendingPathComponent(endpoint))
        request.httpMethod = "POST"
        request.httpBody = photoData
        request.setValue("image/jpeg", forHTTPHeaderField: "Content-Type")
        request.setValue(filename, forHTTPHeaderField: "X-Filename")
        request.setValue("Bearer \(authToken)", forHTTPHeaderField: "Authorization")
        _ = try await session.data(for: request)

    }
}

