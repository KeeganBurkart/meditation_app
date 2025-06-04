import Foundation
import Combine

/// Holds global app state for authentication and user preferences.
public class AppViewModel: ObservableObject {
    @Published public private(set) var authToken: String?
    @Published public private(set) var user: UserProfile?
    @Published public var meditationTypes: [MeditationType] = []
    private var cancellables = Set<AnyCancellable>()

    private let api: APIClient

    public init(api: APIClient = APIClient()) {
        self.api = api
    }

    public var isLoggedIn: Bool { authToken != nil }

    public func socialLogin(provider: String, token: String) {
        let request = SocialLoginRequest(provider: provider, token: token)
        api.socialLogin(request)
            .sink(receiveCompletion: { _ in },
                  receiveValue: { [weak self] response in
                self?.authToken = response.authToken
                self?.user = response.user
            })
            .store(in: &cancellables)
    }

    public func updateVisibility(to visibility: String) {
        guard let token = authToken else { return }
        let request = ProfileVisibilityRequest(visibility: visibility)
        api.updateProfileVisibility(request, authToken: token)
            .sink(receiveCompletion: { _ in },
                  receiveValue: { [weak self] response in
                self?.user = response.user
            })
            .store(in: &cancellables)
    }

    public func loadMeditationTypes() {
        guard let token = authToken else { return }
        api.fetchMeditationTypes(authToken: token)
            .sink(receiveCompletion: { _ in }, receiveValue: { [weak self] types in
                self?.meditationTypes = types
            })
            .store(in: &cancellables)
    }

    public func addMeditationType(name: String) {
        guard let token = authToken else { return }
        let request = CreateMeditationTypeRequest(name: name)
        api.createMeditationType(request, authToken: token)
            .sink(receiveCompletion: { _ in }, receiveValue: { [weak self] type in
                self?.meditationTypes.append(type)
            })
            .store(in: &cancellables)
    }

    public func deleteMeditationType(id: UUID) {
        guard let token = authToken else { return }
        api.deleteMeditationType(id: id, authToken: token)
            .sink(receiveCompletion: { _ in }, receiveValue: { [weak self] in
                self?.meditationTypes.removeAll { $0.id == id }
            })
            .store(in: &cancellables)
    }
}
