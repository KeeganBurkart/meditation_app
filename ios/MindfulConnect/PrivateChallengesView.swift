import SwiftUI

struct PrivateChallengesView: View {
    @EnvironmentObject var viewModel: AppViewModel
    @State private var challenges: [Challenge] = []
    @State private var isPremium = false
    @State private var isLoading = false
    @State private var errorMessage: String?

    @State private var showForm = false
    @State private var editing: Challenge?
    @State private var formName = ""
    @State private var formMinutes = ""
    @State private var formStart = ""
    @State private var formEnd = ""

    private let api = APIClient()

    var body: some View {
        Group {
            if isPremium {
                List {
                    ForEach(challenges) { challenge in
                        VStack(alignment: .leading) {
                            Text(challenge.name)
                                .font(.headline)
                            if let minutes = challenge.targetMinutes {
                                Text("Target: \(minutes) min")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                        }
                        .swipeActions {
                            Button("Edit") { edit(challenge) }
                            Button(role: .destructive) {
                                Task { await delete(challenge) }
                            } label: {
                                Label("Delete", systemImage: "trash")
                            }
                        }
                    }
                }
                .toolbar {
                    Button("Add") { newChallenge() }
                }
                .onAppear { load() }
                .sheet(isPresented: $showForm) { formView }
                .overlay { if isLoading { ProgressView() } }
                .alert("Error", isPresented: Binding(get: { errorMessage != nil }, set: { _ in errorMessage = nil })) {
                    Button("OK", role: .cancel) {}
                } message: {
                    Text(errorMessage ?? "")
                }
            } else {
                Text("Premium required to manage private challenges.")
                    .padding()
            }
        }
    }

    private var formView: some View {
        NavigationView {
            Form {
                TextField("Name", text: $formName)
                TextField("Target Minutes", text: $formMinutes)
                    .keyboardType(.numberPad)
                TextField("Start Date (YYYY-MM-DD)", text: $formStart)
                TextField("End Date (YYYY-MM-DD)", text: $formEnd)
            }
            .navigationTitle(editing == nil ? "New Challenge" : "Edit Challenge")
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { showForm = false }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") { Task { await save() } }
                }
            }
        }
    }

    private func load() {
        guard let token = viewModel.authToken else { return }
        Task {
            isLoading = true
            do {
                let sub = try await api.getSubscription(authToken: token)
                isPremium = sub.tier == "premium"
                if isPremium {
                    challenges = try await api.fetchPrivateChallenges(authToken: token)
                }
            } catch {
                errorMessage = error.localizedDescription
            }
            isLoading = false
        }
    }

    private func newChallenge() {
        editing = nil
        formName = ""
        formMinutes = ""
        formStart = ""
        formEnd = ""
        showForm = true
    }

    private func edit(_ challenge: Challenge) {
        editing = challenge
        formName = challenge.name
        formMinutes = String(challenge.targetMinutes ?? 0)
        formStart = challenge.startDate ?? ""
        formEnd = challenge.endDate ?? ""
        showForm = true
    }

    private func save() async {
        guard let token = viewModel.authToken else { return }
        guard let minutes = Int(formMinutes) else { return }
        let input = ChallengeInput(name: formName, targetMinutes: minutes, startDate: formStart, endDate: formEnd, description: nil)
        isLoading = true
        do {
            if let editing = editing {
                try await api.updatePrivateChallenge(id: editing.id, input: input, authToken: token)
            } else {
                _ = try await api.createPrivateChallenge(input, authToken: token)
            }
            challenges = try await api.fetchPrivateChallenges(authToken: token)
            showForm = false
        } catch {
            errorMessage = error.localizedDescription
        }
        isLoading = false
    }

    private func delete(_ challenge: Challenge) async {
        guard let token = viewModel.authToken else { return }
        isLoading = true
        do {
            try await api.deletePrivateChallenge(id: challenge.id, authToken: token)
            challenges = try await api.fetchPrivateChallenges(authToken: token)
        } catch {
            errorMessage = error.localizedDescription
        }
        isLoading = false
    }
}

#Preview {
    PrivateChallengesView()
}

