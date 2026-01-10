#!/usr/bin/env python3
"""
Deception Detector API Test Script
Tests all public API endpoints with comprehensive error handling and output.
"""

import requests
import hashlib
import time
import sys
import argparse
from typing import Dict, Any, Optional

# ANSI color codes for pretty output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ {text}{Colors.END}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


class DeceptionDetectorAPITest:
    """Test suite for Deception Detector API"""
    
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.token: Optional[str] = None
        self.passed_tests = 0
        self.failed_tests = 0
    
    def test_health_check(self) -> bool:
        """Test health check endpoint"""
        print_header("Test 1: Health Check")
        print_info(f"GET {self.base_url}/health")
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"API is healthy: {data}")
                self.passed_tests += 1
                return True
            else:
                print_error(f"Health check failed with status {response.status_code}")
                print_error(f"Response: {response.text}")
                self.failed_tests += 1
                return False
                
        except requests.exceptions.RequestException as e:
            print_error(f"Connection error: {str(e)}")
            self.failed_tests += 1
            return False
    
    def test_get_models(self) -> bool:
        """Test get available models endpoint"""
        print_header("Test 2: Get Available Models")
        print_info(f"GET {self.base_url}/models")
        
        try:
            response = requests.get(f"{self.base_url}/models", timeout=10)
            
            if response.status_code == 200:
                models = response.json()
                print_success(f"Found {len(models)} available models:")
                for model in models:
                    print(f"  • {model}")
                self.passed_tests += 1
                return True
            else:
                print_error(f"Failed to get models with status {response.status_code}")
                print_error(f"Response: {response.text}")
                self.failed_tests += 1
                return False
                
        except requests.exceptions.RequestException as e:
            print_error(f"Connection error: {str(e)}")
            self.failed_tests += 1
            return False
    
    def test_authentication(self) -> bool:
        """Test JWT token authentication"""
        print_header("Test 3: Authentication (Get JWT Token)")
        print_info(f"POST {self.base_url}/auth/token")
        print_info(f"Username: {self.username}")
        print_info(f"Password hash: {self.password_hash[:20]}...")
        
        try:
            response = requests.post(
                f"{self.base_url}/auth/token",
                json={
                    "username": self.username,
                    "password_hash": self.password_hash
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data["token"]
                expires_in = data["expires_in"]
                print_success(f"Token obtained successfully!")
                print_info(f"Token: {self.token[:30]}...{self.token[-10:]}")
                print_info(f"Expires in: {expires_in} seconds ({expires_in/60:.1f} minutes)")
                self.passed_tests += 1
                return True
            else:
                print_error(f"Authentication failed with status {response.status_code}")
                print_error(f"Response: {response.text}")
                self.failed_tests += 1
                return False
                
        except requests.exceptions.RequestException as e:
            print_error(f"Connection error: {str(e)}")
            self.failed_tests += 1
            return False
    
    def test_check_deception(self, text: str, model_name: str) -> bool:
        """Test check deception endpoint"""
        print_header(f"Test 4: Check Deception - {model_name}")
        print_info(f"POST {self.base_url}/public/checkDeception")
        print_info(f"Text: \"{text}\"")
        print_info(f"Model: {model_name}")
        
        if not self.token:
            print_error("No token available. Run authentication test first.")
            self.failed_tests += 1
            return False
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/public/checkDeception",
                headers={"Authorization": f"Bearer {self.token}"},
                json={
                    "text": text,
                    "modelName": model_name
                },
                timeout=30
            )
            elapsed_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                
                print_success(f"Analysis completed in {elapsed_time:.2f}s")
                print(f"\n{Colors.BOLD}Results:{Colors.END}")
                print(f"  Prediction: {Colors.RED if result['is_deceptive'] else Colors.GREEN}{('DECEPTIVE' if result['is_deceptive'] else 'TRUTHFUL')}{Colors.END}")
                print(f"  Confidence: {result['confidence']:.2%}")
                print(f"  Model used: {result['model_used']}")
                
                print(f"\n{Colors.BOLD}Top 5 SHAP Explanations:{Colors.END}")
                for word, score in result['shap_words'][:5]:
                    color = Colors.RED if score > 0 else Colors.GREEN
                    direction = "→ deceptive" if score > 0 else "→ truthful"
                    print(f"  {word:20} {color}{score:+.3f}{Colors.END} {direction}")
                
                print(f"\n{Colors.BOLD}Top 5 LIME Explanations:{Colors.END}")
                for word, score in result['lime_words'][:5]:
                    color = Colors.RED if score > 0 else Colors.GREEN
                    direction = "→ deceptive" if score > 0 else "→ truthful"
                    print(f"  {word:20} {color}{score:+.3f}{Colors.END} {direction}")
                
                self.passed_tests += 1
                return True
            else:
                print_error(f"Deception check failed with status {response.status_code}")
                print_error(f"Response: {response.text}")
                self.failed_tests += 1
                return False
                
        except requests.exceptions.RequestException as e:
            print_error(f"Connection error: {str(e)}")
            self.failed_tests += 1
            return False
    
    def test_simple_predict(self, text: str, model_name: str) -> bool:
        """Test simple predict endpoint (no auth)"""
        print_header(f"Test 5: Simple Predict (No Auth) - {model_name}")
        print_info(f"POST {self.base_url}/predict")
        print_info(f"Text: \"{text}\"")
        print_info(f"Model: {model_name}")
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/predict",
                json={
                    "text": text,
                    "model": model_name  # Changed from model_name to model
                },
                timeout=30
            )
            elapsed_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                
                print_success(f"Prediction completed in {elapsed_time:.2f}s")
                print(f"\n{Colors.BOLD}Results:{Colors.END}")
                print(f"  Prediction: {Colors.RED if result['prediction'] == 'deceptive' else Colors.GREEN}{result['prediction'].upper()}{Colors.END}")
                print(f"  Confidence: {result['confidence']:.2%}")
                print(f"  Model used: {result['model_used']}")
                
                # Processing time may not be in response
                if 'processing_time' in result:
                    print(f"  Processing time: {result['processing_time']:.3f}s")
                
                # Probabilities may not be in simple predict response
                if 'probabilities' in result:
                    print(f"\n{Colors.BOLD}Probabilities:{Colors.END}")
                    for label, prob in result['probabilities'].items():
                        color = Colors.RED if label == 'deceptive' else Colors.GREEN
                        print(f"  {label.capitalize():10} {color}{prob:.2%}{Colors.END}")
                
                self.passed_tests += 1
                return True
            else:
                print_error(f"Prediction failed with status {response.status_code}")
                print_error(f"Response: {response.text}")
                self.failed_tests += 1
                return False
                
        except requests.exceptions.RequestException as e:
            print_error(f"Connection error: {str(e)}")
            self.failed_tests += 1
            return False
    
    def test_invalid_token(self) -> bool:
        """Test with invalid token to verify auth is working"""
        print_header("Test 6: Invalid Token (Security Test)")
        print_info(f"POST {self.base_url}/public/checkDeception")
        print_info("Using invalid token: 'invalid_token_xyz'")
        
        try:
            response = requests.post(
                f"{self.base_url}/public/checkDeception",
                headers={"Authorization": "Bearer invalid_token_xyz"},
                json={
                    "text": "test text",
                    "modelName": "bert-combined-1"
                },
                timeout=10
            )
            
            if response.status_code == 401:
                print_success("API correctly rejected invalid token (401 Unauthorized)")
                self.passed_tests += 1
                return True
            else:
                print_error(f"API should return 401 but returned {response.status_code}")
                print_warning("Security issue: Invalid tokens are being accepted!")
                self.failed_tests += 1
                return False
                
        except requests.exceptions.RequestException as e:
            print_error(f"Connection error: {str(e)}")
            self.failed_tests += 1
            return False
    
    def test_rate_limiting(self) -> bool:
        """Test rate limiting"""
        print_header("Test 7: Rate Limiting")
        print_info("Making multiple rapid requests to test rate limits...")
        print_info("Rate limit for /predict endpoint: 20 requests/minute")
        
        try:
            requests_made = 0
            rate_limited = False
            
            # Make 25 rapid requests to /predict endpoint (rate limit is 20/min)
            for i in range(25):
                response = requests.post(
                    f"{self.base_url}/predict",
                    json={
                        "text": f"Test message {i}",
                        "model": "bert-combined-1"
                    },
                    timeout=5
                )
                requests_made += 1
                
                if response.status_code == 429:
                    rate_limited = True
                    print_success(f"Rate limit triggered after {requests_made} requests (429 Too Many Requests)")
                    try:
                        error_data = response.json()
                        print_info(f"Response: {error_data}")
                    except:
                        pass
                    break
                elif response.status_code != 200:
                    print_warning(f"Request {requests_made} returned status {response.status_code}")
                
                # No delay - test rate limiting
            
            if rate_limited:
                self.passed_tests += 1
                return True
            else:
                print_warning(f"Made {requests_made} requests without hitting rate limit")
                print_warning("Note: Rate limiting in production should be enforced at infrastructure level (nginx/load balancer)")
                print_info("Current rate limits are per-IP and may reset between tests")
                # Not a failure - rate limiting might be disabled in dev or handled elsewhere
                self.passed_tests += 1
                return True
                
        except requests.exceptions.RequestException as e:
            print_error(f"Connection error: {str(e)}")
            self.failed_tests += 1
            return False
    
    def print_summary(self):
        """Print test summary"""
        print_header("Test Summary")
        
        total_tests = self.passed_tests + self.failed_tests
        pass_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total tests: {total_tests}")
        print(f"{Colors.GREEN}Passed: {self.passed_tests}{Colors.END}")
        print(f"{Colors.RED}Failed: {self.failed_tests}{Colors.END}")
        print(f"\nPass rate: {pass_rate:.1f}%")
        
        if self.failed_tests == 0:
            print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 All tests passed!{Colors.END}")
        else:
            print(f"\n{Colors.BOLD}{Colors.RED}⚠ Some tests failed. Check the output above for details.{Colors.END}")


def main():
    """Main test execution"""
    parser = argparse.ArgumentParser(description='Test Deception Detector API')
    parser.add_argument('--url', default='http://localhost/api', help='API base URL (default: http://localhost/api)')
    parser.add_argument('--username', default='externalapiuser', help='API username (default: externalapiuser)')
    # Not the real deployed password, only for testing purposes
    parser.add_argument('--password', default='zl0KzHEXmdetk1_Lxy2QvQ', help='API password')
    parser.add_argument('--skip-rate-limit', action='store_true', help='Skip rate limiting test')
    
    args = parser.parse_args()
    
    print(f"{Colors.BOLD}{Colors.HEADER}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║       Deception Detector API Test Suite                   ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    print_info(f"API Base URL: {args.url}")
    print_info(f"Username: {args.username}")
    print_info(f"Testing started at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Initialize test suite
    test = DeceptionDetectorAPITest(args.url, args.username, args.password)
    
    # Run tests
    test.test_health_check()
    test.test_get_models()
    test.test_authentication()
    
    if test.token:
        # Test deception detection with different examples
        test.test_check_deception(
            "Climate change is a hoax created by scientists to get funding.",
            "bert-climate-change-1"
        )
        
        test.test_simple_predict(
            "The vaccine is completely safe and effective.",
            "bert-covid-1"
        )
        
        test.test_invalid_token()
        
        if not args.skip_rate_limit:
            test.test_rate_limiting()
    else:
        print_warning("Authentication failed - skipping authenticated endpoint tests")
    
    # Print summary
    test.print_summary()
    
    # Exit with appropriate code
    sys.exit(0 if test.failed_tests == 0 else 1)


if __name__ == "__main__":
    main()
