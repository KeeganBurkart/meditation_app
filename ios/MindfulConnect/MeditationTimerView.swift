import SwiftUI
import PhotosUI

struct MeditationTimerView: View {
    @EnvironmentObject var viewModel: AppViewModel
    @StateObject private var timer = MeditationTimer(duration: 60)
    @State private var pickerItem: PhotosPickerItem?
    @State private var image: Image?

    var body: some View {
        VStack(spacing: 16) {
            Text("Elapsed: \(Int(timer.elapsed))s")
                .font(.headline)

            if let image = image {
                image
                    .resizable()
                    .scaledToFit()
                    .frame(height: 150)
            }

            PhotosPicker(selection: $pickerItem, matching: .images) {
                Text("Select Photo")
            }
            .onChange(of: pickerItem) { newItem in
                guard let item = newItem else { return }
                Task {
                    if let data = try? await item.loadTransferable(type: Data.self) {
                        let url = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
                        try? data.write(to: url)
                        timer.attachPhoto(url: url)
                        if let uiImage = UIImage(data: data) {
                            image = Image(uiImage: uiImage)
                        }
                    }
                }
            }

            HStack {
                Button("Start") { timer.start() }
                Button("Stop") { timer.stop() }
            }
        }
        .padding()
    }
}

#Preview {
    MeditationTimerView().environmentObject(AppViewModel())
}
