import SwiftUI

/// Root view that switches between login and main content based on auth state.
struct ContentView: View {
    @EnvironmentObject var viewModel: AppViewModel

    var body: some View {
        NavigationView {
            if viewModel.isLoggedIn {
                List {
                    NavigationLink("Profile Settings") {
                        ProfileSettingsView()
                    }
                    NavigationLink("Meditation Types") {
                        MeditationTypesView()
                    }
                }
                .navigationTitle("Mindful Connect")
            } else {
                SocialLoginView()
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView().environmentObject(AppViewModel())
    }
}
