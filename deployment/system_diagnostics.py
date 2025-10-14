#!/usr/bin/env python3
"""
System Diagnostics for D&D Character Art Generator
Provides comprehensive system analysis and optimization recommendations
"""

import os
import time
import psutil
import torch
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SystemInfo:
    """System information structure"""
    gpu_available: bool
    gpu_name: str
    gpu_memory_total: float
    gpu_memory_free: float
    gpu_memory_used: float
    cpu_count: int
    cpu_percent: float
    memory_total: float
    memory_available: float
    memory_percent: float
    disk_total: float
    disk_free: float
    disk_percent: float

@dataclass
class PerformanceMetrics:
    """Performance metrics structure"""
    generation_time: float
    memory_peak: float
    gpu_utilization: float
    cpu_utilization: float
    success_rate: float
    error_count: int

class SystemDiagnostics:
    """Comprehensive system diagnostics and optimization"""
    
    def __init__(self):
        self.system_info = self._get_system_info()
        self.performance_history = []
        self.optimization_cache = {}
    
    def _get_system_info(self) -> SystemInfo:
        """Get comprehensive system information"""
        # GPU information
        gpu_available = torch.cuda.is_available()
        gpu_name = "Unknown"
        gpu_memory_total = 0.0
        gpu_memory_free = 0.0
        gpu_memory_used = 0.0
        
        if gpu_available:
            gpu_name = torch.cuda.get_device_name()
            gpu_memory_total = torch.cuda.get_device_properties(0).total_memory / 1e9
            gpu_memory_used = torch.cuda.memory_allocated() / 1e9
            gpu_memory_free = gpu_memory_total - gpu_memory_used
        
        # CPU and memory information
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        # Disk information
        disk = psutil.disk_usage('/')
        
        return SystemInfo(
            gpu_available=gpu_available,
            gpu_name=gpu_name,
            gpu_memory_total=gpu_memory_total,
            gpu_memory_free=gpu_memory_free,
            gpu_memory_used=gpu_memory_used,
            cpu_count=cpu_count,
            cpu_percent=cpu_percent,
            memory_total=memory.total / 1e9,
            memory_available=memory.available / 1e9,
            memory_percent=memory.percent,
            disk_total=disk.total / 1e9,
            disk_free=disk.free / 1e9,
            disk_percent=(disk.used / disk.total) * 100
        )
    
    def analyze_system(self) -> Dict[str, Any]:
        """Comprehensive system analysis"""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "system_info": self._system_info_to_dict(),
            "performance_score": self._calculate_performance_score(),
            "recommended_settings": self._get_optimal_settings(),
            "optimization_suggestions": self._get_optimization_suggestions(),
            "health_status": self._get_health_status(),
            "resource_usage": self._get_resource_usage()
        }
        
        return analysis
    
    def _system_info_to_dict(self) -> Dict[str, Any]:
        """Convert system info to dictionary"""
        return {
            "gpu": {
                "available": self.system_info.gpu_available,
                "name": self.system_info.gpu_name,
                "memory_total_gb": round(self.system_info.gpu_memory_total, 2),
                "memory_free_gb": round(self.system_info.gpu_memory_free, 2),
                "memory_used_gb": round(self.system_info.gpu_memory_used, 2),
                "memory_usage_percent": round((self.system_info.gpu_memory_used / self.system_info.gpu_memory_total) * 100, 2) if self.system_info.gpu_memory_total > 0 else 0
            },
            "cpu": {
                "count": self.system_info.cpu_count,
                "usage_percent": round(self.system_info.cpu_percent, 2)
            },
            "memory": {
                "total_gb": round(self.system_info.memory_total, 2),
                "available_gb": round(self.system_info.memory_available, 2),
                "usage_percent": round(self.system_info.memory_percent, 2)
            },
            "disk": {
                "total_gb": round(self.system_info.disk_total, 2),
                "free_gb": round(self.system_info.disk_free, 2),
                "usage_percent": round(self.system_info.disk_percent, 2)
            }
        }
    
    def _calculate_performance_score(self) -> float:
        """Calculate overall system performance score (0-100)"""
        score = 0
        
        # GPU score (0-50 points)
        if self.system_info.gpu_available:
            score += 30  # Base GPU score
            vram_gb = self.system_info.gpu_memory_total
            if vram_gb >= 16:
                score += 20
            elif vram_gb >= 8:
                score += 15
            elif vram_gb >= 4:
                score += 10
            else:
                score += 5
        else:
            score += 10  # CPU only
        
        # Memory score (0-25 points)
        memory_percent = self.system_info.memory_percent
        if memory_percent < 50:
            score += 25
        elif memory_percent < 75:
            score += 20
        elif memory_percent < 90:
            score += 15
        else:
            score += 10
        
        # CPU score (0-15 points)
        cpu_percent = self.system_info.cpu_percent
        if cpu_percent < 50:
            score += 15
        elif cpu_percent < 75:
            score += 12
        elif cpu_percent < 90:
            score += 8
        else:
            score += 5
        
        # Disk score (0-10 points)
        disk_percent = self.system_info.disk_percent
        if disk_percent < 80:
            score += 10
        elif disk_percent < 90:
            score += 8
        else:
            score += 5
        
        return min(100, max(0, score))
    
    def _get_optimal_settings(self) -> Dict[str, Any]:
        """Get optimal settings based on system specs"""
        if self.system_info.gpu_available:
            vram_gb = self.system_info.gpu_memory_total
            
            if vram_gb >= 16:
                return {
                    "quality": "ultra",
                    "max_resolution": [1280, 1536],
                    "batch_size": 4,
                    "steps": 40,
                    "cfg": 6.5,
                    "enable_refiner": True,
                    "enable_controlnet": True
                }
            elif vram_gb >= 8:
                return {
                    "quality": "high",
                    "max_resolution": [1024, 1280],
                    "batch_size": 2,
                    "steps": 30,
                    "cfg": 6.5,
                    "enable_refiner": True,
                    "enable_controlnet": True
                }
            elif vram_gb >= 4:
                return {
                    "quality": "medium",
                    "max_resolution": [896, 1120],
                    "batch_size": 1,
                    "steps": 25,
                    "cfg": 6.0,
                    "enable_refiner": False,
                    "enable_controlnet": True
                }
            else:
                return {
                    "quality": "low",
                    "max_resolution": [640, 800],
                    "batch_size": 1,
                    "steps": 20,
                    "cfg": 5.5,
                    "enable_refiner": False,
                    "enable_controlnet": False
                }
        else:
            return {
                "quality": "low",
                "max_resolution": [640, 800],
                "batch_size": 1,
                "steps": 20,
                "cfg": 5.5,
                "enable_refiner": False,
                "enable_controlnet": False
            }
    
    def _get_optimization_suggestions(self) -> List[str]:
        """Get AI-powered optimization suggestions"""
        suggestions = []
        
        # GPU suggestions
        if not self.system_info.gpu_available:
            suggestions.append("🚨 No GPU detected - consider using Colab Pro for better performance")
        elif self.system_info.gpu_memory_total < 4:
            suggestions.append("⚠️ Low VRAM detected - reduce resolution and batch size")
        
        # Memory suggestions
        if self.system_info.memory_percent > 90:
            suggestions.append("🚨 High memory usage - close other applications")
        elif self.system_info.memory_percent > 75:
            suggestions.append("⚠️ Moderate memory usage - monitor for potential issues")
        
        # CPU suggestions
        if self.system_info.cpu_percent > 90:
            suggestions.append("🚨 High CPU usage - reduce concurrent operations")
        elif self.system_info.cpu_percent > 75:
            suggestions.append("⚠️ Moderate CPU usage - consider reducing quality settings")
        
        # Disk suggestions
        if self.system_info.disk_percent > 90:
            suggestions.append("🚨 Low disk space - free up storage")
        elif self.system_info.disk_percent > 80:
            suggestions.append("⚠️ Moderate disk usage - consider cleanup")
        
        # Performance-based suggestions
        performance_score = self._calculate_performance_score()
        if performance_score < 50:
            suggestions.append("🔧 Low performance score - consider upgrading hardware or using Colab Pro")
        elif performance_score < 75:
            suggestions.append("⚡ Moderate performance - optimize settings for better results")
        
        # GPU-specific optimizations
        if self.system_info.gpu_available:
            if self.system_info.gpu_memory_used / self.system_info.gpu_memory_total > 0.8:
                suggestions.append("🧹 High GPU memory usage - clear cache and reduce batch size")
            
            if "T4" in self.system_info.gpu_name:
                suggestions.append("💡 T4 GPU detected - use medium quality settings for optimal performance")
            elif "V100" in self.system_info.gpu_name:
                suggestions.append("🚀 V100 GPU detected - can handle high quality settings")
            elif "A100" in self.system_info.gpu_name:
                suggestions.append("🔥 A100 GPU detected - can handle ultra quality settings")
        
        return suggestions
    
    def _get_health_status(self) -> Dict[str, str]:
        """Get system health status"""
        status = {
            "overall": "healthy",
            "gpu": "healthy",
            "memory": "healthy",
            "cpu": "healthy",
            "disk": "healthy"
        }
        
        # GPU health
        if not self.system_info.gpu_available:
            status["gpu"] = "warning"
        elif self.system_info.gpu_memory_used / self.system_info.gpu_memory_total > 0.9:
            status["gpu"] = "critical"
        elif self.system_info.gpu_memory_used / self.system_info.gpu_memory_total > 0.8:
            status["gpu"] = "warning"
        
        # Memory health
        if self.system_info.memory_percent > 95:
            status["memory"] = "critical"
        elif self.system_info.memory_percent > 85:
            status["memory"] = "warning"
        
        # CPU health
        if self.system_info.cpu_percent > 95:
            status["cpu"] = "critical"
        elif self.system_info.cpu_percent > 85:
            status["cpu"] = "warning"
        
        # Disk health
        if self.system_info.disk_percent > 95:
            status["disk"] = "critical"
        elif self.system_info.disk_percent > 90:
            status["disk"] = "warning"
        
        # Overall health
        if any(status[key] == "critical" for key in ["gpu", "memory", "cpu", "disk"]):
            status["overall"] = "critical"
        elif any(status[key] == "warning" for key in ["gpu", "memory", "cpu", "disk"]):
            status["overall"] = "warning"
        
        return status
    
    def _get_resource_usage(self) -> Dict[str, Any]:
        """Get current resource usage"""
        return {
            "gpu_memory_usage": {
                "used_gb": round(self.system_info.gpu_memory_used, 2),
                "free_gb": round(self.system_info.gpu_memory_free, 2),
                "total_gb": round(self.system_info.gpu_memory_total, 2),
                "usage_percent": round((self.system_info.gpu_memory_used / self.system_info.gpu_memory_total) * 100, 2) if self.system_info.gpu_memory_total > 0 else 0
            },
            "system_memory_usage": {
                "used_gb": round(self.system_info.memory_total - self.system_info.memory_available, 2),
                "free_gb": round(self.system_info.memory_available, 2),
                "total_gb": round(self.system_info.memory_total, 2),
                "usage_percent": round(self.system_info.memory_percent, 2)
            },
            "cpu_usage": {
                "usage_percent": round(self.system_info.cpu_percent, 2),
                "core_count": self.system_info.cpu_count
            },
            "disk_usage": {
                "used_gb": round(self.system_info.disk_total - self.system_info.disk_free, 2),
                "free_gb": round(self.system_info.disk_free, 2),
                "total_gb": round(self.system_info.disk_total, 2),
                "usage_percent": round(self.system_info.disk_percent, 2)
            }
        }
    
    def monitor_performance(self, generation_time: float, memory_peak: float) -> Dict[str, Any]:
        """Monitor performance during generation"""
        metrics = PerformanceMetrics(
            generation_time=generation_time,
            memory_peak=memory_peak,
            gpu_utilization=self._get_gpu_utilization(),
            cpu_utilization=self.system_info.cpu_percent,
            success_rate=1.0,  # Would be calculated from history
            error_count=0  # Would be tracked from history
        )
        
        self.performance_history.append({
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics.__dict__
        })
        
        # Keep only last 100 entries
        if len(self.performance_history) > 100:
            self.performance_history = self.performance_history[-100:]
        
        return {
            "current_metrics": metrics.__dict__,
            "performance_trend": self._analyze_performance_trend(),
            "recommendations": self._get_performance_recommendations(metrics)
        }
    
    def _get_gpu_utilization(self) -> float:
        """Get GPU utilization percentage"""
        if not self.system_info.gpu_available:
            return 0.0
        
        # This would require nvidia-ml-py or similar
        # For now, return a placeholder
        return 50.0
    
    def _analyze_performance_trend(self) -> Dict[str, Any]:
        """Analyze performance trends over time"""
        if len(self.performance_history) < 2:
            return {"trend": "insufficient_data"}
        
        recent_times = [entry["metrics"]["generation_time"] for entry in self.performance_history[-10:]]
        avg_time = sum(recent_times) / len(recent_times)
        
        if len(recent_times) >= 5:
            trend = "improving" if recent_times[-1] < recent_times[0] else "degrading"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "average_generation_time": round(avg_time, 2),
            "performance_score": self._calculate_performance_score()
        }
    
    def _get_performance_recommendations(self, metrics: PerformanceMetrics) -> List[str]:
        """Get performance-based recommendations"""
        recommendations = []
        
        if metrics.generation_time > 60:
            recommendations.append("⏱️ Slow generation - consider reducing resolution or steps")
        
        if metrics.memory_peak > self.system_info.gpu_memory_total * 0.8:
            recommendations.append("🧹 High memory usage - reduce batch size or resolution")
        
        if metrics.gpu_utilization < 50:
            recommendations.append("⚡ Low GPU utilization - increase batch size or quality")
        
        if metrics.cpu_utilization > 90:
            recommendations.append("🔥 High CPU usage - reduce concurrent operations")
        
        return recommendations
    
    def get_optimization_report(self) -> Dict[str, Any]:
        """Get comprehensive optimization report"""
        analysis = self.analyze_system()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "system_analysis": analysis,
            "optimization_score": self._calculate_optimization_score(),
            "priority_actions": self._get_priority_actions(),
            "performance_predictions": self._get_performance_predictions()
        }
    
    def _calculate_optimization_score(self) -> float:
        """Calculate optimization potential score"""
        score = 0
        
        # GPU optimization potential
        if self.system_info.gpu_available:
            vram_usage = self.system_info.gpu_memory_used / self.system_info.gpu_memory_total
            if vram_usage < 0.5:
                score += 30  # Can increase quality
            elif vram_usage < 0.8:
                score += 20  # Moderate optimization
            else:
                score += 10  # Limited optimization
        
        # Memory optimization potential
        if self.system_info.memory_percent < 50:
            score += 25  # Can increase batch size
        elif self.system_info.memory_percent < 75:
            score += 15  # Moderate optimization
        else:
            score += 5  # Limited optimization
        
        # CPU optimization potential
        if self.system_info.cpu_percent < 50:
            score += 20  # Can increase concurrency
        elif self.system_info.cpu_percent < 75:
            score += 10  # Moderate optimization
        else:
            score += 5  # Limited optimization
        
        return min(100, score)
    
    def _get_priority_actions(self) -> List[str]:
        """Get priority optimization actions"""
        actions = []
        
        if not self.system_info.gpu_available:
            actions.append("🚨 CRITICAL: Enable GPU runtime in Colab")
        
        if self.system_info.memory_percent > 90:
            actions.append("🚨 HIGH: Free up system memory")
        
        if self.system_info.disk_percent > 90:
            actions.append("🚨 HIGH: Free up disk space")
        
        if self.system_info.gpu_memory_used / self.system_info.gpu_memory_total > 0.9:
            actions.append("⚠️ MEDIUM: Reduce GPU memory usage")
        
        if self.system_info.cpu_percent > 85:
            actions.append("⚠️ MEDIUM: Reduce CPU load")
        
        return actions
    
    def _get_performance_predictions(self) -> Dict[str, Any]:
        """Get performance predictions based on current system"""
        predictions = {}
        
        # Generation time prediction
        if self.system_info.gpu_available:
            if self.system_info.gpu_memory_total >= 16:
                predictions["generation_time"] = "15-30 seconds"
            elif self.system_info.gpu_memory_total >= 8:
                predictions["generation_time"] = "20-40 seconds"
            else:
                predictions["generation_time"] = "30-60 seconds"
        else:
            predictions["generation_time"] = "2-5 minutes"
        
        # Quality prediction
        if self.system_info.gpu_available and self.system_info.gpu_memory_total >= 8:
            predictions["max_quality"] = "High (1024x1280)"
        elif self.system_info.gpu_available:
            predictions["max_quality"] = "Medium (896x1120)"
        else:
            predictions["max_quality"] = "Low (640x800)"
        
        # Batch size prediction
        if self.system_info.gpu_available and self.system_info.gpu_memory_total >= 16:
            predictions["max_batch_size"] = 4
        elif self.system_info.gpu_available and self.system_info.gpu_memory_total >= 8:
            predictions["max_batch_size"] = 2
        else:
            predictions["max_batch_size"] = 1
        
        return predictions

# Example usage and testing
if __name__ == "__main__":
    # Test the diagnostics
    diagnostics = SystemDiagnostics()
    
    # Run system analysis
    analysis = diagnostics.analyze_system()
    print("System Analysis:")
    print(json.dumps(analysis, indent=2))
    
    # Get optimization report
    report = diagnostics.get_optimization_report()
    print("\nOptimization Report:")
    print(json.dumps(report, indent=2))
