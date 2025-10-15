"""
Setup Indian National Holidays Calendar
Loads all major Indian holidays for the current year and next year
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime, date

sys.path.insert(0, str(Path(__file__).parent))

from app.database import db_manager, Holiday

# Indian National Holidays 2024-2025
INDIAN_HOLIDAYS = [
    # 2024 Holidays
    {"date": "2024-01-26", "name": "Republic Day", "holiday_type": "national", "is_working_day": False},
    {"date": "2024-03-08", "name": "Holi", "holiday_type": "national", "is_working_day": False},
    {"date": "2024-03-25", "name": "Holi", "holiday_type": "national", "is_working_day": False},
    {"date": "2024-04-11", "name": "Eid al-Fitr", "holiday_type": "national", "is_working_day": False},
    {"date": "2024-04-14", "name": "Ambedkar Jayanti", "holiday_type": "national", "is_working_day": False},
    {"date": "2024-04-17", "name": "Ram Navami", "holiday_type": "national", "is_working_day": False},
    {"date": "2024-05-01", "name": "Labour Day", "holiday_type": "national", "is_working_day": False},
    {"date": "2024-08-15", "name": "Independence Day", "holiday_type": "national", "is_working_day": False},
    {"date": "2024-08-26", "name": "Janmashtami", "holiday_type": "national", "is_working_day": False},
    {"date": "2024-09-15", "name": "Ganesh Chaturthi", "holiday_type": "national", "is_working_day": False},
    {"date": "2024-10-02", "name": "Gandhi Jayanti", "holiday_type": "national", "is_working_day": False},
    {"date": "2024-10-12", "name": "Dussehra", "holiday_type": "national", "is_working_day": False},
    {"date": "2024-10-31", "name": "Diwali", "holiday_type": "national", "is_working_day": False},
    {"date": "2024-11-01", "name": "Diwali", "holiday_type": "national", "is_working_day": False},
    {"date": "2024-11-15", "name": "Guru Nanak Jayanti", "holiday_type": "national", "is_working_day": False},
    {"date": "2024-12-25", "name": "Christmas", "holiday_type": "national", "is_working_day": False},
    
    # 2025 Holidays
    {"date": "2025-01-26", "name": "Republic Day", "holiday_type": "national", "is_working_day": False},
    {"date": "2025-03-14", "name": "Holi", "holiday_type": "national", "is_working_day": False},
    {"date": "2025-03-29", "name": "Holi", "holiday_type": "national", "is_working_day": False},
    {"date": "2025-03-31", "name": "Eid al-Fitr", "holiday_type": "national", "is_working_day": False},
    {"date": "2025-04-14", "name": "Ambedkar Jayanti", "holiday_type": "national", "is_working_day": False},
    {"date": "2025-04-06", "name": "Ram Navami", "holiday_type": "national", "is_working_day": False},
    {"date": "2025-05-01", "name": "Labour Day", "holiday_type": "national", "is_working_day": False},
    {"date": "2025-08-15", "name": "Independence Day", "holiday_type": "national", "is_working_day": False},
    {"date": "2025-08-15", "name": "Janmashtami", "holiday_type": "national", "is_working_day": False},
    {"date": "2025-09-04", "name": "Ganesh Chaturthi", "holiday_type": "national", "is_working_day": False},
    {"date": "2025-10-02", "name": "Gandhi Jayanti", "holiday_type": "national", "is_working_day": False},
    {"date": "2025-10-02", "name": "Dussehra", "holiday_type": "national", "is_working_day": False},
    {"date": "2025-10-20", "name": "Diwali", "holiday_type": "national", "is_working_day": False},
    {"date": "2025-10-21", "name": "Diwali", "holiday_type": "national", "is_working_day": False},
    {"date": "2025-11-05", "name": "Guru Nanak Jayanti", "holiday_type": "national", "is_working_day": False},
    {"date": "2025-12-25", "name": "Christmas", "holiday_type": "national", "is_working_day": False},
    
    # Regional Holidays (Maharashtra)
    {"date": "2024-02-19", "name": "Chhatrapati Shivaji Maharaj Jayanti", "holiday_type": "regional", "region": "Maharashtra", "is_working_day": False},
    {"date": "2024-05-01", "name": "Maharashtra Day", "holiday_type": "regional", "region": "Maharashtra", "is_working_day": False},
    {"date": "2025-02-19", "name": "Chhatrapati Shivaji Maharaj Jayanti", "holiday_type": "regional", "region": "Maharashtra", "is_working_day": False},
    {"date": "2025-05-01", "name": "Maharashtra Day", "holiday_type": "regional", "region": "Maharashtra", "is_working_day": False},
    
    # Regional Holidays (Karnataka)
    {"date": "2024-11-01", "name": "Karnataka Rajyotsava", "holiday_type": "regional", "region": "Karnataka", "is_working_day": False},
    {"date": "2025-11-01", "name": "Karnataka Rajyotsava", "holiday_type": "regional", "region": "Karnataka", "is_working_day": False},
    
    # Regional Holidays (Tamil Nadu)
    {"date": "2024-01-15", "name": "Pongal", "holiday_type": "regional", "region": "Tamil Nadu", "is_working_day": False},
    {"date": "2024-01-16", "name": "Pongal", "holiday_type": "regional", "region": "Tamil Nadu", "is_working_day": False},
    {"date": "2025-01-14", "name": "Pongal", "holiday_type": "regional", "region": "Tamil Nadu", "is_working_day": False},
    {"date": "2025-01-15", "name": "Pongal", "holiday_type": "regional", "region": "Tamil Nadu", "is_working_day": False},
    
    # Company Holidays (Optional - can be customized)
    {"date": "2024-12-31", "name": "New Year's Eve", "holiday_type": "company", "is_working_day": False},
    {"date": "2025-01-01", "name": "New Year's Day", "holiday_type": "company", "is_working_day": False},
    {"date": "2025-12-31", "name": "New Year's Eve", "holiday_type": "company", "is_working_day": False},
]


async def setup_indian_holidays():
    """Load Indian holidays into the database"""
    print("=" * 80)
    print("  SETTING UP INDIAN HOLIDAY CALENDAR")
    print("=" * 80)
    print()
    
    try:
        await db_manager.connect()
        
        print("🇮🇳 Loading Indian National Holidays...")
        print("-" * 80)
        
        success_count = 0
        skip_count = 0
        
        for holiday_data in INDIAN_HOLIDAYS:
            try:
                # Check if holiday already exists
                existing = await db_manager.db.holidays.find_one({
                    "date": holiday_data["date"],
                    "name": holiday_data["name"]
                })
                
                if existing:
                    print(f"⚠️  {holiday_data['name']} ({holiday_data['date']}) already exists - skipping")
                    skip_count += 1
                    continue
                
                holiday = Holiday(**holiday_data)
                await db_manager.create_holiday(holiday)
                print(f"✅ Added: {holiday_data['name']} ({holiday_data['date']})")
                success_count += 1
                
            except Exception as e:
                print(f"❌ Error adding {holiday_data['name']}: {e}")
        
        print()
        print("=" * 80)
        print(f"✅ Indian Holiday Calendar Setup Complete!")
        print(f"   - Holidays Added: {success_count}")
        print(f"   - Skipped (already exist): {skip_count}")
        print("=" * 80)
        print()
        print("📅 Holiday Summary:")
        print("   - National Holidays: Republic Day, Independence Day, Gandhi Jayanti, etc.")
        print("   - Religious Holidays: Holi, Diwali, Eid, Christmas, etc.")
        print("   - Regional Holidays: Maharashtra, Karnataka, Tamil Nadu")
        print("   - Company Holidays: New Year's Eve/Day")
        print()
        print("🎯 Features:")
        print("   - All agents will have these holidays applied")
        print("   - Holiday-aware ticket assignment")
        print("   - Regional holiday support")
        print("   - Company-specific holidays")
        print()
        
        await db_manager.disconnect()
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(setup_indian_holidays())
