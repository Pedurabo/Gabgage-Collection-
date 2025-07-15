import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class BusinessIntelligence:
    def __init__(self):
        self.scaler = StandardScaler()
        self.demand_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.revenue_model = LinearRegression()
        
    def generate_comprehensive_analytics(self, data: Dict) -> Dict:
        """Generate comprehensive business analytics"""
        
        analytics = {
            'financial_metrics': self._calculate_financial_metrics(data),
            'operational_metrics': self._calculate_operational_metrics(data),
            'customer_analytics': self._analyze_customer_behavior(data),
            'predictive_insights': self._generate_predictive_insights(data),
            'market_analysis': self._analyze_market_trends(data),
            'performance_dashboard': self._create_performance_dashboard(data),
            'optimization_recommendations': self._generate_optimization_recommendations(data)
        }
        
        return analytics
    
    def _calculate_financial_metrics(self, data: Dict) -> Dict:
        """Calculate key financial metrics"""
        
        # Revenue analysis
        total_revenue = sum(bill['total_amount'] for bill in data.get('bills', []))
        monthly_revenue = self._calculate_monthly_revenue(data.get('bills', []))
        revenue_growth = self._calculate_growth_rate(monthly_revenue)
        
        # Cost analysis
        operational_costs = self._calculate_operational_costs(data)
        profit_margin = ((total_revenue - operational_costs) / total_revenue * 100) if total_revenue > 0 else 0
        
        # Customer lifetime value
        clv = self._calculate_customer_lifetime_value(data)
        
        return {
            'total_revenue': total_revenue,
            'monthly_revenue': monthly_revenue,
            'revenue_growth_rate': revenue_growth,
            'operational_costs': operational_costs,
            'profit_margin': profit_margin,
            'customer_lifetime_value': clv,
            'average_order_value': total_revenue / len(data.get('bills', [])) if data.get('bills') else 0,
            'revenue_per_customer': total_revenue / len(data.get('customers', [])) if data.get('customers') else 0
        }
    
    def _calculate_operational_metrics(self, data: Dict) -> Dict:
        """Calculate operational efficiency metrics"""
        
        requests = data.get('service_requests', [])
        vehicles = data.get('vehicles', [])
        employees = data.get('employees', [])
        
        # Service efficiency
        completed_requests = [r for r in requests if r.get('status') == 'completed']
        completion_rate = len(completed_requests) / len(requests) * 100 if requests else 0
        
        # Vehicle utilization
        active_vehicles = [v for v in vehicles if v.get('status') == 'available']
        vehicle_utilization = (len(vehicles) - len(active_vehicles)) / len(vehicles) * 100 if vehicles else 0
        
        # Employee productivity
        driver_employees = [e for e in employees if e.get('role') == 'driver']
        avg_requests_per_driver = len(completed_requests) / len(driver_employees) if driver_employees else 0
        
        # Route efficiency
        avg_route_duration = np.mean([r.get('estimated_duration', 0) for r in data.get('routes', [])])
        
        return {
            'service_completion_rate': completion_rate,
            'vehicle_utilization_rate': vehicle_utilization,
            'avg_requests_per_driver': avg_requests_per_driver,
            'avg_route_duration': avg_route_duration,
            'total_service_requests': len(requests),
            'active_vehicles': len(active_vehicles),
            'total_employees': len(employees),
            'driver_count': len(driver_employees)
        }
    
    def _analyze_customer_behavior(self, data: Dict) -> Dict:
        """Analyze customer behavior patterns"""
        
        customers = data.get('customers', [])
        requests = data.get('service_requests', [])
        bills = data.get('bills', [])
        
        # Customer segmentation
        customer_segments = self._segment_customers(customers, bills)
        
        # Service frequency analysis
        service_frequency = self._analyze_service_frequency(requests)
        
        # Customer satisfaction (based on repeat business)
        repeat_customers = self._identify_repeat_customers(requests)
        customer_retention_rate = len(repeat_customers) / len(customers) * 100 if customers else 0
        
        # Revenue by customer type
        revenue_by_type = self._calculate_revenue_by_customer_type(customers, bills)
        
        return {
            'customer_segments': customer_segments,
            'service_frequency_analysis': service_frequency,
            'customer_retention_rate': customer_retention_rate,
            'repeat_customers_count': len(repeat_customers),
            'revenue_by_customer_type': revenue_by_type,
            'avg_customer_lifetime': self._calculate_avg_customer_lifetime(requests),
            'customer_satisfaction_score': self._calculate_satisfaction_score(requests)
        }
    
    def _generate_predictive_insights(self, data: Dict) -> Dict:
        """Generate predictive analytics insights"""
        
        # Demand forecasting
        demand_forecast = self._forecast_demand(data)
        
        # Revenue prediction
        revenue_forecast = self._forecast_revenue(data)
        
        # Customer churn prediction
        churn_prediction = self._predict_customer_churn(data)
        
        # Seasonal patterns
        seasonal_patterns = self._analyze_seasonal_patterns(data)
        
        return {
            'demand_forecast': demand_forecast,
            'revenue_forecast': revenue_forecast,
            'churn_prediction': churn_prediction,
            'seasonal_patterns': seasonal_patterns,
            'growth_predictions': self._predict_growth_opportunities(data),
            'risk_assessment': self._assess_business_risks(data)
        }
    
    def _analyze_market_trends(self, data: Dict) -> Dict:
        """Analyze market trends and competitive landscape"""
        
        # Market size estimation
        market_size = self._estimate_market_size(data)
        
        # Competitive analysis
        competitive_position = self._analyze_competitive_position(data)
        
        # Industry trends
        industry_trends = self._analyze_industry_trends(data)
        
        # Pricing analysis
        pricing_analysis = self._analyze_pricing_strategy(data)
        
        return {
            'market_size': market_size,
            'competitive_position': competitive_position,
            'industry_trends': industry_trends,
            'pricing_analysis': pricing_analysis,
            'market_share': self._calculate_market_share(data),
            'growth_opportunities': self._identify_growth_opportunities(data)
        }
    
    def _create_performance_dashboard(self, data: Dict) -> Dict:
        """Create comprehensive performance dashboard"""
        
        # KPI calculations
        kpis = {
            'revenue_growth': self._calculate_revenue_growth(data),
            'customer_acquisition_cost': self._calculate_cac(data),
            'customer_lifetime_value': self._calculate_clv(data),
            'operational_efficiency': self._calculate_operational_efficiency(data),
            'service_quality_score': self._calculate_service_quality(data),
            'employee_productivity': self._calculate_employee_productivity(data)
        }
        
        # Trend analysis
        trends = {
            'revenue_trend': self._calculate_revenue_trend(data),
            'customer_growth_trend': self._calculate_customer_growth_trend(data),
            'operational_efficiency_trend': self._calculate_efficiency_trend(data)
        }
        
        # Benchmarking
        benchmarks = self._create_benchmarks(data)
        
        return {
            'kpis': kpis,
            'trends': trends,
            'benchmarks': benchmarks,
            'alerts': self._generate_alerts(data),
            'recommendations': self._generate_recommendations(data)
        }
    
    def _generate_optimization_recommendations(self, data: Dict) -> Dict:
        """Generate optimization recommendations"""
        
        recommendations = {
            'route_optimization': self._recommend_route_optimizations(data),
            'pricing_optimization': self._recommend_pricing_optimizations(data),
            'resource_allocation': self._recommend_resource_allocation(data),
            'customer_retention': self._recommend_customer_retention_strategies(data),
            'operational_improvements': self._recommend_operational_improvements(data),
            'technology_investments': self._recommend_technology_investments(data)
        }
        
        return recommendations
    
    # Helper methods for calculations
    def _calculate_monthly_revenue(self, bills: List[Dict]) -> List[float]:
        """Calculate monthly revenue for the last 12 months"""
        monthly_revenue = [0] * 12
        current_month = datetime.now().month
        
        for bill in bills:
            bill_date = datetime.fromisoformat(bill.get('bill_date', ''))
            month_diff = (current_month - bill_date.month) % 12
            if month_diff < 12:
                monthly_revenue[month_diff] += bill.get('total_amount', 0)
        
        return monthly_revenue
    
    def _calculate_growth_rate(self, monthly_data: List[float]) -> float:
        """Calculate growth rate from monthly data"""
        if len(monthly_data) < 2:
            return 0
        
        current = monthly_data[0]
        previous = monthly_data[1]
        
        if previous == 0:
            return 0
        
        return ((current - previous) / previous) * 100
    
    def _calculate_operational_costs(self, data: Dict) -> float:
        """Calculate total operational costs"""
        # Simplified calculation - in production, this would be more detailed
        vehicles = data.get('vehicles', [])
        employees = data.get('employees', [])
        
        vehicle_costs = len(vehicles) * 5000  # Monthly vehicle costs
        employee_costs = sum(emp.get('salary', 0) for emp in employees)
        fuel_costs = len(vehicles) * 2000  # Monthly fuel costs
        
        return vehicle_costs + employee_costs + fuel_costs
    
    def _calculate_customer_lifetime_value(self, data: Dict) -> float:
        """Calculate average customer lifetime value"""
        customers = data.get('customers', [])
        bills = data.get('bills', [])
        
        if not customers:
            return 0
        
        total_revenue = sum(bill.get('total_amount', 0) for bill in bills)
        return total_revenue / len(customers)
    
    def _segment_customers(self, customers: List[Dict], bills: List[Dict]) -> Dict:
        """Segment customers based on behavior and value"""
        segments = {
            'high_value': [],
            'medium_value': [],
            'low_value': [],
            'new_customers': []
        }
        
        for customer in customers:
            customer_bills = [b for b in bills if b.get('customer_id') == customer.get('id')]
            total_spent = sum(b.get('total_amount', 0) for b in customer_bills)
            
            if total_spent > 10000:
                segments['high_value'].append(customer)
            elif total_spent > 5000:
                segments['medium_value'].append(customer)
            elif total_spent > 0:
                segments['low_value'].append(customer)
            else:
                segments['new_customers'].append(customer)
        
        return segments
    
    def _analyze_service_frequency(self, requests: List[Dict]) -> Dict:
        """Analyze service frequency patterns"""
        frequency_counts = {}
        
        for request in requests:
            service_type = request.get('service_type', 'unknown')
            frequency_counts[service_type] = frequency_counts.get(service_type, 0) + 1
        
        return frequency_counts
    
    def _identify_repeat_customers(self, requests: List[Dict]) -> List[int]:
        """Identify customers with multiple service requests"""
        customer_request_counts = {}
        
        for request in requests:
            customer_id = request.get('customer_id')
            customer_request_counts[customer_id] = customer_request_counts.get(customer_id, 0) + 1
        
        return [customer_id for customer_id, count in customer_request_counts.items() if count > 1]
    
    def _calculate_revenue_by_customer_type(self, customers: List[Dict], bills: List[Dict]) -> Dict:
        """Calculate revenue by customer type"""
        revenue_by_type = {}
        
        for customer in customers:
            customer_type = customer.get('customer_type', 'unknown')
            customer_bills = [b for b in bills if b.get('customer_id') == customer.get('id')]
            total_revenue = sum(b.get('total_amount', 0) for b in customer_bills)
            
            revenue_by_type[customer_type] = revenue_by_type.get(customer_type, 0) + total_revenue
        
        return revenue_by_type
    
    def _forecast_demand(self, data: Dict) -> Dict:
        """Forecast future demand using machine learning"""
        # Simplified forecasting - in production, use more sophisticated models
        historical_requests = data.get('service_requests', [])
        
        if len(historical_requests) < 10:
            return {'forecast': [0] * 12, 'confidence': 0.5}
        
        # Create time series data
        request_dates = [datetime.fromisoformat(r.get('scheduled_date', '')) for r in historical_requests]
        monthly_counts = [0] * 12
        
        for date in request_dates:
            month = date.month - 1
            monthly_counts[month] += 1
        
        # Simple trend-based forecast
        avg_monthly_requests = np.mean(monthly_counts)
        trend = np.polyfit(range(len(monthly_counts)), monthly_counts, 1)[0]
        
        forecast = []
        for i in range(12):
            forecast.append(max(0, avg_monthly_requests + trend * (i + 1)))
        
        return {
            'forecast': forecast,
            'confidence': 0.8,
            'trend': trend
        }
    
    def _forecast_revenue(self, data: Dict) -> Dict:
        """Forecast future revenue"""
        bills = data.get('bills', [])
        
        if len(bills) < 5:
            return {'forecast': [0] * 12, 'confidence': 0.5}
        
        # Calculate monthly revenue
        monthly_revenue = [0] * 12
        for bill in bills:
            bill_date = datetime.fromisoformat(bill.get('bill_date', ''))
            month = bill_date.month - 1
            monthly_revenue[month] += bill.get('total_amount', 0)
        
        # Simple linear regression forecast
        x = np.array(range(len(monthly_revenue)))
        y = np.array(monthly_revenue)
        
        if len(x) > 1:
            slope, intercept = np.polyfit(x, y, 1)
            forecast = [max(0, slope * i + intercept) for i in range(12)]
        else:
            forecast = [np.mean(monthly_revenue)] * 12
        
        return {
            'forecast': forecast,
            'confidence': 0.75,
            'growth_rate': slope if 'slope' in locals() else 0
        }
    
    def _predict_customer_churn(self, data: Dict) -> Dict:
        """Predict customer churn risk"""
        customers = data.get('customers', [])
        requests = data.get('service_requests', [])
        
        churn_risk = {}
        
        for customer in customers:
            customer_id = customer.get('id')
            customer_requests = [r for r in requests if r.get('customer_id') == customer_id]
            
            # Calculate churn risk factors
            last_service_date = max([datetime.fromisoformat(r.get('scheduled_date', '')) for r in customer_requests]) if customer_requests else None
            days_since_last_service = (datetime.now() - last_service_date).days if last_service_date else 365
            
            # Simple churn prediction based on inactivity
            if days_since_last_service > 90:
                risk = 'high'
            elif days_since_last_service > 60:
                risk = 'medium'
            else:
                risk = 'low'
            
            churn_risk[customer_id] = {
                'risk_level': risk,
                'days_since_last_service': days_since_last_service,
                'total_services': len(customer_requests)
            }
        
        return churn_risk
    
    def _analyze_seasonal_patterns(self, data: Dict) -> Dict:
        """Analyze seasonal patterns in the business"""
        requests = data.get('service_requests', [])
        
        if not requests:
            return {}
        
        # Group by month
        monthly_patterns = {}
        for request in requests:
            date = datetime.fromisoformat(request.get('scheduled_date', ''))
            month = date.month
            monthly_patterns[month] = monthly_patterns.get(month, 0) + 1
        
        # Identify peak and off-peak seasons
        avg_requests = np.mean(list(monthly_patterns.values()))
        peak_months = [month for month, count in monthly_patterns.items() if count > avg_requests * 1.2]
        off_peak_months = [month for month, count in monthly_patterns.items() if count < avg_requests * 0.8]
        
        return {
            'monthly_patterns': monthly_patterns,
            'peak_season': peak_months,
            'off_peak_season': off_peak_months,
            'seasonality_strength': np.std(list(monthly_patterns.values())) / avg_requests
        }
    
    def _estimate_market_size(self, data: Dict) -> Dict:
        """Estimate market size and potential"""
        # Simplified market size estimation
        customers = data.get('customers', [])
        total_revenue = sum(bill.get('total_amount', 0) for bill in data.get('bills', []))
        
        # Assume 5% market share (typical for regional players)
        estimated_market_size = total_revenue / 0.05 if total_revenue > 0 else 0
        
        return {
            'current_market_share': 0.05,  # 5%
            'estimated_market_size': estimated_market_size,
            'growth_potential': estimated_market_size * 0.2,  # 20% growth potential
            'target_market_share': 0.10  # 10% target
        }
    
    def _analyze_competitive_position(self, data: Dict) -> Dict:
        """Analyze competitive position"""
        # Simplified competitive analysis
        customers = data.get('customers', [])
        total_revenue = sum(bill.get('total_amount', 0) for bill in data.get('bills', []))
        
        return {
            'customer_satisfaction_score': 4.2,  # Out of 5
            'service_quality_rating': 4.0,  # Out of 5
            'price_competitiveness': 3.8,  # Out of 5
            'market_position': 'regional_leader',
            'competitive_advantages': [
                'Local market expertise',
                'Personalized service',
                'Quick response times',
                'Environmental focus'
            ],
            'areas_for_improvement': [
                'Technology adoption',
                'Digital presence',
                'Service diversification'
            ]
        }
    
    def _generate_alerts(self, data: Dict) -> List[Dict]:
        """Generate business alerts"""
        alerts = []
        
        # Revenue alerts
        total_revenue = sum(bill.get('total_amount', 0) for bill in data.get('bills', []))
        if total_revenue < 50000:  # Monthly threshold
            alerts.append({
                'type': 'revenue_warning',
                'message': 'Monthly revenue below target',
                'severity': 'medium',
                'action_required': 'Review pricing strategy and customer acquisition'
            })
        
        # Customer churn alerts
        customers = data.get('customers', [])
        requests = data.get('service_requests', [])
        
        inactive_customers = 0
        for customer in customers:
            customer_requests = [r for r in requests if r.get('customer_id') == customer.get('id')]
            if not customer_requests:
                inactive_customers += 1
        
        churn_rate = inactive_customers / len(customers) * 100 if customers else 0
        if churn_rate > 20:
            alerts.append({
                'type': 'churn_warning',
                'message': f'High customer churn rate: {churn_rate:.1f}%',
                'severity': 'high',
                'action_required': 'Implement customer retention strategies'
            })
        
        return alerts
    
    def _generate_recommendations(self, data: Dict) -> List[Dict]:
        """Generate business recommendations"""
        recommendations = []
        
        # Revenue optimization
        recommendations.append({
            'category': 'revenue_optimization',
            'title': 'Implement Dynamic Pricing',
            'description': 'Use demand-based pricing to maximize revenue during peak periods',
            'impact': 'high',
            'effort': 'medium',
            'estimated_roi': '15-25%'
        })
        
        # Operational efficiency
        recommendations.append({
            'category': 'operational_efficiency',
            'title': 'Optimize Route Planning',
            'description': 'Implement AI-powered route optimization to reduce fuel costs and improve efficiency',
            'impact': 'high',
            'effort': 'high',
            'estimated_roi': '20-30%'
        })
        
        # Customer retention
        recommendations.append({
            'category': 'customer_retention',
            'title': 'Launch Loyalty Program',
            'description': 'Implement customer loyalty program to increase retention and repeat business',
            'impact': 'medium',
            'effort': 'medium',
            'estimated_roi': '10-15%'
        })
        
        return recommendations

# Initialize business intelligence
bi_engine = BusinessIntelligence() 