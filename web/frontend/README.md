# Web Frontend

This folder contains the React + TypeScript application built with Vite.

## Development

1. Install dependencies:
   ```bash
   npm install
   ```
2. Copy the example environment file and configure the API URL:
   ```bash
   cp .env.example .env
   # edit .env if your backend is not running on http://localhost:8000
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

The app will automatically reload when files are modified.

## Building for Production

```bash
npm run build
```

The compiled files are placed in `dist/` and can be served by any static host.

## Testing

Run unit tests with Vitest:

```bash
npm run test
```

Execute end-to-end tests using Cypress:

```bash
npm run e2e
```
