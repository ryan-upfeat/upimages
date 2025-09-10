#!/bin/bash
# Simple script to update the image list
# Run this whenever you add new images to automatically update the inventory

echo "🔄 Updating image list..."
python3 list_images.py

echo ""
echo "📋 Files updated:"
echo "  • IMAGE_LIST.md (human-readable)"
echo "  • images.json (machine-readable)"
echo ""
echo "💡 Tip: You can also run 'python3 list_images.py' directly"
