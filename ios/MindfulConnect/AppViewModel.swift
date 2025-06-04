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
        Task {
            do {
                try await api.updateProfileVisibility(request, authToken: token)
                user?.visibility = isPublic ? "public" : "private"
            } catch {
                errorMessage = error.localizedDescription
            }
            isLoading = false
        }
    }

    public func loadMeditationTypes() {
        guard let token = authToken else { return }
        isLoading = true
        Task {
            do {
                let types = try await api.fetchMeditationTypes(authToken: token)
                meditationTypes = types
            } catch {
                errorMessage = error.localizedDescription
            }
            isLoading = false
        }
    }

    public func addMeditationType(name: String) {
        guard let token = authToken else { return }
        let request = CreateMeditationTypeRequest(name: name)
        isLoading = true
        Task {
            do {
                let type = try await api.createMeditationType(request, authToken: token)
                meditationTypes.append(type)
            } catch {
                errorMessage = error.localizedDescription
            }
            isLoading = false
        }
    }

    public func deleteMeditationType(id: String) {
        guard let token = authToken else { return }
        isLoading = true
        Task {
            do {
                try await api.deleteMeditationType(id: id, authToken: token)
                meditationTypes.removeAll { $0.id == id }
            } catch {
                errorMessage = error.localizedDescription
            }
            isLoading = false
        }
    }
}
