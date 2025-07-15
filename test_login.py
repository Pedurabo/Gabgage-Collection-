from app import app

with app.test_client() as client:
    try:
        print("Testing login route...")
        response = client.get('/auth/login')
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.data[:200]}...")
        
        if response.status_code == 500:
            print("500 error detected!")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc() 