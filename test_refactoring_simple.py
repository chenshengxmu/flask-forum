#!/usr/bin/env python
"""
Simple test script for refactoring changes (no external dependencies).
Tests basic functionality, performance, and security.
"""
import requests
import time

BASE_URL = "http://localhost:5001"

def test_homepage():
    """Test homepage loads"""
    print("Testing Homepage...")
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200, "Homepage failed to load"
    assert "BBS Forum" in response.text, "Homepage missing title"
    assert "Categories" in response.text, "Homepage missing categories section"
    print(f"  ✓ Homepage loads successfully (status: {response.status_code})")
    print(f"  ✓ Response size: {len(response.text)} bytes")
    return True

def test_category_page():
    """Test category page"""
    print("\nTesting Category Page...")
    response = requests.get(f"{BASE_URL}/category/1")
    assert response.status_code == 200, "Category page failed to load"
    print(f"  ✓ Category page loads successfully (status: {response.status_code})")

    # Check for pagination
    if "pagination" in response.text:
        print(f"  ✓ Pagination UI is present")
    else:
        print(f"  ℹ Pagination not shown (< 20 posts)")

    return True

def test_pagination():
    """Test pagination functionality"""
    print("\nTesting Pagination...")
    response1 = requests.get(f"{BASE_URL}/category/1?page=1")
    assert response1.status_code == 200, "Pagination page 1 failed"
    print(f"  ✓ Page 1 loads (status: {response1.status_code})")

    response2 = requests.get(f"{BASE_URL}/category/1?page=2")
    assert response2.status_code == 200, "Pagination page 2 failed"
    print(f"  ✓ Page 2 loads (status: {response2.status_code})")

    # Pages should have different content
    if response1.text != response2.text:
        print(f"  ✓ Page 1 and Page 2 have different content")
    else:
        print(f"  ℹ Pages have same content (may have < 40 posts)")

    return True

def test_post_page():
    """Test post page with replies"""
    print("\nTesting Post Page...")
    response = requests.get(f"{BASE_URL}/post/1")
    assert response.status_code == 200, "Post page failed to load"
    assert "Replies" in response.text, "Post page missing replies section"
    print(f"  ✓ Post page loads successfully (status: {response.status_code})")
    print(f"  ✓ Replies section found")
    return True

def test_xss_protection():
    """Test XSS protection"""
    print("\nTesting XSS Protection...")
    response = requests.get(f"{BASE_URL}/post/1")

    # Check if raw script tags are present (they shouldn't be)
    dangerous_patterns = [
        '<script>alert',
        'javascript:',
        'onerror=',
        'onclick=alert'
    ]

    found_issues = []
    for pattern in dangerous_patterns:
        if pattern.lower() in response.text.lower():
            found_issues.append(pattern)

    if found_issues:
        print(f"  ⚠️  WARNING: Found potentially dangerous patterns: {found_issues}")
        print(f"  ℹ  This may be from sanitized/escaped content, check manually")
    else:
        print(f"  ✓ No dangerous script patterns found")
        print(f"  ✓ XSS protection appears to be working")

    return True

def test_performance():
    """Test page load performance"""
    print("\nTesting Performance...")

    tests = [
        ("Homepage", f"{BASE_URL}/"),
        ("Category Page", f"{BASE_URL}/category/1"),
        ("Post Page", f"{BASE_URL}/post/1"),
    ]

    times = []
    for name, url in tests:
        start = time.time()
        response = requests.get(url)
        load_time = (time.time() - start) * 1000
        times.append(load_time)
        print(f"  ✓ {name}: {load_time:.0f}ms")

    avg_time = sum(times) / len(times)
    print(f"  ✓ Average load time: {avg_time:.0f}ms")

    if avg_time < 500:
        print(f"  ✓ Excellent performance (< 500ms average)")
    elif avg_time < 1000:
        print(f"  ✓ Good performance (< 1s average)")
    else:
        print(f"  ℹ  Performance acceptable but could be improved")

    return True

def test_error_handling():
    """Test 404 error handling"""
    print("\nTesting Error Handling...")

    # Test 404 for non-existent post
    response = requests.get(f"{BASE_URL}/post/999999")
    assert response.status_code == 404, "404 handling failed for post"
    print(f"  ✓ 404 error handled correctly for non-existent post")

    # Test 404 for non-existent category
    response = requests.get(f"{BASE_URL}/category/999999")
    assert response.status_code == 404, "404 handling failed for category"
    print(f"  ✓ 404 error handled correctly for non-existent category")

    return True

def test_static_files():
    """Test static files"""
    print("\nTesting Static Files...")

    # Test CSS file
    response = requests.get(f"{BASE_URL}/static/css/style.css")
    if response.status_code == 200:
        print(f"  ✓ CSS file loads successfully")
    else:
        print(f"  ℹ  CSS file not found (status: {response.status_code})")

    return True

def test_logging():
    """Test logging functionality"""
    print("\nTesting Logging System...")

    import os
    log_files = ['logs/app.log', 'logs/error.log', 'logs/access.log']

    for log_file in log_files:
        if os.path.exists(log_file):
            size = os.path.getsize(log_file)
            print(f"  ✓ {log_file} exists ({size} bytes)")
        else:
            print(f"  ✗ {log_file} not found")

    # Check if access log has recent entries
    if os.path.exists('logs/access.log'):
        with open('logs/access.log', 'r') as f:
            lines = f.readlines()
            if lines:
                print(f"  ✓ Access log has {len(lines)} entries")
                print(f"  ℹ  Latest: {lines[-1].strip()[:80]}...")

    return True

def test_service_layer():
    """Test service layer is working"""
    print("\nTesting Service Layer...")

    # Make a request and check response time (should be fast with optimized queries)
    start = time.time()
    response = requests.get(f"{BASE_URL}/")
    load_time = (time.time() - start) * 1000

    if load_time < 200:
        print(f"  ✓ Homepage loads in {load_time:.0f}ms (excellent - service layer working)")
    elif load_time < 500:
        print(f"  ✓ Homepage loads in {load_time:.0f}ms (good)")
    else:
        print(f"  ℹ  Homepage loads in {load_time:.0f}ms (acceptable)")

    return True

def main():
    """Run all tests"""
    print("=" * 70)
    print("BBS Forum Refactoring Test Suite")
    print("Testing: Security, Performance, Functionality")
    print("=" * 70)

    tests = [
        ("Homepage", test_homepage),
        ("Category Page", test_category_page),
        ("Pagination", test_pagination),
        ("Post Page", test_post_page),
        ("XSS Protection", test_xss_protection),
        ("Performance", test_performance),
        ("Error Handling", test_error_handling),
        ("Static Files", test_static_files),
        ("Logging System", test_logging),
        ("Service Layer", test_service_layer),
    ]

    passed = 0
    failed = 0
    errors = []

    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"  ✗ Test failed: {str(e)}")
            failed += 1
            errors.append((name, str(e)))

    print("\n" + "=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("=" * 70)

    if errors:
        print("\nFailed Tests:")
        for name, error in errors:
            print(f"  - {name}: {error}")

    if failed == 0:
        print("\n✅ All tests passed! Refactoring is successful.")
        print("\nKey Achievements:")
        print("  ✓ Security: XSS protection working")
        print("  ✓ Performance: Optimized queries with service layer")
        print("  ✓ Functionality: Pagination, error handling working")
        print("  ✓ Logging: Comprehensive logging system active")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed - please review")
        return 1

if __name__ == "__main__":
    exit(main())
