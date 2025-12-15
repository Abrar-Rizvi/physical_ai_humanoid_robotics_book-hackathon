import asyncio
from datetime import datetime
from typing import Dict, Any
from .models.response_models import HealthStatus
from .clients.qdrant_client import qdrant_client, verify_collection_exists
from .clients.openai_client import openai_client
from .config import settings


async def check_qdrant_health() -> str:
    """
    Check Qdrant connection health
    """
    try:
        # Try to get the collection to verify connection
        qdrant_client.get_collection(settings.qdrant_collection_name)
        return "connected"
    except Exception as e:
        print(f"Qdrant health check failed: {str(e)}")
        return "disconnected"


async def check_openai_health() -> str:
    """
    Check OpenAI connection health by making a simple API call
    """
    try:
        # Make a simple API call to verify connection
        response = openai_client.models.list()
        if response.data:
            return "connected"
        return "disconnected"
    except Exception as e:
        print(f"OpenAI health check failed: {str(e)}")
        return "disconnected"


async def get_health_status() -> HealthStatus:
    """
    Get comprehensive health status of the system
    """
    # Perform health checks concurrently
    qdrant_task = check_qdrant_health()
    openai_task = check_openai_health()

    qdrant_status, openai_status = await asyncio.gather(qdrant_task, openai_task)

    # Determine overall status
    overall_status = "healthy"
    if qdrant_status != "connected" or openai_status != "connected":
        overall_status = "degraded" if (qdrant_status == "connected" or openai_status == "connected") else "unhealthy"

    # Prepare services status
    services_status = {
        "qdrant": qdrant_status,
        "openai": openai_status
    }

    # Prepare metrics (placeholder for now)
    metrics = {
        "response_time_ms": 0,  # This would be calculated in a real implementation
        "uptime_seconds": 0     # This would track actual uptime
    }

    return HealthStatus(
        status=overall_status,
        timestamp=datetime.utcnow().isoformat() + "Z",
        services=services_status,
        metrics=metrics
    )