"""
Django management command to generate videos from CSV file.

Usage:
    python manage.py generate_videos_from_csv <csv_file> [options]

Examples:
    python manage.py generate_videos_from_csv sample_texts.csv
    python manage.py generate_videos_from_csv texts.csv --output-dir /path/to/output
    python manage.py generate_videos_from_csv texts.csv --avatar /path/to/avatar.png
"""
from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
from api.csv_processor import read_csv_texts, validate_csv_format
from api.batch_generator import batch_generate_videos


class Command(BaseCommand):
    help = 'Generate videos from text entries in a CSV file'

    def add_arguments(self, parser):
        # Positional argument
        parser.add_argument(
            'csv_file',
            type=str,
            help='Path to the CSV file containing text entries'
        )
        
        # Optional arguments
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
            help='Path to avatar image file (default: avatar/avatar.png)'
        )
        
        parser.add_argument(
            '--validate-only',
            action='store_true',
            help='Only validate CSV format without generating videos'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        output_dir = Path(options['output_dir'])
        avatar_path = Path(options['avatar']) if options['avatar'] else None
        validate_only = options['validate_only']
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('CSV to Video Batch Generator'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))
        
        # Validate CSV file
        self.stdout.write(f"Validating CSV file: {csv_file}")
        
        if not validate_csv_format(csv_file):
            raise CommandError(f'Invalid CSV format. Please check the file.')
        
        self.stdout.write(self.style.SUCCESS('✓ CSV format is valid\n'))
        
        if validate_only:
            self.stdout.write(self.style.SUCCESS('Validation complete (--validate-only mode)'))
            return
        
        # Read CSV entries
        try:
            entries = read_csv_texts(csv_file)
            
            if not entries:
                raise CommandError('No valid entries found in CSV file')
            
            self.stdout.write(f"Found {len(entries)} text entries to process\n")
            
        except FileNotFoundError as e:
            raise CommandError(str(e))
        except ValueError as e:
            raise CommandError(f'CSV format error: {e}')
        except Exception as e:
            raise CommandError(f'Error reading CSV: {e}')
        
        # Show configuration
        self.stdout.write("Configuration:")
        self.stdout.write(f"  CSV file: {csv_file}")
        self.stdout.write(f"  Output directory: {output_dir}")
        if avatar_path:
            self.stdout.write(f"  Avatar image: {avatar_path}")
        else:
            self.stdout.write(f"  Avatar image: (using default)")
        
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
            self.stdout.write('\n' + '='*60)
            if failed == 0:
                self.stdout.write(self.style.SUCCESS(
                    f'✓ All {successful} videos generated successfully!'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'⚠ Completed with {successful} successes and {failed} failures'
                ))
            
            self.stdout.write(self.style.SUCCESS(f'\nOutput directory: {output_dir.absolute()}'))
            self.stdout.write('='*60 + '\n')
            
        except Exception as e:
            raise CommandError(f'Error during video generation: {e}')
