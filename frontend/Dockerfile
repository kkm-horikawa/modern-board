# syntax=docker/dockerfile:1

# ==============================================================================
# Base stage: Set up Node.js environment
# ==============================================================================
FROM node:23-slim AS base

# Set environment variables
ENV NODE_ENV=production \
    PNPM_HOME=/pnpm \
    PATH="$PNPM_HOME:$PATH"

# Enable corepack for pnpm
RUN corepack enable

# Create non-root user with home directory
RUN groupadd -r vite && useradd -r -g vite -m -d /home/vite vite

# ==============================================================================
# Dependencies stage: Install dependencies
# ==============================================================================
FROM base AS deps

WORKDIR /app

# Copy package files
COPY package.json pnpm-lock.yaml* ./

# Install dependencies
RUN --mount=type=cache,id=pnpm,target=/pnpm/store \
    pnpm install --frozen-lockfile --prod=false

# ==============================================================================
# Builder stage: Build the application
# ==============================================================================
FROM base AS builder

WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules

# Copy application code
COPY . .

# Build the application
RUN pnpm run build

# ==============================================================================
# Development stage: For local development with hot-reload
# ==============================================================================
FROM base AS development

WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules

# Set ownership
RUN chown -R vite:vite /app /home/vite

# Switch to non-root user
USER vite

# Expose Vite dev server port
EXPOSE 5173

# Development server with HMR
CMD ["pnpm", "run", "dev", "--host", "0.0.0.0"]

# ==============================================================================
# Production stage: Serve built files with nginx
# ==============================================================================
FROM nginx:alpine AS production

# Copy custom nginx configuration
COPY <<'EOF' /etc/nginx/conf.d/default.conf
server {
    listen 5173;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # SPA routing fallback
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF

# Copy built files from builder
COPY --from=builder --chown=nginx:nginx /app/dist /usr/share/nginx/html

# Create non-root nginx user
RUN chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

# Switch to non-root user
USER nginx

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:5173/health || exit 1

# Expose port
EXPOSE 5173

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
