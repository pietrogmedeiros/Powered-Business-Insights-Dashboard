from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.analytics_service import AnalyticsService
from app.services.data_service import DataService
import logging

router = APIRouter()
analytics_service = AnalyticsService()
data_service = DataService()

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Business Insights API"}

@router.get("/dashboard/overview")
async def get_dashboard_overview():
    """Get high-level business metrics"""
    try:
        overview = await analytics_service.get_business_overview()
        return overview
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/forecast/sales")
async def get_sales_forecast(periods: int = 30):
    """Get sales forecasting results"""
    try:
        forecast = await analytics_service.generate_sales_forecast(periods)
        return forecast
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/segmentation/customers")
async def get_customer_segmentation():
    """Get customer segmentation analysis"""
    try:
        segmentation = await analytics_service.analyze_customer_segments()
        return segmentation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sentiment/analysis")
async def get_sentiment_analysis():
    """Get product review sentiment analysis"""
    try:
        sentiment = await analytics_service.analyze_sentiment()
        return sentiment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/churn/prediction")
async def get_churn_prediction():
    """Get customer churn predictions"""
    try:
        churn_analysis = await analytics_service.predict_churn()
        return churn_analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/retrain")
async def retrain_models(background_tasks: BackgroundTasks):
    """Trigger model retraining"""
    background_tasks.add_task(analytics_service.retrain_all_models)
    return {"message": "Model retraining initiated"}