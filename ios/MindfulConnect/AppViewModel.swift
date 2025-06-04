import Foundation
import Combine

/// Holds global app state for authentication and user preferences.
public class AppViewModel: ObservableObject {
    @Published public private(set) var authToken: String?
    @Published public private(set) var user: UserProfile?
    @Published public var meditationTypes: [MeditationType] = []
    @Published public var isLoading: Bool = false
    @Published public var errorMessage: String?
    private var cancellables = Set<AnyCancellable>()

    private let api: APIClient

    public init(api: APIClient = APIClient()) {
        self.api = api
    }

    public var isLoggedIn: Bool { authToken != nil }

    public func socialLogin(provider: String, token: String) {
        let request = SocialLoginRequest(provider: provider, token: token)
        isLoading = true
        api.socialLogin(request)
            .sink(receiveCompletion: { [weak self] completion in
                guard let self = self else { return }
                self.isLoading = false
                if case .failure(let error) = completion {
                    self.errorMessage = error.localizedDescription
                }
            }, receiveValue: { [weak self] response in
                self?.authToken = response.authToken
                self?.user = response.user
            })
            .store(in: &cancellables)
    }

    public func updateVisibility(isPublic: Bool) {
        guard let token = authToken else { return }
        let request = ProfileVisibilityRequest(isPublic: isPublic)
        isLoading = true
        api.updateProfileVisibility(request, authToken: token)
            .sink(receiveCompletion: { [weak self] completion in
                guard let self = self else { return }
                self.isLoading = false
                if case .failure(let error) = completion {
                    self.errorMessage = error.localizedDescription
                }
            }, receiveValue: { [weak self] in
                self?.user?.visibility = isPublic ? "public" : "private"
            })
            .store(in: &cancellables)
    }

    public func loadMeditationTypes() {
        guard let token = authToken else { return }
        isLoading = true
        api.fetchMeditationTypes(authToken: token)
            .sink(receiveCompletion: { [weak self] completion in
                guard let self = self else { return }
                self.isLoading = false
                if case .failure(let error) = completion {
                    self.errorMessage = error.localizedDescription
                }
            }, receiveValue: { [weak self] types in
                self?.meditationTypes = types
            })
            .store(in: &cancellables)
    }

    public func addMeditationType(name: String) {
        guard let token = authToken else { return }
        let request = CreateMeditationTypeRequest(name: name)
        isLoading = true
        api.createMeditationType(request, authToken: token)
            .sink(receiveCompletion: { [weak self] completion in
                guard let self = self else { return }
                self.isLoading = false
                if case .failure(let error) = completion {
                    self.errorMessage = error.localizedDescription
                }
            }, receiveValue: { [weak self] type in
                self?.meditationTypes.append(type)
            })
            .store(in: &cancellables)
    }

    public func deleteMeditationType(id: String) {
        guard let token = authToken else { return }
        isLoading = true
        api.deleteMeditationType(id: id, authToken: token)
            .sink(receiveCompletion: { [weak self] completion in
                guard let self = self else { return }
                self.isLoading = false
                if case .failure(let error) = completion {
                    self.errorMessage = error.localizedDescription
                }
            }, receiveValue: { [weak self] in
                self?.meditationTypes.removeAll { $0.id == id }
            })
            .store(in: &cancellables)
    }
}
