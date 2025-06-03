# iOS App

This directory contains Swift source code for the Mindful Connect iOS application.

## MeditationTimer

`MeditationTimer` is a lightweight timer utility that automatically logs a meditation
session once the countdown finishes. The session data is passed to a `SessionLogger`
which can be adapted to persist the information locally or send it to the backend.

The timer publishes elapsed seconds using `Combine` so it can be easily bound to a
SwiftUI interface.
