"""
URL patterns for dashboard app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'dashboard'

# Create router for ViewSets
router = DefaultRouter()
router.register(r'widgets', views.DashboardWidgetViewSet, basename='widget')
router.register(r'health-metrics', views.UserHealthMetricsViewSet, basename='healthmetrics')
router.register(r'analytics', views.DashboardAnalyticsViewSet, basename='analytics')
router.register(r'goals', views.UserGoalViewSet, basename='goal')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Additional custom endpoints
    path('summary/', views.DashboardSummaryView.as_view(), name='summary'),
]
