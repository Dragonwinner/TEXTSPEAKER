#!/usr/bin/env python3
"""
Standalone script to generate videos from CSV file.

This script can be run directly without Django's manage.py.

Usage:
    python generate_videos.py sample_texts.csv
    python generate_videos.py texts.csv --output-dir my_videos
    python generate_videos.py texts.csv --avatar avatar/my_avatar.png
"""
import sys
import os
import argparse
from pathlib import Path

# Add the project to the path
sys.path.insert(0, str(Path(__file__).parent / 'videogen_backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videogen_backend.settings')

import django
django.setup()

from api.csv_processor import read_csv_texts, validate_csv_format
from api.batch_generator import batch_generate_videos


def main():
    parser = argparse.ArgumentParser(
        description='Generate videos from text entries in a CSV file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_videos.py sample_texts.csv
  python generate_videos.py texts.csv --output-dir output_videos
  python generate_videos.py texts.csv --avatar avatar/avatar.png
  python generate_videos.py texts.csv --validate-only

CSV Format:
  The CSV file should have a header row with at least a 'text' column.
  Optional columns: 'filename' (custom name for video), 'avatar' (path to avatar image)
  
  Example:
    text,filename,avatar
    "Hello world!","video1",
    "Another text","video2","custom_avatar.png"
        """
    )
    
    parser.add_argument(
        'csv_file',
        type=str,
        help='Path to the CSV file containing text entries'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='output',
        help='Directory to save generated videos (default: output/)'
    )
    
    parser.add_argument(
        '--avatar',
        type=str,
        default=None,
        help='Path to avatar image file (optional)'
    )
    
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate CSV format without generating videos'
    )
    
    args = parser.parse_args()
    
    csv_file = args.csv_file
    output_dir = Path(args.output_dir)
    avatar_path = Path(args.avatar) if args.avatar else None
    
    print('\n' + '='*60)
    print('CSV to Video Batch Generator')
    print('='*60 + '\n')
    
    # Validate CSV file
    print(f"Validating CSV file: {csv_file}")
    
    if not validate_csv_format(csv_file):
        print('\n❌ Error: Invalid CSV format. Please check the file.')
        return 1
    
    print('✓ CSV format is valid\n')
    
    if args.validate_only:
        print('✓ Validation complete (--validate-only mode)')
        return 0
    
    # Read CSV entries
    try:
        entries = read_csv_texts(csv_file)
        
        if not entries:
            print('❌ Error: No valid entries found in CSV file')
            return 1
        
        print(f"Found {len(entries)} text entries to process\n")
        
    except FileNotFoundError as e:
        print(f'❌ Error: {e}')
        return 1
    except ValueError as e:
        print(f'❌ CSV format error: {e}')
        return 1
    except Exception as e:
        print(f'❌ Error reading CSV: {e}')
        return 1
    
    # Show configuration
    print("Configuration:")
    print(f"  CSV file: {csv_file}")
    print(f"  Output directory: {output_dir}")
    if avatar_path:
        print(f"  Avatar image: {avatar_path}")
    else:
        print(f"  Avatar image: (using default)")
    
    # Generate videos
    try:
        results = batch_generate_videos(
            entries=entries,
            output_dir=output_dir,
            avatar_path=avatar_path
        )
        
        # Count successes and failures
        successful = sum(1 for r in results if r['status'] == 'success')
        failed = sum(1 for r in results if r['status'] == 'error')
        
        # Display final summary
        print('\n' + '='*60)
        if failed == 0:
            print(f'✓ All {successful} videos generated successfully!')
        else:
            print(f'⚠ Completed with {successful} successes and {failed} failures')
        
        print(f'\n📁 Output directory: {output_dir.absolute()}')
        print('='*60 + '\n')
        
        return 0 if failed == 0 else 1
        
    except Exception as e:
        print(f'❌ Error during video generation: {e}')
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
