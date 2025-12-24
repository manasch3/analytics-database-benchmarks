from dataclasses import dataclass
from typing import Optional


@dataclass
class Feature:
    tenant_id: str
    name: str
    description: str
    window_seconds: int
    ttl_seconds: int
    default: int
    type: str
    entity_type: Optional[str] = None


@dataclass
class Event:
    tenant_id: str
    feature_name: str
    entity_id: str
    timestamp: int
    event_id: Optional[str] = None


@dataclass
class CounterResult:
    tenant_id: str
    feature_name: str
    entity_id: str
    value: int
    is_fresh: bool
