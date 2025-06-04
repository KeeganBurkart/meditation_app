# iOS App

This directory contains Swift source code for the Mindful Connect iOS application.

## MeditationTimer

`MeditationTimer` is a lightweight timer utility that automatically logs a meditation
session once the countdown finishes. The session data is passed to a `SessionLogger`
which can be adapted to persist the information locally or send it to the backend.

The timer publishes elapsed seconds using `Combine` so it can be easily bound to a
SwiftUI interface.

## UI Tests

UI tests are located under `MindfulConnectUITests`. They verify the timer interface by launching the app, tapping the **Start** button and waiting for the timer to finish.

To run the tests from the command line, use `xcodebuild` and specify a simulator destination:

```bash
xcodebuild test -project MindfulConnect.xcodeproj \
  -scheme MindfulConnect \
  -destination 'platform=iOS Simulator,name=iPhone 14,OS=latest'
```

The command builds the app and executes the `MindfulConnectUITests` target.

## Networking Layer

`APIClient` and the models in `APIModels.swift` provide mocked networking
endpoints used during development. `MockAPIClient` loads JSON from the
`MockResponses` directory to simulate backend calls for feed interactions,
badges, private challenges and advertisements.

## Mocked Social Features

`ActivityFeedView`, `BadgeListView`, `PrivateChallengesView` and `AdBannerView` provide placeholder SwiftUI interfaces for the new community functionality. They consume `MockAPIClient` to display feed comments, earned badges, premium challenges and in-app ads while real APIs are under development.

