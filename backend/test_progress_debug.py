#!/usr/bin/env python3
"""
Debug script for training progress system
"""

import sys
import os
from datetime import datetime

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

def test_progress_functions():
    """Test progress functions without API"""
    try:
        from app.database import engine, get_db
        from app.crud import (
            get_training_by_course_id,
            update_training_progress, 
            get_training_progress,
            reset_training_progress
        )
        
        print("🧪 Testing progress system...")
        
        # Test database connection
        db = next(get_db())
        print("✅ Database connection successful")
        
        # Find a training to test with
        from app.models.database_models import Training
        training = db.query(Training).first()
        
        if not training:
            print("❌ No trainings found in database")
            return False
            
        print(f"📚 Found training: {training.course_title} (ID: {training.course_id})")
        print(f"📋 Training plan items: {len(training.training_plan) if training.training_plan else 0}")
        
        if not training.training_plan:
            print("⚠️ Training has no training_plan - cannot test progress")
            return False
            
        # Test user ID (use 1 for testing)
        test_user_id = 1
        total_items = len(training.training_plan)
        
        print(f"\n🧪 Testing with user_id: {test_user_id}, training_id: {training.id}")
        
        # Test 1: Update progress for item 0
        print("\n1️⃣ Testing progress update for item 0...")
        try:
            progress = update_training_progress(db, test_user_id, training.id, 0)
            print(f"✅ Progress updated: {progress.progress_percentage:.1f}%")
            print(f"   Completed items: {progress.completed_items}")
        except Exception as e:
            print(f"❌ Error updating progress: {e}")
            return False
            
        # Test 2: Get progress
        print("\n2️⃣ Testing progress retrieval...")
        try:
            progress = get_training_progress(db, test_user_id, training.id)
            if progress:
                print(f"✅ Progress retrieved: {progress.progress_percentage:.1f}%")
                print(f"   Completed items: {progress.completed_items}")
                print(f"   Total items: {progress.total_items}")
            else:
                print("❌ No progress found")
                return False
        except Exception as e:
            print(f"❌ Error getting progress: {e}")
            return False
            
        # Test 3: Update another item
        if total_items > 1:
            print("\n3️⃣ Testing progress update for item 1...")
            try:
                progress = update_training_progress(db, test_user_id, training.id, 1)
                print(f"✅ Progress updated: {progress.progress_percentage:.1f}%")
                print(f"   Completed items: {progress.completed_items}")
            except Exception as e:
                print(f"❌ Error updating progress: {e}")
                return False
                
        # Test 4: Try to update same item again (should not change)
        print("\n4️⃣ Testing duplicate item update...")
        try:
            progress_before = get_training_progress(db, test_user_id, training.id)
            progress_after = update_training_progress(db, test_user_id, training.id, 0)
            
            if progress_before.progress_percentage == progress_after.progress_percentage:
                print("✅ Duplicate update correctly ignored")
            else:
                print("⚠️ Duplicate update changed progress (unexpected)")
                
        except Exception as e:
            print(f"❌ Error testing duplicate: {e}")
            return False
            
        # Test 5: Reset progress
        print("\n5️⃣ Testing progress reset...")
        try:
            success = reset_training_progress(db, test_user_id, training.id)
            if success:
                print("✅ Progress reset successful")
                progress = get_training_progress(db, test_user_id, training.id)
                if progress and progress.progress_percentage == 0.0:
                    print("✅ Progress verified as reset")
                else:
                    print("❌ Progress not properly reset")
                    return False
            else:
                print("❌ Progress reset failed")
                return False
        except Exception as e:
            print(f"❌ Error resetting progress: {e}")
            return False
            
        # Test 6: Test invalid item number
        print("\n6️⃣ Testing invalid item number...")
        try:
            update_training_progress(db, test_user_id, training.id, 999)
            print("❌ Invalid item number should have failed")
            return False
        except ValueError as e:
            print(f"✅ Invalid item correctly rejected: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
            
        print("\n🎉 All tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure the database is running and migrations are applied")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_database_tables():
    """Check if required tables exist"""
    try:
        from app.database import engine
        from sqlalchemy import text
        
        print("🔍 Checking database tables...")
        
        with engine.connect() as connection:
            # Check if training_progress table exists
            result = connection.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'training_progress'
                );
            """))
            
            table_exists = result.scalar()
            
            if table_exists:
                print("✅ training_progress table exists")
                
                # Check table structure
                result = connection.execute(text("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'training_progress'
                    ORDER BY ordinal_position;
                """))
                
                columns = result.fetchall()
                print("📋 Table columns:")
                for col_name, col_type in columns:
                    print(f"   - {col_name}: {col_type}")
                    
                return True
            else:
                print("❌ training_progress table does not exist")
                print("Please run: python add_training_progress_migration.py")
                return False
                
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Training Progress Debug Tool")
    print("=" * 50)
    
    # Check database tables first
    if not check_database_tables():
        print("\n❌ Database check failed. Cannot proceed with tests.")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    
    # Run tests
    if test_progress_functions():
        print("\n✅ All diagnostics passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1) 