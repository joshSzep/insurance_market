from ninja import Router

router = Router()


@router.get("/health")
def health_check(request) -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
