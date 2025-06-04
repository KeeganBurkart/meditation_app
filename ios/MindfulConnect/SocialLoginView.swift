import SwiftUI

/// Simple UI allowing a user to perform a mocked social login.
struct SocialLoginView: View {
    @EnvironmentObject var viewModel: AppViewModel

    var body: some View {
        VStack(spacing: 16) {
            Text("Welcome to Mindful Connect")
                .font(.title)

            Button(action: {
                viewModel.socialLogin(provider: "google", token: "demo-token")
            }) {
                Text("Login with Google")
                    .padding()
                    .frame(maxWidth: .infinity)
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(8)
            }
        }
        .padding()
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

struct SocialLoginView_Previews: PreviewProvider {
    static var previews: some View {
        SocialLoginView().environmentObject(AppViewModel())
    }
}
