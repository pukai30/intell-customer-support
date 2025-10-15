"""
Airline Customer Support Knowledge Base
Load comprehensive airline policies and procedures
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from app.rag_system import rag_system
from datetime import datetime

# Airline Knowledge Documents
AIRLINE_KNOWLEDGE = [
    {
        "title": "Flight Cancellation Policy",
        "content": """
        Flight Cancellation Policy - SkyHigh Airlines
        
        Passenger-Initiated Cancellations:
        
        1. 24-Hour Free Cancellation:
           - All tickets can be cancelled within 24 hours of booking for a full refund
           - Applies to bookings made at least 7 days before departure
           - No cancellation fees apply
        
        2. Cancellation Fees (after 24 hours):
           Economy Class:
           - More than 7 days before: $150 cancellation fee
           - 3-7 days before: $250 cancellation fee
           - Less than 3 days: $350 cancellation fee
           
           Business/First Class:
           - More than 7 days before: Free cancellation, 90% refund
           - 3-7 days before: $100 cancellation fee
           - Less than 3 days: $200 cancellation fee
        
        3. Refund Processing:
           - Refunds processed within 7-10 business days
           - Original payment method used
           - Cancellation fee deducted from refund amount
        
        Airline-Initiated Cancellations:
        - Full refund or free rebooking
        - Compensation up to $800 depending on delay
        - Hotel accommodation if overnight delay
        - Meal vouchers for delays over 3 hours
        """,
        "category": "airline_policy",
        "tags": ["cancellation", "refund", "policy"],
        "priority": 2,
        "domain": "AIRLINE"
    },
    {
        "title": "Ticket Refund Process",
        "content": """
        Ticket Refund Process - SkyHigh Airlines
        
        How to Request a Refund:
        
        1. Online Refund Request:
           - Go to skyh igh.com/manage-booking
           - Enter booking reference (PNR) and last name
           - Click "Cancel and Refund"
           - Confirm cancellation
           - Refund automatically processed
        
        2. Customer Service Refund:
           - Call: 1-800-SKYHI GH (24/7)
           - Email: refunds@skyhigh.com
           - Provide: Booking reference, passenger name, reason
           - Response within 24 hours
        
        3. Refund Timeline:
           - Credit/Debit Card: 7-10 business days
           - Travel Voucher: Immediate (additional 10% bonus)
           - Wire Transfer: 10-15 business days
        
        4. Non-Refundable Tickets:
           - Basic Economy fares are non-refundable
           - Can be changed with a change fee ($75-$200)
           - Name changes not permitted
           - Can convert to travel credit (minus $100 fee)
        
        5. Travel Credit:
           - Valid for 12 months from issue date
           - Can be used for any SkyHigh flight
           - Transferable to family members (one time)
           - Combinable with other credits
        
        Special Circumstances (Full Refund):
        - Medical emergency (doctor's note required)
        - Death in family (death certificate required)
        - Military deployment (orders required)
        - Jury duty (court summons required)
        """,
        "category": "airline_policy",
        "tags": ["refund", "cancellation", "process"],
        "priority": 2,
        "domain": "AIRLINE"
    },
    {
        "title": "Flight Change and Modification Policy",
        "content": """
        Flight Change and Modification Policy - SkyHigh Airlines
        
        Online Flight Changes:
        1. Visit skyh igh.com/manage-booking
        2. Enter booking reference and last name
        3. Select "Change Flight"
        4. Choose new flight (same route)
        5. Pay fare difference + change fee
        
        Change Fees:
        Economy Class:
        - More than 14 days before: $75 change fee
        - 7-14 days before: $150 change fee
        - Less than 7 days: $200 change fee
        - Same day changes: $100 standby fee
        
        Business/First Class:
        - More than 7 days: Free changes
        - Less than 7 days: $50 change fee
        - Same day changes: Free
        
        Elite Member Benefits:
        - Gold/Platinum: Free changes anytime
        - Silver: 50% off change fees
        - Basic members: Standard fees apply
        
        Date/Time Changes:
        - Can change to any date within 1 year
        - Subject to seat availability
        - Fare difference applies if new flight costs more
        - No refund if new flight costs less
        
        Route Changes:
        - Must cancel and rebook as new ticket
        - Original ticket rules apply
        - May require additional payment
        
        Name Corrections:
        - Minor spelling errors: Free (up to 3 characters)
        - Legal name change: $50 fee (proof required)
        - Complete name change: Not permitted, must cancel
        """,
        "category": "airline_policy",
        "tags": ["flight change", "modification", "rebooking"],
        "priority": 2,
        "domain": "AIRLINE"
    },
    {
        "title": "Baggage Policy and Fees",
        "content": """
        Baggage Policy - SkyHigh Airlines
        
        Carry-On Baggage (Free):
        - 1 personal item (purse, laptop bag): Max 18x14x8 inches
        - 1 carry-on bag: Max 22x14x9 inches, 15 lbs
        - Must fit in overhead bin or under seat
        
        Checked Baggage Fees:
        Domestic Flights:
        - 1st bag: $35 (Economy), Free (Business/First)
        - 2nd bag: $45 (Economy), Free (Business/First)
        - 3rd+ bag: $150 each
        - Overweight (50-70 lbs): $100 extra
        - Oversized (62-80 linear inches): $200 extra
        
        International Flights:
        - 1st bag: Free (all classes)
        - 2nd bag: $100 (Economy), Free (Business/First)
        - 3rd+ bag: $200 each
        
        Weight and Size Limits:
        - Standard: 50 lbs, 62 linear inches (L+W+H)
        - Heavy bag (50-70 lbs): Additional fee
        - Oversized (62-80 inches): Additional fee
        - Over limits may not be accepted
        
        Special Items:
        - Sports equipment: $150 per item
        - Musical instruments: Free as carry-on if fits
        - Pet carrier: $125 in cabin, $200 in cargo
        - Wheelchairs/mobility aids: Always free
        
        Elite Member Benefits:
        - Gold/Platinum: 2 free checked bags (70 lbs each)
        - Silver: 1 free checked bag (50 lbs)
        
        Lost or Damaged Baggage:
        - Report immediately at baggage claim
        - File claim within 24 hours
        - Compensation up to $3,500 domestic
        - Compensation up to $1,780 international
        - Tracking available via app
        """,
        "category": "airline_policy",
        "tags": ["baggage", "fees", "luggage"],
        "priority": 2,
        "domain": "AIRLINE"
    },
    {
        "title": "Check-in and Boarding Process",
        "content": """
        Check-in and Boarding Process - SkyHigh Airlines
        
        Online Check-in:
        - Available 24 hours before departure
        - Access via website or mobile app
        - Select/change seats (fees may apply)
        - Download or email boarding pass
        - Add baggage and pay fees
        
        Airport Check-in:
        - Self-service kiosks: 24 hours before to 45 min before
        - Counter check-in: 3 hours before to 45 min before
        - Bag drop: Until 45 minutes before departure
        
        Check-in Deadlines:
        Domestic Flights:
        - Online check-in: 24 hrs before to 1 hr before
        - Airport check-in: 45 minutes before departure
        - Bag drop: 45 minutes before departure
        
        International Flights:
        - Online check-in: 24 hrs before to 90 min before
        - Airport check-in: 90 minutes before departure
        - Bag drop: 60 minutes before departure
        
        Boarding Process:
        1. Pre-boarding: Families with young children, special assistance
        2. Zone 1: First Class, Business Class
        3. Zone 2: Gold/Platinum elite members
        4. Zone 3: Silver elite members
        5. Zone 4: Main cabin (rear seats first)
        6. Zone 5: Basic economy
        
        Mobile Boarding Pass:
        - Save to Apple Wallet or Google Pay
        - Offline access available
        - Scan at TSA and gate
        - Backup: Show confirmation email
        
        Travel Documents:
        Domestic:
        - Government-issued photo ID required
        - TSA PreCheck if enrolled
        
        International:
        - Valid passport required
        - Visa (if required for destination)
        - Return/onward ticket
        - COVID-19 documents (if required)
        """,
        "category": "airline_procedures",
        "tags": ["check-in", "boarding", "process"],
        "priority": 2,
        "domain": "AIRLINE"
    },
    {
        "title": "Seat Selection and Upgrades",
        "content": """
        Seat Selection and Upgrades - SkyHigh Airlines
        
        Advance Seat Selection:
        Basic Economy:
        - Random seat assignment at check-in (free)
        - Cannot select in advance
        - May pay $15-$35 to choose standard seat
        
        Economy:
        - Free seat selection at booking
        - Preferred seats (extra legroom): $25-$75
        - Exit row seats: $40-$100 (restrictions apply)
        
        Business/First Class:
        - Free seat selection anytime
        - Preferred seats always free
        
        Seat Types and Fees:
        - Standard seat: Free (Economy and above)
        - Preferred seat (extra legroom): $25-$75
        - Exit row: $40-$100
        - Bulkhead: $35-$85
        - Window/Aisle (Basic Economy): $15-$30
        
        Seat Change:
        - Change anytime before check-in (subject to fees)
        - Free changes for elite members
        - At airport: Subject to availability
        - Families: Seating together assistance available
        
        Upgrade Options:
        1. Paid Upgrades:
           - Economy to Economy Plus: $75-$150
           - Economy to Business: $200-$500
           - Check at airport for last-minute deals
        
        2. Miles Upgrade:
           - Use miles to upgrade at booking
           - 15,000-25,000 miles per segment
           - Subject to availability
        
        3. Bid for Upgrade:
           - Place bid 72 hours before flight
           - Minimum bid shown in app
           - Notified 24 hours before if successful
        
        4. Complimentary Upgrades:
           - Platinum members: Confirmed 72 hours before
           - Gold members: Waitlist, cleared at departure
           - Based on elite status, fare class, and availability
        
        Special Seating:
        - Bassinet seats: Request at booking (infants)
        - Wheelchair accessible: Available at no charge
        - Extra seat: Purchase adjacent seat at booking
        """,
        "category": "airline_services",
        "tags": ["seats", "upgrades", "selection"],
        "priority": 2,
        "domain": "AIRLINE"
    },
    {
        "title": "Flight Delays and Compensation",
        "content": """
        Flight Delays and Compensation - SkyHigh Airlines
        
        Delay Notifications:
        - Email and SMS alerts sent automatically
        - Check flight status: skyhigh.com or mobile app
        - Real-time updates at airport
        
        Passenger Rights - Delays:
        
        1-2 Hour Delay (Controllable):
        - Free wifi access
        - Updates every 30 minutes
        - May rebook at no charge
        
        2-4 Hour Delay:
        - Meal vouchers ($12 domestic, $20 international)
        - Free rebooking to next available flight
        - Option to cancel for full refund
        
        4+ Hour Delay or Overnight:
        - Hotel accommodation provided
        - Ground transportation to hotel
        - Meal vouchers ($40 value)
        - Full refund or rebooking
        
        Cancellation Compensation:
        Airline Fault (weather, mechanical):
        - Full refund or free rebooking
        - Up to $800 cash compensation (EU/Canada flights)
        - Hotel and meals if overnight
        
        Uncontrollable (severe weather, ATC):
        - Free rebooking only
        - No compensation required
        - May rebook on partner airlines
        
        Denied Boarding (Oversold):
        Volunteer:
        - Travel voucher up to $1,000
        - Confirmed seat on next flight
        - Meal vouchers
        
        Involuntary:
        - Cash compensation: 200-400% of fare (up to $1,550)
        - Rebook on next available flight
        - Hotel if overnight
        - Meals and transportation
        
        How to Claim Compensation:
        1. Keep all receipts
        2. File claim online: skyhigh.com/compensation
        3. Provide: Booking reference, flight details, receipts
        4. Response within 30 days
        5. Payment within 60 days if approved
        
        Elite Member Benefits:
        - Priority rebooking
        - Confirmed seats on standby
        - Access to airline lounges during delay
        - Proactive notification
        """,
        "category": "airline_policy",
        "tags": ["delays", "compensation", "rights"],
        "priority": 2,
        "domain": "AIRLINE"
    },
    {
        "title": "Loyalty Program - SkyMiles Rewards",
        "content": """
        SkyMiles Rewards Program - SkyHigh Airlines
        
        Membership Tiers:
        1. Blue (Basic): 0-24,999 miles/year
        2. Silver: 25,000-49,999 miles/year
        3. Gold: 50,000-99,999 miles/year
        4. Platinum: 100,000+ miles/year
        
        Earning Miles:
        - Flights: 5 miles per $1 spent (Blue)
        - Silver: 7 miles per $1
        - Gold: 9 miles per $1
        - Platinum: 11 miles per $1
        
        Bonus Miles:
        - Credit card: 2-3 miles per $1 on purchases
        - Hotel partners: 500-1,000 miles per stay
        - Car rentals: 50-500 miles per rental
        - Shopping portal: 2-10 miles per $1
        
        Redeeming Miles:
        Flights:
        - Domestic: Starting at 7,500 miles one-way
        - International: Starting at 15,000 miles one-way
        - Partner airlines: 10,000+ miles
        - No blackout dates
        
        Other Redemptions:
        - Seat upgrades: 7,500 miles
        - Baggage fees: 2,500 miles
        - Vacation packages: 15,000+ miles
        - Magazine subscriptions: 3,000 miles
        
        Elite Benefits:
        Silver:
        - Priority check-in
        - 1 free checked bag
        - 25% bonus miles
        - Free seat selection
        
        Gold:
        - All Silver benefits
        - 2 free checked bags (70 lbs)
        - Free upgrades (domestic)
        - 50% bonus miles
        - Lounge access (2 visits/year)
        
        Platinum:
        - All Gold benefits
        - 3 free checked bags (70 lbs)
        - Unlimited upgrades
        - 100% bonus miles
        - Unlimited lounge access + guest
        - Dedicated phone line
        - Complimentary same-day changes
        
        Miles Expiration:
        - Miles valid for 24 months
        - Activity extends expiration
        - Any earning/redeeming resets clock
        - Purchase/gift miles to extend
        
        Family Pooling:
        - Combine miles with up to 7 family members
        - Minimum age: 13 years
        - Same household requirement
        - No fee to join
        """,
        "category": "airline_services",
        "tags": ["loyalty", "miles", "rewards", "elite status"],
        "priority": 2,
        "domain": "AIRLINE"
    },
    {
        "title": "Special Assistance and Accessibility",
        "content": """
        Special Assistance and Accessibility - SkyHigh Airlines
        
        Wheelchair Services:
        - Complimentary at all airports
        - Request at booking or 48 hours before flight
        - Curb to gate, gate to gate, or gate to seat
        - Personal wheelchairs: Free checked baggage
        - Battery-powered wheelchairs: Special handling
        
        Visual Impairments:
        - Guide dogs fly free in cabin
        - Escort assistance available
        - Braille safety cards on request
        - Audio announcements at gate
        
        Hearing Impairments:
        - Visual alerts and notifications
        - Text-based communication at counters
        - Captioned safety videos
        - Staff trained in basic sign language
        
        Cognitive/Developmental Disabilities:
        - Early boarding available
        - Assistance through security
        - Quiet room access at airports
        - Patience cards available
        
        Medical Conditions:
        Portable Oxygen Concentrators (POC):
        - Approved POCs allowed in cabin
        - Notify airline 48 hours in advance
        - Bring extra batteries (not checked)
        - FAA-approved devices only
        
        Medical Equipment:
        - CPAP, nebulizers: Free carry-on
        - Medication: Carry in original packaging
        - Syringes: With prescription label
        - Refrigerated medication: Notify in advance
        
        Special Meals:
        Request 24 hours before flight:
        - Diabetic meals
        - Low sodium
        - Gluten-free
        - Kosher/Halal
        - Vegetarian/Vegan
        - Allergy-friendly
        
        Traveling with Service Animals:
        - Service dogs fly free in cabin
        - Must be trained and certified
        - Advance notice: 48 hours
        - Health/vaccination records required
        - Relief area maps available at airports
        
        Unaccompanied Minors (5-14 years):
        - $150 service fee each way
        - Direct flights only (or connecting with escort)
        - Check-in: 90 minutes before
        - ID required for drop-off/pick-up persons
        - Flight attendant supervision
        - Escorted through connections
        
        How to Request Assistance:
        1. At booking: Select assistance type
        2. By phone: 1-800-SKYACCESS (24/7)
        3. Online: Manage booking section
        4. At airport: 2 hours before flight
        
        Airport Assistance Available:
        - Wheelchair/mobility assistance
        - Priority security screening
        - Boarding assistance
        - Deplaning assistance
        - Baggage assistance
        - Connection guidance
        """,
        "category": "airline_services",
        "tags": ["accessibility", "special assistance", "disabilities"],
        "priority": 2,
        "domain": "AIRLINE"
    },
    {
        "title": "International Travel Requirements",
        "content": """
        International Travel Requirements - SkyHigh Airlines
        
        Travel Documents:
        
        Passport Requirements:
        - Must be valid for 6 months beyond travel dates
        - Blank pages: 2-4 required for stamps
        - Child passport: Same requirements
        - Check expiry date well in advance
        
        Visa Requirements:
        - Check destination country requirements
        - Apply 4-8 weeks before travel
        - Electronic visas (eVisa): Apply online
        - Transit visas: May be required for connections
        - Visit: skyhigh.com/travel-info for country guide
        
        Health Requirements:
        
        Vaccinations:
        - Yellow fever: Required for certain countries
        - COVID-19: Check current requirements
        - Malaria prophylaxis: Recommended for some regions
        - Carry vaccination card
        
        COVID-19 Protocols (if applicable):
        - Vaccination proof or negative test
        - Check requirements for destination
        - Transit country requirements may differ
        - Download health apps if required
        - Carry paper copies of all documents
        
        Customs and Immigration:
        
        Declaration Forms:
        - Complete before arrival
        - Available on flight or electronically
        - Declare: Cash over $10,000, goods, food
        - Keep receipts for expensive items
        
        Duty-Free Allowances:
        US Residents returning:
        - $800 duty-free allowance
        - 1 liter alcohol (21+)
        - 200 cigarettes
        - Family members: Combine allowances
        
        Prohibited Items:
        - Fresh fruits and vegetables
        - Meat products
        - Plants and seeds
        - Certain medications
        - Check country-specific restrictions
        
        Airport Transit:
        - May need transit visa even without leaving airport
        - Check minimum connection times
        - International to domestic: Reclear security
        - Collect and recheck bags if required
        
        Currency and Customs:
        - Carry cash in local currency
        - Declare amounts over $10,000
        - Keep customs receipts for claims
        - VAT refund: Keep receipts and forms
        
        Travel Insurance:
        Recommended coverage:
        - Medical emergency
        - Trip cancellation
        - Lost/delayed baggage
        - Travel delays
        - Emergency evacuation
        
        Helpful Resources:
        - US State Dept: travel.state.gov
        - CDC Travel: wwwnc.cdc.gov/travel
        - SkyHigh Travel Info: skyhigh.com/international
        - Embassy contact: Keep handy
        - Smart Traveler Enrollment (STEP): Register trip
        
        Pre-Flight Checklist:
        □ Passport valid 6+ months
        □ Visa obtained (if required)
        □ Vaccinations current
        □ Health/COVID docs ready
        □ Travel insurance purchased
        □ Copies of all documents
        □ Emergency contacts saved
        □ Credit card travel notice
        □ Local currency obtained
        □ SkyHigh app downloaded
        """,
        "category": "airline_procedures",
        "tags": ["international", "travel", "documents", "requirements"],
        "priority": 2,
        "domain": "AIRLINE"
    }
]


async def load_airline_knowledge():
    """Load airline knowledge base into the system"""
    print("=" * 80)
    print("  LOADING AIRLINE CUSTOMER SUPPORT KNOWLEDGE BASE")
    print("=" * 80)
    print()
    
    try:
        # Initialize RAG system
        await rag_system.initialize()
        
        success_count = 0
        fail_count = 0
        
        for idx, doc in enumerate(AIRLINE_KNOWLEDGE, 1):
            try:
                print(f"[{idx}/{len(AIRLINE_KNOWLEDGE)}] Adding: {doc['title']}")
                
                result = await rag_system.add_documents_to_knowledge_base(
                    documents=[{
                        "title": doc["title"],
                        "content": doc["content"],
                        "category": doc["category"],
                        "tags": doc["tags"],
                        "source": "airline_knowledge_base",
                        "priority": doc["priority"],
                        "domain": doc["domain"]
                    }],
                    created_by="system",
                    source="airline_knowledge_base"
                )
                
                if result and "document_ids" in result:
                    print(f"   ✓ Successfully added (ID: {result['document_ids'][0]})")
                    success_count += 1
                else:
                    print(f"   ✗ Failed to add")
                    fail_count += 1
                    
            except Exception as e:
                print(f"   ✗ Error: {e}")
                fail_count += 1
        
        print()
        print("=" * 80)
        print(f"✅ Airline Knowledge Base Loading Complete!")
        print(f"   - Successfully added: {success_count}/{len(AIRLINE_KNOWLEDGE)}")
        print(f"   - Failed: {fail_count}/{len(AIRLINE_KNOWLEDGE)}")
        print("=" * 80)
        print()
        print("📚 Loaded Knowledge Categories:")
        print("   - Flight Cancellation Policy")
        print("   - Ticket Refund Process")
        print("   - Flight Change and Modification")
        print("   - Baggage Policy and Fees")
        print("   - Check-in and Boarding Process")
        print("   - Seat Selection and Upgrades")
        print("   - Flight Delays and Compensation")
        print("   - Loyalty Program (SkyMiles)")
        print("   - Special Assistance and Accessibility")
        print("   - International Travel Requirements")
        print()
        
    except Exception as e:
        print(f"❌ Error loading airline knowledge base: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(load_airline_knowledge())

