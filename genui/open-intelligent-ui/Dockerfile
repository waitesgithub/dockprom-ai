FROM node:24-alpine AS builder

ARG OPEN_INTELLIGENT_UI_REF=3b39c06b954e87c394ef95fee41a7e0084f94a27

WORKDIR /app
RUN apk add --no-cache git libc6-compat

RUN git clone https://github.com/thesysdev/open-intelligent-ui.git . \
    && git checkout "${OPEN_INTELLIGENT_UI_REF}"

# This upstream revision declares compatible version ranges that currently
# resolve to newer, API-incompatible OpenUI packages. Pin the tested set so
# reproducible builds retain the Ollama adapter APIs used by this revision.
RUN npm pkg set \
    "dependencies.@openuidev/react-ui=0.16.3" \
    "dependencies.@openuidev/react-headless=0.16.3" \
    "dependencies.zustand=4.5.5" \
    && npm install
RUN npm run build
RUN rm -rf .git && npm prune --omit=dev

FROM node:24-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000
ENV HOSTNAME=0.0.0.0

COPY --from=builder /app ./

EXPOSE 3000

CMD ["npm", "run", "start"]
