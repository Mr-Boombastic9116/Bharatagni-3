# ==============================================================================
# BharatAgri Iteration 3 - Multi-Stage Production Dockerfile
# Serves the FastAPI Backend + Vite React SPA in a single unified Render service
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Build Frontend Assets
# ------------------------------------------------------------------------------
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Install dependencies with lockfile reproducibility
COPY frontend/package*.json ./
RUN npm ci || npm install

# Copy source and build production bundle
COPY frontend/ ./
RUN npm run build

# ------------------------------------------------------------------------------
# Stage 2: Production Python Runtime
# ------------------------------------------------------------------------------
FROM python:3.12-slim AS runner

# Install essential system runtime libraries (OpenMP for XGBoost/sklearn)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application backend, ML models, and uploads
COPY backend/ ./backend/
COPY ml/ ./ml/
COPY uploads/ ./uploads/
COPY database/ ./database/

# Copy built frontend assets from Stage 1 into the runtime image
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Set Python module resolution path
ENV PYTHONPATH="/app"
ENV PORT=10000

# Expose standard web service port
EXPOSE 10000

# Healthcheck endpoint (read-only)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT}/api/health || exit 1

# Start Uvicorn bound to 0.0.0.0 and environment-supplied PORT
CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
