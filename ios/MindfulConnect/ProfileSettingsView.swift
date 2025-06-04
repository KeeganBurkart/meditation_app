import SwiftUI

/// Allows the user to toggle their profile visibility between public and private.
struct ProfileSettingsView: View {
    @EnvironmentObject var viewModel: AppViewModel

    var body: some View {
        Form {
            Toggle(isOn: Binding(
                get: { viewModel.user?.visibility == "public" },
                set: { isPublic in
                    viewModel.updateVisibility(isPublic: isPublic)
                }
            )) {
                Text("Public Profile")
            }
        }
        .navigationTitle("Profile")
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

struct ProfileSettingsView_Previews: PreviewProvider {
    static var previews: some View {
        let vm = AppViewModel()
        vm.user = UserProfile(id: UUID(), name: "Demo", email: "demo@example.com", visibility: "public")
        return ProfileSettingsView().environmentObject(vm)
    }
}
