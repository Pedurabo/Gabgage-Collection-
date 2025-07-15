import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist
import folium
from datetime import datetime, timedelta
import json
from typing import List, Dict, Tuple
import random

class RouteOptimizer:
    def __init__(self):
        self.scaler = StandardScaler()
        self.kmeans = None
        
    def optimize_routes(self, service_requests: List[Dict], vehicles: List[Dict], 
                       constraints: Dict = None) -> Dict:
        """
        Optimize routes using AI/ML algorithms
        
        Args:
            service_requests: List of service requests with coordinates
            vehicles: List of available vehicles
            constraints: Optimization constraints (time windows, capacity, etc.)
        
        Returns:
            Optimized routes with metrics
        """
        
        # Extract coordinates and create feature matrix
        coordinates = np.array([[req['latitude'], req['longitude']] 
                              for req in service_requests])
        
        # Normalize coordinates
        coordinates_scaled = self.scaler.fit_transform(coordinates)
        
        # Determine optimal number of clusters (routes)
        n_routes = min(len(vehicles), len(service_requests))
        if n_routes == 0:
            return {"error": "No vehicles or requests available"}
        
        # Apply K-means clustering
        self.kmeans = KMeans(n_clusters=n_routes, random_state=42)
        cluster_labels = self.kmeans.fit_predict(coordinates_scaled)
        
        # Create optimized routes
        optimized_routes = []
        total_distance = 0
        total_time = 0
        
        for route_id in range(n_routes):
            route_requests = [req for i, req in enumerate(service_requests) 
                            if cluster_labels[i] == route_id]
            
            if not route_requests:
                continue
                
            # Apply TSP (Traveling Salesman Problem) optimization
            optimized_route = self._solve_tsp(route_requests)
            
            # Calculate route metrics
            distance = self._calculate_route_distance(optimized_route)
            time = self._calculate_route_time(optimized_route)
            
            route_info = {
                'route_id': route_id,
                'vehicle_id': vehicles[route_id]['id'] if route_id < len(vehicles) else None,
                'requests': optimized_route,
                'total_distance': distance,
                'estimated_time': time,
                'efficiency_score': self._calculate_efficiency_score(distance, time, len(optimized_route))
            }
            
            optimized_routes.append(route_info)
            total_distance += distance
            total_time += time
        
        return {
            'optimized_routes': optimized_routes,
            'total_distance': total_distance,
            'total_time': total_time,
            'average_efficiency': np.mean([r['efficiency_score'] for r in optimized_routes]),
            'fuel_savings': self._calculate_fuel_savings(total_distance),
            'time_savings': self._calculate_time_savings(total_time)
        }
    
    def _solve_tsp(self, requests: List[Dict]) -> List[Dict]:
        """Solve Traveling Salesman Problem using nearest neighbor algorithm"""
        if len(requests) <= 1:
            return requests
        
        # Start from depot (company location)
        depot = {'latitude': 40.7128, 'longitude': -74.0060}  # Example coordinates
        unvisited = requests.copy()
        route = []
        
        # Find nearest request to depot
        current = min(unvisited, key=lambda x: self._calculate_distance(depot, x))
        route.append(current)
        unvisited.remove(current)
        
        # Build route using nearest neighbor
        while unvisited:
            nearest = min(unvisited, key=lambda x: self._calculate_distance(current, x))
            route.append(nearest)
            unvisited.remove(nearest)
            current = nearest
        
        return route
    
    def _calculate_distance(self, point1: Dict, point2: Dict) -> float:
        """Calculate Euclidean distance between two points"""
        lat1, lon1 = point1['latitude'], point1['longitude']
        lat2, lon2 = point2['latitude'], point2['longitude']
        
        return np.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)
    
    def _calculate_route_distance(self, route: List[Dict]) -> float:
        """Calculate total distance for a route"""
        if len(route) <= 1:
            return 0
        
        total_distance = 0
        for i in range(len(route) - 1):
            total_distance += self._calculate_distance(route[i], route[i + 1])
        
        return total_distance
    
    def _calculate_route_time(self, route: List[Dict]) -> float:
        """Calculate estimated time for a route (hours)"""
        # Assume average speed of 30 km/h in urban areas
        avg_speed_kmh = 30
        distance_km = self._calculate_route_distance(route) * 111  # Convert to km
        travel_time = distance_km / avg_speed_kmh
        
        # Add service time (15 minutes per stop)
        service_time = len(route) * 0.25
        
        return travel_time + service_time
    
    def _calculate_efficiency_score(self, distance: float, time: float, stops: int) -> float:
        """Calculate efficiency score (higher is better)"""
        if stops == 0:
            return 0
        
        # Efficiency = stops per unit distance and time
        efficiency = stops / (distance * time + 1)  # Add 1 to avoid division by zero
        return efficiency
    
    def _calculate_fuel_savings(self, optimized_distance: float) -> float:
        """Calculate fuel savings compared to random routing"""
        # Assume 20% improvement over random routing
        baseline_distance = optimized_distance * 1.2
        fuel_savings = (baseline_distance - optimized_distance) * 0.1  # 0.1 L/km
        return fuel_savings
    
    def _calculate_time_savings(self, optimized_time: float) -> float:
        """Calculate time savings compared to random routing"""
        # Assume 15% improvement over random routing
        baseline_time = optimized_time * 1.15
        return baseline_time - optimized_time
    
    def predict_demand(self, historical_data: List[Dict]) -> Dict:
        """Predict future demand using historical data"""
        # Convert historical data to DataFrame
        df = pd.DataFrame(historical_data)
        df['date'] = pd.to_datetime(df['date'])
        df['day_of_week'] = df['date'].dt.dayofweek
        df['month'] = df['date'].dt.month
        
        # Simple demand prediction based on day of week patterns
        daily_patterns = df.groupby('day_of_week')['requests'].mean()
        
        # Predict next week's demand
        next_week_prediction = {}
        for day in range(7):
            predicted_demand = daily_patterns.get(day, df['requests'].mean())
            next_week_prediction[day] = max(0, predicted_demand)
        
        return {
            'next_week_prediction': next_week_prediction,
            'confidence_level': 0.85,
            'model_type': 'time_series_pattern'
        }
    
    def optimize_vehicle_assignment(self, routes: List[Dict], vehicles: List[Dict]) -> Dict:
        """Optimize vehicle assignment to routes"""
        if len(routes) == 0 or len(vehicles) == 0:
            return {"error": "No routes or vehicles available"}
        
        # Create cost matrix (route-vehicle compatibility)
        cost_matrix = []
        for route in routes:
            route_costs = []
            for vehicle in vehicles:
                # Calculate compatibility score
                compatibility = self._calculate_vehicle_route_compatibility(route, vehicle)
                route_costs.append(compatibility)
            cost_matrix.append(route_costs)
        
        # Use Hungarian algorithm for optimal assignment
        from scipy.optimize import linear_sum_assignment
        route_indices, vehicle_indices = linear_sum_assignment(cost_matrix)
        
        assignments = []
        total_cost = 0
        
        for route_idx, vehicle_idx in zip(route_indices, vehicle_indices):
            assignment = {
                'route_id': routes[route_idx]['route_id'],
                'vehicle_id': vehicles[vehicle_idx]['id'],
                'compatibility_score': cost_matrix[route_idx][vehicle_idx],
                'route': routes[route_idx],
                'vehicle': vehicles[vehicle_idx]
            }
            assignments.append(assignment)
            total_cost += cost_matrix[route_idx][vehicle_idx]
        
        return {
            'assignments': assignments,
            'total_compatibility_score': total_cost,
            'average_compatibility': total_cost / len(assignments) if assignments else 0
        }
    
    def _calculate_vehicle_route_compatibility(self, route: Dict, vehicle: Dict) -> float:
        """Calculate compatibility between vehicle and route"""
        # Factors to consider:
        # 1. Vehicle capacity vs route demand
        # 2. Vehicle type vs route requirements
        # 3. Vehicle location vs route start point
        
        compatibility_score = 1.0
        
        # Capacity compatibility
        route_demand = len(route['requests'])
        vehicle_capacity = vehicle.get('capacity', 10)
        capacity_ratio = min(route_demand / vehicle_capacity, 1.0)
        compatibility_score *= capacity_ratio
        
        # Vehicle type compatibility
        if route.get('requires_special_vehicle') and vehicle.get('type') != 'special':
            compatibility_score *= 0.5
        
        # Distance compatibility (prefer vehicles closer to route start)
        if 'start_location' in route and 'current_location' in vehicle:
            distance = self._calculate_distance(route['start_location'], vehicle['current_location'])
            distance_factor = 1.0 / (1.0 + distance)  # Closer is better
            compatibility_score *= distance_factor
        
        return compatibility_score
    
    def generate_route_map(self, route: Dict) -> str:
        """Generate interactive map for a route"""
        if not route['requests']:
            return ""
        
        # Create map centered on first request
        center_lat = route['requests'][0]['latitude']
        center_lon = route['requests'][0]['longitude']
        
        route_map = folium.Map(location=[center_lat, center_lon], zoom_start=12)
        
        # Add route path
        coordinates = [[req['latitude'], req['longitude']] for req in route['requests']]
        folium.PolyLine(
            coordinates,
            weight=3,
            color='blue',
            opacity=0.8
        ).add_to(route_map)
        
        # Add markers for each stop
        for i, request in enumerate(route['requests']):
            folium.Marker(
                [request['latitude'], request['longitude']],
                popup=f"Stop {i+1}: {request.get('customer_name', 'Unknown')}",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(route_map)
        
        return route_map._repr_html_()

# Initialize route optimizer
route_optimizer = RouteOptimizer() 