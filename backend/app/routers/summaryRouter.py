from fastapi import APIRouter, HTTPException

from app.services.yearInReviewInteractor import get_year_in_review

router = APIRouter(prefix="/summary", tags=["Summary"])


@router.get("/{user_id}/year/{year}", response_model=None)
def get_user_year_summary(user_id: str, year: int):
    try:
        summary = get_year_in_review(user_id, year)
        return summary.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")
