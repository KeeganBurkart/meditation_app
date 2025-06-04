import Foundation
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
