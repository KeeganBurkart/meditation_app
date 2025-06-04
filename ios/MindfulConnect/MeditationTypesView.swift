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
