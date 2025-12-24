CREATE TABLE IF NOT EXISTS events
(
    tenant_id String,
    event_name String,
    entity_id String,
    attributes Map(String, String),
    event_time DateTime
)
ENGINE = MergeTree
PARTITION BY toDate(event_time)
ORDER BY (tenant_id, event_name, entity_id, event_time);

