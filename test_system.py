"""
Test script to verify the customer support system
"""
import requests
import json
import time


API_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_add_knowledge():
    """Test adding knowledge"""
    print("\n=== Testing Add Knowledge ===")
    try:
        knowledge = {
            "title": "Test FAQ",
            "content": "This is a test knowledge base entry for testing purposes.",
            "category": "test",
            "tags": ["test", "demo"]
        }
        
        response = requests.post(
            f"{API_URL}/api/knowledge/add",
            json=knowledge
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_chat():
    """Test chat endpoint"""
    print("\n=== Testing Chat Endpoint ===")
    
    test_messages = [
        "How do I reset my password?",
        "What are your business hours?",
        "How much does the professional plan cost?",
        "Can I cancel my subscription?"
    ]
    
    conversation_id = None
    
    for msg in test_messages:
        try:
            print(f"\n→ User: {msg}")
            
            payload = {
                "message": msg,
                "customer_identifier": "test@example.com",
                "customer_name": "Test User"
            }
            
            if conversation_id:
                payload["conversation_id"] = conversation_id
            
            response = requests.post(
                f"{API_URL}/api/chat",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                conversation_id = data["conversation_id"]
                print(f"← Bot: {data['response']}")
                print(f"   Confidence: {data['confidence']:.2%}")
                print(f"   Conversation ID: {conversation_id}")
            else:
                print(f"✗ Error: {response.text}")
                return False
            
            time.sleep(1)
        
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
    
    return True


def test_get_ticket():
    """Test getting ticket details"""
    print("\n=== Testing Get Ticket ===")
    
    # First create a conversation
    try:
        response = requests.post(
            f"{API_URL}/api/chat",
            json={
                "message": "Test message",
                "customer_identifier": "ticket-test@example.com"
            }
        )
        
        if response.status_code == 200:
            ticket_id = response.json()["conversation_id"]
            
            # Now get the ticket
            response = requests.get(f"{API_URL}/api/tickets/{ticket_id}")
            
            if response.status_code == 200:
                print(f"Status: {response.status_code}")
                ticket = response.json()
                print(f"Ticket ID: {ticket['ticket_id']}")
                print(f"Channel: {ticket['channel']}")
                print(f"Status: {ticket['status']}")
                print(f"Messages: {len(ticket['conversation'])}")
                return True
            else:
                print(f"✗ Error: {response.text}")
                return False
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_list_tickets():
    """Test listing tickets"""
    print("\n=== Testing List Tickets ===")
    try:
        response = requests.get(f"{API_URL}/api/tickets?status=open&limit=10")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {response.status_code}")
            print(f"Total tickets: {data['count']}")
            
            if data['tickets']:
                print("\nFirst ticket:")
                print(f"  ID: {data['tickets'][0]['ticket_id']}")
                print(f"  Channel: {data['tickets'][0]['channel']}")
                print(f"  Status: {data['tickets'][0]['status']}")
            
            return True
        else:
            print(f"✗ Error: {response.text}")
            return False
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_statistics():
    """Test statistics endpoint"""
    print("\n=== Testing Statistics ===")
    try:
        response = requests.get(f"{API_URL}/api/stats")
        
        if response.status_code == 200:
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"✗ Error: {response.text}")
            return False
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("   INTELLIGENT CUSTOMER SUPPORT SYSTEM - TEST SUITE")
    print("=" * 70)
    
    tests = [
        ("Health Check", test_health),
        ("Add Knowledge", test_add_knowledge),
        ("Chat Functionality", test_chat),
        ("Get Ticket", test_get_ticket),
        ("List Tickets", test_list_tickets),
        ("Statistics", test_statistics)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
        time.sleep(1)
    
    # Summary
    print("\n" + "=" * 70)
    print("   TEST SUMMARY")
    print("=" * 70)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")


if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except requests.exceptions.ConnectionError:
        print(f"\n✗ Cannot connect to API at {API_URL}")
        print("  Make sure the application is running (python main.py)")

