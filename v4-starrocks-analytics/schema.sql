CREATE DATABASE IF NOT EXISTS analytics;
USE analytics;

CREATE TABLE IF NOT EXISTS events (
    tenant_id VARCHAR(20),
    event_name VARCHAR(20),
    entity_id VARCHAR(50),
    event_time DATETIME,
    attributes JSON
)
DUPLICATE KEY(tenant_id, event_name, entity_id, event_time)
DISTRIBUTED BY HASH(tenant_id) BUCKETS 8
PROPERTIES (
    "replication_num" = "1"
);
