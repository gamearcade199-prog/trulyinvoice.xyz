"""
📸 IMAGE QUALITY CHECKER
Verify image quality before expensive AI processing
Prevents wasted API calls on blurry/dark/low-quality images
"""

import io
import numpy as np
from PIL import Image
from typing import Dict, Any, List


class ImageQualityChecker:
    """
    Check image quality before processing with AI APIs
    Scores: Good (80-100%), Fair (60-80%), Poor (<60%)
    """
    
    def __init__(self):
        self.thresholds = {
            "brightness": (0.2, 0.8),     # 20% - 80% brightness
            "contrast": 0.3,                # Minimum contrast score
            "sharpness": 0.1,              # Minimum sharpness (Laplacian variance)
            "noise": 0.4,                  # Maximum noise level
        }
    
    def check_quality(self, image_data: bytes) -> Dict[str, Any]:
        """
        Check overall image quality before processing
        
        Returns: {
            quality: 'good' | 'fair' | 'poor',
            score: 0-100,
            confidence: 0-1,
            details: {brightness, contrast, sharpness, noise, resolution},
            recommendations: [],
            can_process: True/False
        }
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            image_array = np.array(image)
            
            # Convert to grayscale for analysis
            if len(image_array.shape) == 3:
                # RGB to grayscale
                image_gray = np.dot(image_array[...,:3], [0.299, 0.587, 0.114])
            else:
                image_gray = image_array
            
            # Calculate individual scores
            brightness_score = self._check_brightness(image_gray)
            contrast_score = self._check_contrast(image_gray)
            sharpness_score = self._check_sharpness(image_gray)
            noise_score = self._check_noise(image_gray)
            
            # Combine into overall score
            component_scores = [
                brightness_score,
                contrast_score,
                sharpness_score,
                1.0 - noise_score  # Invert noise (lower is better)
            ]
            overall_score = np.mean(component_scores)
            
            # Determine quality level
            if overall_score >= 0.80:
                quality = "good"
            elif overall_score >= 0.60:
                quality = "fair"
            else:
                quality = "poor"
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                brightness_score, contrast_score, 
                sharpness_score, noise_score, quality
            )
            
            return {
                "quality": quality,
                "score": int(overall_score * 100),
                "confidence": float(overall_score),
                "details": {
                    "brightness": float(brightness_score),
                    "contrast": float(contrast_score),
                    "sharpness": float(sharpness_score),
                    "noise": float(noise_score),
                    "resolution": image.size,
                },
                "recommendations": recommendations,
                "can_process": quality != "poor"
            }
            
        except Exception as e:
            return {
                "quality": "error",
                "score": 0,
                "confidence": 0,
                "error": str(e),
                "can_process": False
            }
    
    def _check_brightness(self, image_gray: np.ndarray) -> float:
        """Check if image is too dark or too bright"""
        brightness = np.mean(image_gray) / 255.0
        min_brightness, max_brightness = self.thresholds["brightness"]
        
        if min_brightness <= brightness <= max_brightness:
            return 1.0
        elif brightness < min_brightness:
            return brightness / min_brightness
        else:
            return (1.0 - (brightness - max_brightness)) / (1.0 - max_brightness)
    
    def _check_contrast(self, image_gray: np.ndarray) -> float:
        """Check image contrast (std dev of pixel values)"""
        contrast = np.std(image_gray) / 255.0
        threshold = self.thresholds["contrast"]
        
        if contrast >= threshold:
            return min(1.0, contrast)
        else:
            return contrast / threshold
    
    def _check_sharpness(self, image_gray: np.ndarray) -> float:
        """Check image sharpness (not blurry)"""
        try:
            # Use Laplacian for blur detection
            kernel = np.array([
                [0, -1, 0],
                [-1, 4, -1],
                [0, -1, 0]
            ], dtype=np.float32)
            
            # Apply Laplacian
            laplacian = self._apply_kernel(image_gray, kernel)
            sharpness = np.var(laplacian)
            
            # Normalize
            normalized = min(1.0, sharpness / 100.0)
            threshold = self.thresholds["sharpness"]
            
            if normalized >= threshold:
                return normalized
            else:
                return normalized / threshold
        except:
            return 0.5  # Default if calculation fails
    
    def _check_noise(self, image_gray: np.ndarray) -> float:
        """Check image noise level"""
        try:
            # Compare with bilateral filter
            filtered = self._bilateral_filter(image_gray)
            noise = np.mean(np.abs(image_gray.astype(float) - filtered)) / 255.0
            threshold = self.thresholds["noise"]
            
            if noise <= threshold:
                return noise
            else:
                return threshold
        except:
            return 0.3  # Default if calculation fails
    
    def _apply_kernel(self, image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        """Simple kernel application"""
        h, w = image.shape
        kh, kw = kernel.shape
        result = np.zeros_like(image, dtype=np.float32)
        
        pad_h, pad_w = kh // 2, kw // 2
        
        for y in range(pad_h, h - pad_h):
            for x in range(pad_w, w - pad_w):
                region = image[y-pad_h:y+pad_h+1, x-pad_w:x+pad_w+1].astype(np.float32)
                result[y, x] = np.sum(region * kernel)
        
        return result
    
    def _bilateral_filter(self, image: np.ndarray, d: int = 9, 
                          sigma_color: float = 75, sigma_space: float = 75) -> np.ndarray:
        """Simple bilateral filter approximation"""
        result = image.copy().astype(np.float32)
        h, w = image.shape
        
        # Apply simplified bilateral filter
        for y in range(d, h - d):
            for x in range(d, w - d):
                region = image[y-d:y+d+1, x-d:x+d+1].astype(np.float32)
                center = image[y, x].astype(np.float32)
                
                # Weight by color similarity and distance
                weights = np.exp(-((region - center) ** 2) / (2 * sigma_color ** 2))
                result[y, x] = np.sum(region * weights) / np.sum(weights)
        
        return result.astype(np.uint8)
    
    def _generate_recommendations(self, brightness: float, contrast: float, 
                                   sharpness: float, noise: float, 
                                   quality: str) -> List[str]:
        """Generate specific recommendations for improvement"""
        recommendations = []
        
        if brightness < 0.5:
            recommendations.append("📸 Image is too dark - improve lighting")
        if brightness > 0.9:
            recommendations.append("📸 Image is too bright - reduce glare/reflections")
        if contrast < 0.5:
            recommendations.append("📄 Low contrast - ensure document is clearly visible")
        if sharpness < 0.5:
            recommendations.append("🔍 Image is blurry - use steady hand or tripod")
        if noise > 0.3:
            recommendations.append("🔧 Image is noisy - reduce graininess in lighting")
        
        if quality == "good":
            recommendations.append("✅ Image quality is excellent!")
        elif quality == "fair":
            recommendations.append("⚠️  Image quality is fair - extraction may have minor errors")
        elif quality == "poor":
            recommendations.append("❌ Image quality too low - retake with better conditions")
        
        return recommendations


def test_image_quality_checker():
    """Test image quality checker"""
    print("\n" + "="*70)
    print("🧪 IMAGE QUALITY CHECKER TEST")
    print("="*70)
    
    checker = ImageQualityChecker()
    
    # Create test images
    test_images = [
        ("good", create_good_quality_image()),
        ("fair", create_fair_quality_image()),
        ("poor", create_poor_quality_image()),
    ]
    
    for name, image_data in test_images:
        print(f"\n📋 Testing {name.upper()} quality image:")
        result = checker.check_quality(image_data)
        
        print(f"   Quality: {result['quality']} ({result['score']}%)")
        print(f"   Brightness: {result['details']['brightness']:.0%}")
        print(f"   Contrast: {result['details']['contrast']:.0%}")
        print(f"   Sharpness: {result['details']['sharpness']:.0%}")
        print(f"   Noise: {result['details']['noise']:.0%}")
        print(f"   Can Process: {'✅ Yes' if result['can_process'] else '❌ No'}")
        
        if result['recommendations']:
            print("   Recommendations:")
            for rec in result['recommendations']:
                print(f"     - {rec}")


def create_good_quality_image() -> bytes:
    """Create a test image with good quality"""
    img = Image.new('RGB', (200, 200), color='white')
    pixels = img.load()
    
    # Add high-contrast text-like pattern
    for y in range(50, 150):
        for x in range(50, 150):
            if (x + y) % 20 < 10:
                pixels[x, y] = (0, 0, 0)
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()


def create_fair_quality_image() -> bytes:
    """Create a test image with fair quality (slight blur/noise)"""
    img = Image.new('RGB', (200, 200), color=(200, 200, 200))
    pixels = img.load()
    
    # Add pattern with some noise
    import random
    random.seed(42)
    for y in range(50, 150):
        for x in range(50, 150):
            val = 100 + random.randint(-30, 30)
            if (x + y) % 20 < 10:
                val = max(0, min(255, val - 50))
            pixels[x, y] = (val, val, val)
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()


def create_poor_quality_image() -> bytes:
    """Create a test image with poor quality (very dark)"""
    img = Image.new('RGB', (200, 200), color=(30, 30, 30))
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()


if __name__ == "__main__":
    test_image_quality_checker()
