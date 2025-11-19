#!/usr/bin/env python3
"""
Test script to verify CSV video generation functionality.

This script runs basic tests to ensure the system is working correctly.
"""
import sys
import os
from pathlib import Path
import tempfile
import shutil

# Add the project to the path
sys.path.insert(0, str(Path(__file__).parent / 'videogen_backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videogen_backend.settings')

import django
django.setup()

from api.csv_processor import read_csv_texts, validate_csv_format
from api.batch_generator import batch_generate_videos


def test_csv_validation():
    """Test CSV validation with sample file."""
    print("\n[Test 1] CSV Validation")
    print("-" * 40)
    
    csv_path = "sample_texts.csv"
    if not Path(csv_path).exists():
        print("❌ FAIL: sample_texts.csv not found")
        return False
    
    is_valid = validate_csv_format(csv_path)
    if is_valid:
        print("✓ PASS: CSV validation successful")
        return True
    else:
        print("❌ FAIL: CSV validation failed")
        return False


def test_csv_reading():
    """Test reading entries from CSV."""
    print("\n[Test 2] CSV Reading")
    print("-" * 40)
    
    csv_path = "sample_texts.csv"
    try:
        entries = read_csv_texts(csv_path)
        
        if not entries:
            print("❌ FAIL: No entries read from CSV")
            return False
        
        print(f"✓ PASS: Read {len(entries)} entries from CSV")
        
        # Check first entry has required fields
        if 'text' not in entries[0] or 'filename' not in entries[0]:
            print("❌ FAIL: Entries missing required fields")
            return False
        
        print(f"✓ PASS: Entries have correct structure")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Error reading CSV: {e}")
        return False


def test_video_generation():
    """Test generating a single video."""
    print("\n[Test 3] Video Generation")
    print("-" * 40)
    
    # Create temporary directory for test output
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        try:
            # Read first entry from sample CSV
            entries = read_csv_texts("sample_texts.csv")
            if not entries:
                print("❌ FAIL: No entries to test")
                return False
            
            test_entry = entries[0:1]  # Just test first entry
            
            print(f"Generating test video...")
            results = batch_generate_videos(
                entries=test_entry,
                output_dir=temp_path,
                avatar_path=None
            )
            
            if not results:
                print("❌ FAIL: No results returned")
                return False
            
            result = results[0]
            
            if result['status'] != 'success':
                print(f"❌ FAIL: Video generation failed: {result.get('error', 'Unknown error')}")
                return False
            
            # Check video file exists
            video_path = Path(result['video_path'])
            if not video_path.exists():
                print(f"❌ FAIL: Video file not created at {video_path}")
                return False
            
            # Check video file is not empty
            if video_path.stat().st_size == 0:
                print(f"❌ FAIL: Video file is empty")
                return False
            
            print(f"✓ PASS: Video generated successfully")
            print(f"  Video size: {video_path.stat().st_size} bytes")
            return True
            
        except Exception as e:
            print(f"❌ FAIL: Error during video generation: {e}")
            import traceback
            traceback.print_exc()
            return False


def test_avatar_image():
    """Test avatar image exists."""
    print("\n[Test 4] Avatar Image")
    print("-" * 40)
    
    avatar_path = Path("videogen_backend/avatar/avatar.png")
    
    if not avatar_path.exists():
        print("❌ FAIL: Avatar image not found")
        return False
    
    if avatar_path.stat().st_size == 0:
        print("❌ FAIL: Avatar image is empty")
        return False
    
    print("✓ PASS: Avatar image exists and is valid")
    return True


def main():
    """Run all tests."""
    print("="*60)
    print("CSV Video Generation - Test Suite")
    print("="*60)
    
    tests = [
        test_csv_validation,
        test_csv_reading,
        test_avatar_image,
        test_video_generation,
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"\n❌ EXCEPTION in {test_func.__name__}: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All tests passed!")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
