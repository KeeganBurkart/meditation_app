import SwiftUI

/// Displays and manages custom meditation types for the authenticated user.
struct MeditationTypesView: View {
    @EnvironmentObject var viewModel: AppViewModel
    @State private var newTypeName: String = ""

    var body: some View {
        VStack {
            List {
                ForEach(viewModel.meditationTypes) { type in
                    Text(type.name)
                        .swipeActions {
                            Button(role: .destructive) {
                                viewModel.deleteMeditationType(id: type.id)
                            } label: {
                                Label("Delete", systemImage: "trash")
                            }
                        }
                }
            }

            HStack {
                TextField("New type name", text: $newTypeName)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                Button("Add") {
                    guard !newTypeName.isEmpty else { return }
                    viewModel.addMeditationType(name: newTypeName)
                    newTypeName = ""
                }
            }
            .padding()
        }
        .navigationTitle("Meditation Types")
        .onAppear { viewModel.loadMeditationTypes() }
        .overlay {
            if viewModel.isLoading { ProgressView() }
        }
        .alert("Error", isPresented: Binding(get: { viewModel.errorMessage != nil }, set: { _ in viewModel.errorMessage = nil })) {
            Button("OK", role: .cancel) {}
        } message: {
            Text(viewModel.errorMessage ?? "")
        }
    }
}

struct MeditationTypesView_Previews: PreviewProvider {
    static var previews: some View {
        let vm = AppViewModel()
        vm.authToken = "token"
        vm.meditationTypes = [
            MeditationType(id: UUID(), name: "Breathing"),
            MeditationType(id: UUID(), name: "Walking")
        ]
        return MeditationTypesView().environmentObject(vm)
    }
}
