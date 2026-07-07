# Manga/Manhwa HTML Generator

A Python script that converts manga/manhwa folders into a beautifully formatted, vertically-scrolling HTML reader with full navigation controls.

## Features

✨ **Vertical Scrolling**: Read manga chapter by chapter in full-screen vertical scroll format
🎯 **Chapter Navigation**: PREV/NEXT buttons to move between chapters
📖 **Table of Contents**: Grid-based TOC page to jump to any chapter
⌨️ **Keyboard Controls**: 
   - `Right Arrow` / `Space` - Scroll down
   - `Left Arrow` - Scroll up
📊 **Progress Tracking**: Visual progress bar and page counter
📱 **Responsive Design**: Works on desktop and mobile devices
🎨 **Dark Mode UI**: Easy on the eyes reader interface

## Installation

No external dependencies required. Uses only Python's standard library.

Requires: Python 3.6+

## Usage

### Basic Usage

```bash
python generate_manhwa_html.py "/path/to/manga/folder"
```

This creates an `html_output` folder in the manga directory with all generated HTML files.

### Custom Output Directory

```bash
python generate_manhwa_html.py "/path/to/manga/folder" "/path/to/output"
```

### Example

```bash
python generate_manhwa_html.py "/home/shalom/Dropbox/backups/quests, hobbies and entertainment/manhwa/For My Derelict Favorite"
```

## Folder Structure Expected

```
Your Manga Folder/
├── Chapter_001_Name
│   ├── 001.webp
│   ├── 002.webp
│   └── ...
├── Chapter_002_Name
│   ├── 001.webp
│   └── ...
└── Chapter_NNN_Name
    └── ...
```

**Requirements:**
- Folders must be named starting with `Chapter_`
- Chapter number must come after `Chapter_` (e.g., `Chapter_001`, `Chapter_001.5`)
- Pages can be `.webp`, `.jpg`, `.jpeg`, `.png`, or `.gif` format
- Images should be numbered sequentially for proper ordering

## Generated Output

### Files Created

```
html_output/
├── index.html                          # Table of Contents
├── chapter_Chapter_001_Name.html       # Chapter 1 reader
├── chapter_Chapter_002_Name.html       # Chapter 2 reader
└── ... (one file per chapter)
```

The chapter HTML files use relative paths to reference images in the original chapter folders, so the directory structure must be preserved:

```
Your Manga Folder/
├── Chapter_001_Name/
│   ├── 001.webp
│   ├── 002.webp
│   └── ...
├── Chapter_002_Name/
│   └── ...
└── html_output/                        # Generated HTML files
    ├── index.html
    ├── chapter_Chapter_001_Name.html
    └── ...
```

### Opening the Reader

1. Open `html_output/index.html` in any web browser
2. Click on a chapter to start reading
3. Use PREV/NEXT buttons or keyboard controls to navigate

**Note:** The HTML files reference images using relative paths (`../Chapter_XXX/`) so they must remain in the `html_output` folder within the manga directory. Do not move HTML files outside this folder structure without moving the chapter folders as well.

## Features in Detail

### TOC Page

- Grid layout showing all available chapters
- Click any chapter to jump to it
- Dark theme with hover effects

### Chapter Reader

**Navigation Options:**
- **Top Navigation**: PREV/NEXT/TOC buttons and page counter
- **Bottom Navigation** (desktop only): Same controls
- **Keyboard**: Arrow keys and spacebar
- **Click Links**: Direct links to next/previous chapters

**Display Features:**
- Red progress bar at top shows reading progress
- Current page counter updates as you scroll
- Images are responsive and auto-scale
- Full-screen viewing experience

## Script Options

The script automatically:
- Sorts chapters numerically (including decimal chapters like 001.5)
- Detects all supported image formats
- Handles mixed image formats within chapters
- Generates relative image links (no external dependencies needed)

## Customization

To customize the appearance, edit the CSS section in the generated HTML files:

- **Colors**: Modify the dark theme colors in the `<style>` section
- **Fonts**: Change `font-family` in CSS
- **Navigation Position**: Adjust `.top-nav` and `.bottom-nav` styling
- **Progress Bar**: Edit `.progress-bar` color/height

## Performance Notes

- Large chapters (100+ pages) generate slightly larger HTML files (~12-15KB per chapter)
- All HTML files are self-contained and reference images by relative path
- No server required - open files directly in browser
- Works offline after generation

## Browser Compatibility

✅ Chrome/Chromium (recommended)
✅ Firefox
✅ Safari
✅ Edge
✅ Mobile browsers

## Troubleshooting

**No chapters found:**
- Ensure folders start with `Chapter_` (case-sensitive)
- Verify chapter folders are in the base directory

**Missing pages:**
- Check image files are in supported formats (.webp, .jpg, .png, .gif)
- Verify file permissions allow reading

**Images not displaying:**
- Ensure relative paths are correct
- Check HTML files are in the `html_output` folder
- Verify image files are in their original chapter folders

## Tips

1. **Backup First**: Generate in a separate output folder to preserve originals
2. **Large Collections**: Script handles 100+ chapters efficiently
3. **Mobile Reading**: Copy the entire `html_output` folder to mobile for offline reading
4. **Sharing**: Share the `html_output` folder with others to let them read the manga

## License

This script is provided as-is for personal use. Respect copyright of the manga/manhwa content.
