# Copilot Instructions for Manhwa HTML Generator

## Project Overview

This repository generates interactive HTML-based manga/manhwa readers. It transforms a folder structure of chapter directories into a web reader with table of contents, navigation, and keyboard/touch controls.

## How to Run

### Generate HTML Files

```bash
python generate_manhwa_html.py "/path/to/manga/folder"
```

This creates an `html_output` folder with the generated HTML files.

With custom output directory:
```bash
python generate_manhwa_html.py "/path/to/manga" "/path/to/output"
```

### Check for Missing Chapters

```bash
python check_missing_chapters.py "/path/to/manga/folder"
```

## Architecture

### Core Modules

**`generate_manhwa_html.py`** (880 lines)
- `parse_chapter_number(folder_name)` - Extracts chapter number from folder names (supports decimals like 001.5)
- `get_chapters(base_path)` - Scans base directory and returns sorted list of chapters
- `get_pages(chapter_path)` - Retrieves all image files from a chapter (supports .webp, .jpg, .jpeg, .png, .gif)
- `generate_toc_html(chapters, output_dir)` - Creates the table of contents page
- `generate_chapter_html(...)` - Creates individual chapter reader pages with navigation, keyboard controls, and touch swipe handling
- `generate_all_html(base_path, output_dir)` - Main orchestrator function

**`check_missing_chapters.py`** (97 lines)
- `extract_chapter_numbers(folder_path)` - Extracts chapter numbers from folder names
- `find_missing_chapters(chapter_numbers)` - Identifies gaps in chapter sequence
- Simple utility with minimal dependencies

### Data Flow

1. **Input**: Folder structure with chapters named `Chapter_XXX_Name`
2. **Processing**: Scan folders, extract chapter numbers, load images
3. **Output**: `html_output/` folder containing:
   - `index.html` - TOC with grid layout
   - `chapter_Chapter_XXX_Name.html` - Individual chapter readers with all images embedded as relative paths

### Key Design Patterns

- **Chapter Numbering**: Supports both integers and decimals (001, 001.5, 002). Sorted numerically using `float()` parsing.
- **Cross-Platform Paths**: Uses `pathlib.Path` for file operations (works on Windows/Linux/macOS)
- **Relative Image Paths**: HTML files reference images via `../Chapter_XXX/image.webp` to keep directory structure intact
- **Self-Contained HTML**: Each chapter is a complete HTML file with embedded CSS and JavaScript—no server required
- **Responsive Design**: Uses CSS Grid for TOC, viewport meta tag for mobile compatibility

## Key Conventions

1. **Chapter Folder Names**: Must start with `Chapter_` followed by the chapter number
   - Valid: `Chapter_001_Name`, `Chapter_001.5_Name`
   - Invalid: `Ch_001_Name`, `001_Name`

2. **Image File Naming**: Files must be in a chapter folder and can be any supported format
   - Sorted naturally (001.jpg before 002.jpg)
   - Case-insensitive extension matching

3. **HTML Generation**: 
   - No external dependencies (uses only Python stdlib: `os`, `re`, `sys`, `pathlib`, `typing`, `json`)
   - Files written with UTF-8 encoding
   - Output directory created with `exist_ok=True` (safe to re-run)

4. **Type Hints**: All functions use Python type hints for clarity

## Testing & Validation

No automated tests currently exist. Manual validation:

1. Test with sample chapter folders containing images
2. Verify chapter numbers are parsed and sorted correctly
3. Check that HTML output renders properly in browser
4. Validate relative paths work when folder structure is preserved

## Python Requirements

- Python 3.6+ (uses f-strings, pathlib, typing)
- No external dependencies—uses only the Python standard library

## Common Issues & Troubleshooting

**No chapters found** → Ensure folders start with `Chapter_` (case-sensitive)

**Missing images in output** → Verify:
- Images are in supported formats (.webp, .jpg, .jpeg, .png, .gif)
- Files are in the chapter folder, not the root directory
- HTML files stay in `html_output/` folder (relative paths require this)

**Image paths broken** → Check that the original chapter folder structure is preserved when moving files
