import Foundation
import Combine

public struct MeditationSession: Codable {
    public let duration: TimeInterval
    public let startDate: Date
    public let endDate: Date
}

public class SessionLogger {
    public init() {}

    public func log(session: MeditationSession) {
        // In a real application, this would persist to local storage or send to a backend.
        print("Logged session of \(session.duration) seconds")
    }
}

public class MeditationTimer: ObservableObject {
    @Published public private(set) var elapsed: TimeInterval = 0
    private let duration: TimeInterval
    private var timerCancellable: AnyCancellable?
    private let logger: SessionLogger
    private let startDate: Date

    public init(duration: TimeInterval, logger: SessionLogger = SessionLogger()) {
        self.duration = duration
        self.logger = logger
        self.startDate = Date()
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
        let session = MeditationSession(duration: duration, startDate: startDate, endDate: Date())
        logger.log(session: session)
    }
}
