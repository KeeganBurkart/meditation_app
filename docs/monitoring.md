# Monitoring and Feedback Strategy

This document outlines the initial plan for collecting application metrics,
tracking errors, and gathering feedback across all platforms.

## Backend

- **Logging**: Use Python's standard `logging` module. Logs are streamed to
  STDOUT in the Docker container and should be collected by the hosting
  provider (e.g. CloudWatch, Stackdriver) for retention and analysis.
- **Error Tracking**: Integrate Sentry using the official SDK to capture
  unhandled exceptions and provide alerting.
- **Performance**: Enable FastAPI middleware such as `PrometheusMiddleware` to
  expose metrics for request latency and throughput.

## Web Frontend

- **JavaScript Errors**: Include Sentry in the React app to report uncaught
  exceptions and failed network requests.
- **Performance Metrics**: Use the Web Vitals library to measure page load times
  and send the results to an analytics endpoint.
- **User Feedback**: Provide a small feedback form accessible from the footer
  that posts messages to the backend for review.

## iOS App

- **Crash Reporting**: Use Sentry's Swift SDK to automatically capture crashes
  and significant errors.
- **Usage Analytics**: Leverage the built in `monitoring.log_event` helper to
  log important user actions. Events should be batched and sent when the app is
  active on a network connection.
- **Performance**: Measure app launch time and key screen rendering durations
  with Apple's MetricKit where available.

## Dashboards and Alerts

All collected metrics and errors should be surfaced in Sentry and Prometheus
so the team can monitor trends over time. Critical alerts should page the on-
call engineer via the selected incident response tool.
