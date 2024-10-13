FROM python:3.12.7 AS dependency
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv export --no-dev > requirements.lock \
    && uv export > requirements-dev.lock

FROM python:3.12.7 AS prod-builder
COPY --from=dependency /requirements.lock /requirements.lock
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system -r /requirements.lock

FROM python:3.12.7 AS dev-builder
COPY --from=dependency /requirements-dev.lock /requirements-dev.lock
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system -r /requirements-dev.lock

FROM python:3.12.7-slim AS runner-base

# Ref https://docs.docker.com/reference/dockerfile/#example-cache-apt-packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get -y upgrade \
    && apt-get -y install \
      # For PostgreSQL driver
      libpq5

WORKDIR /app

ENV USER=wsgi
RUN groupadd ${USER} \
    && useradd -g ${USER} ${USER}

USER ${USER}

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000

FROM runner-base AS dev
COPY --from=dev-builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=dev-builder /usr/local/bin /usr/local/bin

FROM runner-base AS prod
COPY --from=prod-builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=prod-builder /usr/local/bin /usr/local/bin

COPY --chown=${USER}:${USER} ./src/ /django/
