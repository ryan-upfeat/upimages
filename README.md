# Image Repository

This repository contains product images and tools for managing them.

## Image Inventory Management

This repository includes automated tools to keep track of all images:

### Quick Start

To generate/update the image list:

```bash
# Option 1: Use the convenience script
./update_image_list.sh

# Option 2: Run the Python script directly
python3 list_images.py
```

### Generated Files

The script creates two files:

- **`IMAGE_LIST.md`** - Human-readable markdown file with:
  - Summary of total images and file types
  - Detailed table with filenames, paths, sizes, and modification dates
  
- **`images.json`** - Machine-readable JSON file for programmatic use

### Supported Image Formats

The script automatically detects these image formats:
- Common: PNG, JPG, JPEG, GIF, BMP, WebP, SVG
- Advanced: TIFF, ICO, HEIC, HEIF, RAW, CR2, NEF, ARW, DNG

### Automation

Run the image list update script whenever you:
- Add new images to the repository
- Remove or rename images
- Want to check the current inventory

The script recursively scans all directories and skips hidden files and git directories automatically.

## Using GitHub as a CDN

This repository is designed to serve images directly from GitHub, acting as a free CDN for your images.

### Workflow

1. **Add your images** to the repository (in any directory structure you prefer)

2. **Update the image inventory**:
   ```bash
   ./update_image_list.sh
   ```

3. **Commit and push to GitHub**:
   ```bash
   git add .
   git commit -m "Add new images and update inventory"
   git push origin main
   ```

4. **Access images via GitHub URLs**:
   ```
   https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO_NAME/main/path/to/image.png
   ```

### Example URLs

For images in this repository, the URLs would be:
```
https://raw.githubusercontent.com/YOUR_USERNAME/upimages/main/oa-img/eggs-product1.png
https://raw.githubusercontent.com/YOUR_USERNAME/upimages/main/oa-img/eggs-product2.png
```

### Benefits

- ✅ **Free hosting** - GitHub provides free bandwidth for public repositories
- ✅ **Global CDN** - GitHub's infrastructure serves files worldwide
- ✅ **Version control** - Track changes to your images over time
- ✅ **Automatic inventory** - The `IMAGE_LIST.md` file provides a catalog of all available images
- ✅ **Direct linking** - Images can be embedded directly in websites, apps, or documentation

### Best Practices

- Keep image file sizes reasonable (< 25MB per file, GitHub's limit)
- Use descriptive filenames and organize in folders
- Run the inventory script before each commit to keep the catalog updated
- Consider using a `main` branch for production images and feature branches for testing