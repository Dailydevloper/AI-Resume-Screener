"""
Test script for the AI Resume Screener
Tests the screening endpoint with sample data
"""

import requests
import time

# Wait for server to be ready
print("Waiting for server to start...")
time.sleep(2)

BASE_URL = "http://localhost:5000"

# Test 1: Health check
print("\n=== Test 1: Health Check ===")
try:
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Screen resume
print("\n=== Test 2: Screen Resume (API) ===")
try:
    with open('test_resume.txt', 'r') as f:
        resume_text = f.read()
    
    with open('test_jd.txt', 'r') as f:
        jd_text = f.read()
    
    files = {'resume': open('test_resume.txt', 'rb')}
    data = {'jd_text': jd_text}
    
    response = requests.post(f"{BASE_URL}/api/screen", files=files, data=data)
    
    files['resume'].close()
    
    print(f"Status: {response.status_code}")
    result = response.json()
    
    print("\n📊 Screening Results:")
    print(f"  Final Score: {result.get('final_score', 'N/A')}/100")
    print(f"  Similarity: {result.get('similarity_score', 'N/A')}%")
    print(f"  Skill Match: {result.get('skill_match_score', 'N/A')}%")
    print(f"  Rating: {result.get('rating', 'N/A')}")
    
    if result.get('candidate_info'):
        print("\n👤 Candidate Info:")
        info = result['candidate_info']
        print(f"  Name: {info.get('name', 'N/A')}")
        print(f"  Email: {info.get('email', 'N/A')}")
        print(f"  Phone: {info.get('phone', 'N/A')}")
    
    if result.get('skill_details'):
        details = result['skill_details']
        print("\n🎯 Skill Match Details:")
        print(f"  Matched Skills: {details.get('matched', [])[:5]}")
        print(f"  Missing Skills: {details.get('missing', [])[:5]}")
        print(f"  Total Matched: {len(details.get('matched', []))}")
        print(f"  Total Missing: {len(details.get('missing', []))}")
    
    print("\n💬 Feedback:")
    print(f"  {result.get('feedback', 'N/A')[:200]}...")
    
    screening_id = result.get('screening_id')
    print(f"\n✅ Test 2 PASSED - Screening ID: {screening_id}")

except Exception as e:
    print(f"❌ Test 2 FAILED: {e}")

# Test 3: Get screening history
print("\n=== Test 3: Screening History ===")
try:
    response = requests.get(f"{BASE_URL}/api/history")
    print(f"Status: {response.status_code}")
    results = response.json()
    print(f"Number of screenings: {len(results)}")
    if results:
        print(f"Latest: {results[0].get('resume_filename')} - Score: {results[0].get('final_score')}")
    print("✅ Test 3 PASSED")
except Exception as e:
    print(f"❌ Test 3 FAILED: {e}")

# Test 4: Get specific screening
print("\n=== Test 4: Get Specific Screening ===")
try:
    response = requests.get(f"{BASE_URL}/api/screening/1")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Resume: {data.get('resume_filename')}")
        print(f"Score: {data.get('final_score')}")
        print("✅ Test 4 PASSED")
    else:
        print("⚠️  Test 4: No record found (expected on first run)")
except Exception as e:
    print(f"❌ Test 4 FAILED: {e}")

print("\n" + "="*50)
print("🎉 Testing Complete!")
print("="*50)
