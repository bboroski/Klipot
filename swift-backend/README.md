# Klipot Server-Side Swift backend

Swift 6 / Vapor service boundary, isolated from existing project components. Run: `cd swift-backend && swift test && swift run klipot-server`.

Configuration: `HOST`, `PORT`, `SERVICE_NAME`, `SERVICE_VERSION`. Secrets must be supplied by a deployment secret provider, never source constants.

Endpoints: `GET /health`, `GET /ready`, `GET /v1/health`. Readiness currently checks process readiness only. Responses propagate `X-Trace-ID`.

Core contracts include immutable Sendable request context, validated Codable config, API error DTO, async repository protocol and trace/security-header middleware. Use bounded DB pools, parameterized SQL and service-level transaction boundaries; never block SwiftNIO event loops.

PostgreSQL/Redis, JWT/RBAC, TLS, OpenTelemetry, Prometheus, migrations, rate limiting, OpenAPI, load tests and Kubernetes are production gates, not claimed as implemented.
