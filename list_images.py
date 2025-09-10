#!/usr/bin/env python3
"""
Image Lister Script
Automatically scans the repository for all image files and generates a comprehensive list.
"""

import os
import json
import subprocess
import re
from pathlib import Path
from datetime import datetime

# Supported image extensions
IMAGE_EXTENSIONS = {
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg', 
    '.tiff', '.tif', '.ico', '.heic', '.heif', '.raw', '.cr2', 
    '.nef', '.arw', '.dng'
}

def get_github_info():
    """Get GitHub repository information from git remote"""
    try:
        result = subprocess.run(['git', 'remote', '-v'], 
                              capture_output=True, text=True, check=True)
        
        # Parse the remote URL to extract owner and repo name
        for line in result.stdout.split('\n'):
            if 'origin' in line and '(fetch)' in line:
                # Handle both SSH and HTTPS formats
                if 'git@github.com:' in line:
                    # SSH format: git@github.com:owner/repo.git
                    match = re.search(r'git@github\.com:([^/]+)/([^\.]+)\.git', line)
                elif 'https://github.com/' in line:
                    # HTTPS format: https://github.com/owner/repo.git
                    match = re.search(r'https://github\.com/([^/]+)/([^\.]+)\.git', line)
                else:
                    continue
                    
                if match:
                    owner, repo = match.groups()
                    return owner, repo
        
        return None, None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None, None

def get_current_branch():
    """Get the current git branch"""
    try:
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip() or 'main'
    except (subprocess.CalledProcessError, FileNotFoundError):
        return 'main'

def get_file_size_human_readable(size_bytes):
    """Convert bytes to human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def scan_for_images(root_dir, github_owner=None, github_repo=None, branch='main'):
    """Scan directory recursively for image files"""
    images = []
    root_path = Path(root_dir)
    
    for file_path in root_path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS:
            # Skip hidden files and .git directory
            if any(part.startswith('.') for part in file_path.parts):
                continue
                
            stat = file_path.stat()
            relative_path = file_path.relative_to(root_path)
            
            # Generate GitHub CDN URL if we have repo info
            cdn_url = None
            if github_owner and github_repo:
                cdn_url = f"https://raw.githubusercontent.com/{github_owner}/{github_repo}/{branch}/{relative_path}"
            
            images.append({
                'filename': file_path.name,
                'path': str(relative_path),
                'full_path': str(file_path),
                'cdn_url': cdn_url,
                'size_bytes': stat.st_size,
                'size_human': get_file_size_human_readable(stat.st_size),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'extension': file_path.suffix.lower()
            })
    
    # Sort by path for consistent ordering
    images.sort(key=lambda x: x['path'])
    return images

def generate_markdown_list(images, output_file, github_owner=None, github_repo=None, branch='main'):
    """Generate a markdown file with the image list"""
    with open(output_file, 'w') as f:
        f.write("# Image Inventory\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total images found: **{len(images)}**\n\n")
        
        if github_owner and github_repo:
            f.write(f"**Repository:** `{github_owner}/{github_repo}` (branch: `{branch}`)\n\n")
        
        if not images:
            f.write("No images found in the repository.\n")
            return
        
        # Summary by extension
        extensions = {}
        total_size = 0
        for img in images:
            ext = img['extension']
            extensions[ext] = extensions.get(ext, 0) + 1
            total_size += img['size_bytes']
        
        f.write("## Summary\n\n")
        f.write("| Extension | Count |\n")
        f.write("|-----------|-------|\n")
        for ext, count in sorted(extensions.items()):
            f.write(f"| {ext} | {count} |\n")
        f.write(f"\n**Total size:** {get_file_size_human_readable(total_size)}\n\n")
        
        # Detailed list with CDN URLs
        if github_owner and github_repo:
            f.write("## Live CDN URLs\n\n")
            f.write("| Filename | CDN URL | Size | Modified |\n")
            f.write("|----------|---------|------|----------|\n")
            
            for img in images:
                modified_date = datetime.fromisoformat(img['modified']).strftime('%Y-%m-%d')
                f.write(f"| {img['filename']} | {img['cdn_url']} | {img['size_human']} | {modified_date} |\n")
            f.write("\n")
        
        # Local paths
        f.write("## Local Paths\n\n")
        f.write("| Filename | Path | Size | Modified |\n")
        f.write("|----------|------|------|----------|\n")
        
        for img in images:
            modified_date = datetime.fromisoformat(img['modified']).strftime('%Y-%m-%d')
            f.write(f"| {img['filename']} | {img['path']} | {img['size_human']} | {modified_date} |\n")

def generate_json_list(images, output_file):
    """Generate a JSON file with the image list"""
    data = {
        'generated_at': datetime.now().isoformat(),
        'total_count': len(images),
        'images': images
    }
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    """Main function"""
    script_dir = Path(__file__).parent
    
    # Get GitHub repository information
    github_owner, github_repo = get_github_info()
    branch = get_current_branch()
    
    print("🔍 Scanning for images...")
    if github_owner and github_repo:
        print(f"📡 Detected GitHub repo: {github_owner}/{github_repo} (branch: {branch})")
    
    images = scan_for_images(script_dir, github_owner, github_repo, branch)
    
    print(f"📸 Found {len(images)} images")
    
    # Generate markdown list
    markdown_file = script_dir / "IMAGE_LIST.md"
    generate_markdown_list(images, markdown_file, github_owner, github_repo, branch)
    print(f"📝 Generated markdown list: {markdown_file}")
    
    # Generate JSON list
    json_file = script_dir / "images.json"
    generate_json_list(images, json_file)
    print(f"📋 Generated JSON list: {json_file}")
    
    print("\n✅ Image listing complete!")
    
    if github_owner and github_repo and images:
        print(f"\n🌐 Live CDN URLs available:")
        for img in images[:3]:  # Show first 3 as examples
            print(f"  • {img['cdn_url']}")
        if len(images) > 3:
            print(f"  • ... and {len(images) - 3} more (see IMAGE_LIST.md)")
    
    if images:
        print(f"\nFound images in these directories:")
        dirs = set(str(Path(img['path']).parent) for img in images)
        for directory in sorted(dirs):
            if directory == '.':
                directory = 'root'
            print(f"  • {directory}")

if __name__ == "__main__":
    main()
