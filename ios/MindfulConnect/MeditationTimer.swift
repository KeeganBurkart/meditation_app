import Foundation
import Combine

public struct MeditationSession: Codable {
    public let duration: TimeInterval
    public let startDate: Date
    public let endDate: Date
    public let photoURL: URL?
}

public class SessionLogger {
    private let storageURL: URL

    public init(storageURL: URL? = nil) {
        let documents = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!
        self.storageURL = storageURL ?? documents.appendingPathComponent("sessions.json")
    }

    public func log(session: MeditationSession) {
        do {
            var sessions: [MeditationSession] = []
            if let data = try? Data(contentsOf: storageURL) {
                sessions = try JSONDecoder().decode([MeditationSession].self, from: data)
            }
            sessions.append(session)
            let encoded = try JSONEncoder().encode(sessions)
            try encoded.write(to: storageURL, options: .atomic)
        } catch {
            print("Failed to log session: \(error)")
        }
    }

    public func uploadSessionPhoto(sessionId: Int, photoData: Data, filename: String, token: String) {
        guard let url = URL(string: "http://localhost:8000/sessions/\(sessionId)/photo") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        request.setValue(filename, forHTTPHeaderField: "X-Filename")
        URLSession.shared.uploadTask(with: request, from: photoData).resume()
    }
}

public class MeditationTimer: ObservableObject {
    @Published public private(set) var elapsed: TimeInterval = 0
    private let duration: TimeInterval
    private var timerCancellable: AnyCancellable?
    private let logger: SessionLogger
    private let startDate: Date
    private var photoURL: URL?
    public var attachedPhotoURL: URL? { photoURL }
    private let api = APIClient()

    public init(duration: TimeInterval, logger: SessionLogger = SessionLogger()) {
        self.duration = duration
        self.logger = logger
        self.startDate = Date()
    }

    public func attachPhoto(url: URL) {
        self.photoURL = url
    }

    public func start() {
        timerCancellable = Timer.publish(every: 1, on: .main, in: .common)
            .autoconnect()
            .sink { [weak self] _ in
                guard let self = self else { return }
                self.elapsed += 1
                if self.elapsed >= self.duration {
                    self.finishSession()
                }
            }
    }

    public func stop() {
        timerCancellable?.cancel()
        timerCancellable = nil
    }

    private func finishSession() {
        stop()
        let session = MeditationSession(duration: duration, startDate: startDate, endDate: Date(), photoURL: photoURL)
        logger.log(session: session)
    }

    public func uploadAttachedPhoto(sessionId: Int, authToken: String) async {
        guard let url = photoURL,
              let data = try? Data(contentsOf: url) else { return }
        try? await api.uploadSessionPhoto(sessionId: sessionId,
                                          photoData: data,
                                          filename: url.lastPathComponent,
                                          authToken: authToken)
    }
}
