CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS events (
    id BIGSERIAL,
    tenant_id TEXT NOT NULL,
    event_name TEXT NOT NULL,
    entity_id TEXT,
    attributes JSONB,
    event_time TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (id, event_time)
);

SELECT create_hypertable(
    'events',
    'event_time',
    if_not_exists => TRUE
);
