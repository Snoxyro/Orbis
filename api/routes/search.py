import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_db
from services.rag_service import get_rag_service

router = APIRouter()


@router.get("/search")
async def search_courses(
    q: str,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    """
    Semantic search for courses with timing information
    
    Example: /search?q=programming with recursion&limit=3
    """
    total_start = time.perf_counter()
    timings = {}
    
    # Get RAG service
    service_start = time.perf_counter()
    rag_service = get_rag_service()
    timings["service_init"] = round((time.perf_counter() - service_start) * 1000, 2)
    
    # Perform search (includes embedding generation + vector search)
    search_start = time.perf_counter()
    results, search_timings = rag_service.search_courses(q, db, limit)
    timings["search_total"] = round((time.perf_counter() - search_start) * 1000, 2)
    
    # Merge detailed timings from service
    timings.update(search_timings)
    
    # Total time
    timings["total"] = round((time.perf_counter() - total_start) * 1000, 2)
    
    return {
        "query": q,
        "results": results,
        "count": len(results),
        "timings_ms": timings
    }
