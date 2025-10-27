#!/usr/bin/env python3
"""
Base Model Cache Manager
Command-line utility for managing cached base models used in training.
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
from base_model_cache import (
    init_base_models_cache, 
    download_base_model, 
    download_all_recommended_models,
    list_cached_models, 
    cleanup_model_cache, 
    get_cache_statistics, 
    validate_cache,
    SUPPORTED_BASE_MODELS
)


def format_size(size_mb: float) -> str:
    """Format size in human-readable format."""
    if size_mb < 1024:
        return f"{size_mb:.1f} MB"
    else:
        return f"{size_mb/1024:.2f} GB"


def format_datetime(timestamp: float) -> str:
    """Format timestamp to readable datetime."""
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def cmd_status(args):
    """Show cache status and statistics."""
    print("🔍 Base Model Cache Status")
    print("=" * 50)
    
    stats = get_cache_statistics()
    
    print(f"Cache location: {Path(__file__).parent / 'base_models'}")
    print(f"Total models cached: {stats['total_models']}")
    print(f"Total cache size: {format_size(stats['total_size_mb'])}")
    print(f"Recommended models: {stats['recommended_cached']}/{stats['recommended_total']} cached")
    
    if stats['cache_created']:
        print(f"Cache created: {format_datetime(stats['cache_created'])}")
    if stats['last_updated']:
        print(f"Last updated: {format_datetime(stats['last_updated'])}")
    
    print()
    
    # List cached models
    cached_models = list_cached_models()
    if cached_models:
        print("📦 Cached Models:")
        print("-" * 50)
        for model in cached_models:
            status = "⭐ Recommended" if model['is_recommended'] else "📎 Optional"
            print(f"{model['model_name']}")
            print(f"  {status} | {format_size(model['size_mb'])}")
            print(f"  {model['description']}")
            print(f"  Cached: {format_datetime(model['cached_at'])}")
            print()
    else:
        print("📭 No models cached yet")
    
    # Validate cache
    issues = validate_cache()
    if issues:
        print("⚠️ Cache Issues Found:")
        for issue in issues:
            print(f"  • {issue}")
        print()


def cmd_list(args):
    """List available base models."""
    print("📋 Available Base Models")
    print("=" * 50)
    
    cached_models = {model['model_name'] for model in list_cached_models()}
    
    for model_name, info in SUPPORTED_BASE_MODELS.items():
        cached_status = "✅ Cached" if model_name in cached_models else "❌ Not Cached"
        recommended_status = "⭐ Recommended" if info.get('recommended') else "📎 Optional"
        
        print(f"{model_name}")
        print(f"  {info['name']} | {format_size(info['size_mb'])} | {cached_status} | {recommended_status}")
        print(f"  {info['description']}")
        print()


def cmd_download(args):
    """Download specific models or all recommended models."""
    if args.all:
        print("📥 Downloading all recommended models...")
        results = download_all_recommended_models()
        
        success_count = sum(1 for success, _ in results.values() if success)
        total_count = len(results)
        
        print("\n" + "=" * 50)
        print(f"Download Summary: {success_count}/{total_count} successful")
        
        for model_name, (success, message) in results.items():
            status = "✅" if success else "❌"
            print(f"  {status} {model_name}: {message}")
    
    elif args.models:
        for model_name in args.models:
            if model_name not in SUPPORTED_BASE_MODELS:
                print(f"⚠️ Unknown model: {model_name}")
                print(f"Available models: {', '.join(SUPPORTED_BASE_MODELS.keys())}")
                continue
            
            print(f"📥 Downloading {model_name}...")
            success, message = download_base_model(model_name, force_redownload=args.force)
            status = "✅" if success else "❌"
            print(f"  {status} {message}")
    
    else:
        print("❌ Please specify --all or provide model names")
        print("Use 'python manage_base_models.py list' to see available models")


def cmd_remove(args):
    """Remove specific models from cache."""
    if not args.models:
        print("❌ Please specify model names to remove")
        return
    
    for model_name in args.models:
        print(f"🗑️ Removing {model_name}...")
        success = cleanup_model_cache(model_name)
        if not success:
            print(f"❌ Failed to remove {model_name}")


def cmd_validate(args):
    """Validate cache integrity."""
    print("🔍 Validating cache integrity...")
    issues = validate_cache()
    
    if not issues:
        print("✅ Cache is valid - no issues found!")
    else:
        print(f"⚠️ Found {len(issues)} issues:")
        for issue in issues:
            print(f"  • {issue}")
        
        if args.fix:
            print("\n🔧 Attempting to fix issues...")
            # Re-download models with issues
            cached_models = list_cached_models()
            for model in cached_models:
                model_name = model['model_name']
                if any(model_name in issue for issue in issues):
                    print(f"📥 Re-downloading {model_name}...")
                    success, message = download_base_model(model_name, force_redownload=True)
                    status = "✅" if success else "❌"
                    print(f"  {status} {message}")


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Manage base model cache for training",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage_base_models.py status                    # Show cache status
  python manage_base_models.py list                      # List available models
  python manage_base_models.py download --all            # Download all recommended
  python manage_base_models.py download bert-base-uncased # Download specific model
  python manage_base_models.py remove bert-base-uncased  # Remove model from cache
  python manage_base_models.py validate --fix            # Validate and fix issues
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show cache status')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available models')
    
    # Download command
    download_parser = subparsers.add_parser('download', help='Download models')
    download_group = download_parser.add_mutually_exclusive_group(required=True)
    download_group.add_argument('--all', action='store_true', help='Download all recommended models')
    download_group.add_argument('models', nargs='*', help='Specific model names to download')
    download_parser.add_argument('--force', action='store_true', help='Force re-download even if cached')
    
    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove models from cache')
    remove_parser.add_argument('models', nargs='+', help='Model names to remove')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate cache integrity')
    validate_parser.add_argument('--fix', action='store_true', help='Attempt to fix issues automatically')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize cache
    init_base_models_cache()
    
    # Execute command
    command_functions = {
        'status': cmd_status,
        'list': cmd_list,
        'download': cmd_download,
        'remove': cmd_remove,
        'validate': cmd_validate
    }
    
    command_functions[args.command](args)


if __name__ == "__main__":
    main()