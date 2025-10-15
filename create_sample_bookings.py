"""
Create sample flight bookings and routes for testing
Run this script to populate the database with sample airline data
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent))

from app.database import db_manager, Booking, FlightRoute

# Sample Flight Routes
FLIGHT_ROUTES = [
    {
        "flight_number": "SH101",
        "airline": "SkyHigh Airlines",
        "origin": "JFK",
        "destination": "LAX",
        "departure_time": "08:00",
        "arrival_time": "11:30",
        "duration_minutes": 330,
        "aircraft_type": "Boeing 737-800",
        "days_of_operation": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    },
    {
        "flight_number": "SH202",
        "airline": "SkyHigh Airlines",
        "origin": "LAX",
        "destination": "JFK",
        "departure_time": "14:00",
        "arrival_time": "22:30",
        "duration_minutes": 330,
        "aircraft_type": "Boeing 737-800",
        "days_of_operation": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    },
    {
        "flight_number": "SH303",
        "airline": "SkyHigh Airlines",
        "origin": "ORD",
        "destination": "MIA",
        "departure_time": "10:30",
        "arrival_time": "14:45",
        "duration_minutes": 195,
        "aircraft_type": "Airbus A320",
        "days_of_operation": ["Mon", "Wed", "Fri", "Sun"]
    },
    {
        "flight_number": "SH404",
        "airline": "SkyHigh Airlines",
        "origin": "SFO",
        "destination": "SEA",
        "departure_time": "07:00",
        "arrival_time": "09:30",
        "duration_minutes": 150,
        "aircraft_type": "Boeing 737-700",
        "days_of_operation": ["Mon", "Tue", "Wed", "Thu", "Fri"]
    },
    {
        "flight_number": "SH505",
        "airline": "SkyHigh Airlines",
        "origin": "DEN",
        "destination": "PHX",
        "departure_time": "16:00",
        "arrival_time": "17:45",
        "duration_minutes": 105,
        "aircraft_type": "Airbus A319",
        "days_of_operation": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    }
]

# Sample Bookings
SAMPLE_BOOKINGS = [
    {
        "booking_reference": "AA123456",
        "customer_email": "john.smith@example.com",
        "customer_name": "John Smith",
        "customer_phone": "+1-555-0101",
        "flight_number": "SH101",
        "origin": "JFK",
        "destination": "LAX",
        "departure_date": datetime.utcnow() + timedelta(days=15),
        "arrival_date": datetime.utcnow() + timedelta(days=15, hours=5, minutes=30),
        "booking_class": "economy",
        "seat_number": "12A",
        "ticket_price": 299.99,
        "booking_status": "confirmed",
        "payment_status": "paid",
        "passengers": [
            {
                "name": "John Smith",
                "age": 35,
                "passport": "US123456789",
                "frequent_flyer": "SH12345678"
            }
        ],
        "special_requests": None
    },
    {
        "booking_reference": "BB789012",
        "customer_email": "sarah.jones@example.com",
        "customer_name": "Sarah Jones",
        "customer_phone": "+1-555-0202",
        "flight_number": "SH202",
        "origin": "LAX",
        "destination": "JFK",
        "departure_date": datetime.utcnow() + timedelta(days=7),
        "arrival_date": datetime.utcnow() + timedelta(days=7, hours=8, minutes=30),
        "booking_class": "business",
        "seat_number": "2C",
        "ticket_price": 899.99,
        "booking_status": "confirmed",
        "payment_status": "paid",
        "passengers": [
            {
                "name": "Sarah Jones",
                "age": 42,
                "passport": "US987654321",
                "frequent_flyer": "SH98765432"
            }
        ],
        "special_requests": "Vegetarian meal"
    },
    {
        "booking_reference": "CC345678",
        "customer_email": "mike.wilson@example.com",
        "customer_name": "Mike Wilson",
        "customer_phone": "+1-555-0303",
        "flight_number": "SH303",
        "origin": "ORD",
        "destination": "MIA",
        "departure_date": datetime.utcnow() + timedelta(days=3),
        "arrival_date": datetime.utcnow() + timedelta(days=3, hours=4, minutes=15),
        "booking_class": "economy",
        "seat_number": "15B",
        "ticket_price": 189.99,
        "booking_status": "confirmed",
        "payment_status": "paid",
        "passengers": [
            {
                "name": "Mike Wilson",
                "age": 28,
                "passport": "US456789123"
            },
            {
                "name": "Lisa Wilson",
                "age": 26,
                "passport": "US456789124"
            }
        ],
        "special_requests": "Extra legroom"
    },
    {
        "booking_reference": "DD901234",
        "customer_email": "emma.davis@example.com",
        "customer_name": "Emma Davis",
        "customer_phone": "+1-555-0404",
        "flight_number": "SH404",
        "origin": "SFO",
        "destination": "SEA",
        "departure_date": datetime.utcnow() + timedelta(days=1),
        "arrival_date": datetime.utcnow() + timedelta(days=1, hours=2, minutes=30),
        "booking_class": "first",
        "seat_number": "1A",
        "ticket_price": 599.99,
        "booking_status": "confirmed",
        "payment_status": "paid",
        "passengers": [
            {
                "name": "Emma Davis",
                "age": 55,
                "passport": "US789012345",
                "frequent_flyer": "SH55555555"
            }
        ],
        "special_requests": "Wheelchair assistance required"
    },
    {
        "booking_reference": "EE567890",
        "customer_email": "alex.brown@example.com",
        "customer_name": "Alex Brown",
        "customer_phone": "+1-555-0505",
        "flight_number": "SH505",
        "origin": "DEN",
        "destination": "PHX",
        "departure_date": datetime.utcnow() + timedelta(days=30),
        "arrival_date": datetime.utcnow() + timedelta(days=30, hours=1, minutes=45),
        "booking_class": "economy",
        "seat_number": "20F",
        "ticket_price": 129.99,
        "booking_status": "confirmed",
        "payment_status": "pending",
        "passengers": [
            {
                "name": "Alex Brown",
                "age": 22,
                "passport": "US234567890"
            }
        ],
        "special_requests": None
    }
]


async def create_sample_data():
    """Create sample flight routes and bookings"""
    print("=" * 80)
    print("  CREATING SAMPLE AIRLINE DATA")
    print("=" * 80)
    print()
    
    try:
        await db_manager.connect()
        
        # Create Flight Routes
        print("📍 Creating Flight Routes...")
        print("-" * 80)
        flight_success = 0
        flight_skip = 0
        
        for flight_data in FLIGHT_ROUTES:
            try:
                # Check if flight exists
                existing = await db_manager.get_flight_route(flight_data["flight_number"])
                if existing:
                    print(f"⚠️  Flight {flight_data['flight_number']} already exists - skipping")
                    flight_skip += 1
                else:
                    flight = FlightRoute(**flight_data)
                    await db_manager.create_flight_route(flight)
                    print(f"✅ Created: {flight_data['flight_number']} ({flight_data['origin']} → {flight_data['destination']})")
                    flight_success += 1
            except Exception as e:
                print(f"❌ Error creating flight {flight_data['flight_number']}: {e}")
        
        print()
        print("📋 Creating Sample Bookings...")
        print("-" * 80)
        booking_success = 0
        booking_skip = 0
        
        for booking_data in SAMPLE_BOOKINGS:
            try:
                # Check if booking exists
                existing = await db_manager.get_booking(booking_data["booking_reference"])
                if existing:
                    print(f"⚠️  Booking {booking_data['booking_reference']} already exists - skipping")
                    booking_skip += 1
                else:
                    booking = Booking(**booking_data)
                    await db_manager.create_booking(booking)
                    print(f"✅ Created: {booking_data['booking_reference']} ({booking_data['customer_name']})")
                    booking_success += 1
            except Exception as e:
                print(f"❌ Error creating booking {booking_data['booking_reference']}: {e}")
        
        print()
        print("=" * 80)
        print(f"✅ Sample Data Creation Complete!")
        print(f"   - Flight Routes Created: {flight_success} (Skipped: {flight_skip})")
        print(f"   - Bookings Created: {booking_success} (Skipped: {booking_skip})")
        print("=" * 80)
        print()
        print("📊 Available Routes:")
        print("   - SH101: JFK → LAX (Daily)")
        print("   - SH202: LAX → JFK (Daily)")
        print("   - SH303: ORD → MIA (Mon/Wed/Fri/Sun)")
        print("   - SH404: SFO → SEA (Weekdays)")
        print("   - SH505: DEN → PHX (Daily)")
        print()
        print("🎫 Sample Bookings:")
        print("   - AA123456: John Smith (JFK→LAX, Economy)")
        print("   - BB789012: Sarah Jones (LAX→JFK, Business)")
        print("   - CC345678: Mike Wilson (ORD→MIA, Economy, 2 passengers)")
        print("   - DD901234: Emma Davis (SFO→SEA, First Class)")
        print("   - EE567890: Alex Brown (DEN→PHX, Economy)")
        print()
        
        await db_manager.disconnect()
        
    except Exception as e:
        print(f"❌ Creation failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(create_sample_data())

