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
    }
}

struct SocialLoginView_Previews: PreviewProvider {
    static var previews: some View {
        SocialLoginView().environmentObject(AppViewModel())
    }
}
