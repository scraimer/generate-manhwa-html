#!/usr/bin/env python3
"""
Generates HTML files for displaying vertically scrolling manga/manhwa chapters.
Creates a TOC page and individual chapter pages with full-screen vertical scrolling.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional
import json


def parse_chapter_number(folder_name: str) -> Tuple[float, str]:
    """
    Parse chapter number from folder name like 'Chapter_001_Chapter 001'.
    Returns (numeric_value, display_name) for sorting.
    """
    match = re.match(r'Chapter_(\d+(?:\.\d+)?)(.*)', folder_name)
    if match:
        num_str = match.group(1)
        num = float(num_str)
        display = folder_name.replace('Chapter_', '')
        return (num, display)
    return (float('inf'), folder_name)


def get_chapters(base_path: str) -> List[Tuple[str, str, str]]:
    """
    Get all chapters from base path.
    Returns list of (folder_name, display_name, full_path).
    """
    chapters = []
    base = Path(base_path)
    
    for item in base.iterdir():
        if item.is_dir() and item.name.startswith('Chapter_'):
            num, display = parse_chapter_number(item.name)
            chapters.append((item.name, display, str(item)))
    
    # Sort by chapter number
    chapters.sort(key=lambda x: parse_chapter_number(x[0])[0])
    return chapters


def get_pages(chapter_path: str) -> List[str]:
    """
    Get all image files from chapter folder, sorted.
    Supports .webp, .jpg, .jpeg, .png
    """
    chapter_dir = Path(chapter_path)
    images = []
    
    for ext in ['*.webp', '*.jpg', '*.jpeg', '*.png', '*.gif']:
        images.extend(sorted(chapter_dir.glob(ext)))
        images.extend(sorted(chapter_dir.glob(ext.upper())))
    
    return [img.name for img in sorted(set(images))]


def generate_toc_html(chapters: List[Tuple[str, str, str]], output_dir: str) -> str:
    """Generate Table of Contents HTML."""
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Table of Contents</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        
        h1 {
            text-align: center;
            margin-bottom: 40px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        
        .chapters-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .chapter-link {
            display: block;
            padding: 20px;
            background: rgba(255,255,255,0.05);
            border: 2px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            text-decoration: none;
            color: #fff;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .chapter-link:hover {
            background: rgba(255,255,255,0.1);
            border-color: rgba(255,255,255,0.3);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        
        .chapter-link h3 {
            font-size: 1.1em;
            margin-bottom: 5px;
        }
        
        .chapter-link p {
            font-size: 0.9em;
            opacity: 0.7;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Manga Reader</h1>
        <div class="chapters-grid">
'''
    
    for folder_name, display_name, _ in chapters:
        chapter_file = f"chapter_{folder_name}.html"
        html += f'''            <a href="{chapter_file}" class="chapter-link">
                <h3>{display_name}</h3>
            </a>
'''
    
    html += '''        </div>
    </div>
</body>
</html>'''
    
    return html


def generate_chapter_html(
    chapter_folder: str,
    chapter_display: str,
    pages: List[str],
    chapter_index: int,
    total_chapters: int,
    chapters: List[Tuple[str, str, str]],
    story_name: str
) -> str:
    """Generate chapter page HTML with vertical scrolling."""
    
    # Calculate previous and next chapter
    prev_chapter = None
    next_chapter = None
    next_chapter_file = None
    
    if chapter_index > 0:
        prev_chapter = chapters[chapter_index - 1][0]
    
    if chapter_index < total_chapters - 1:
        next_chapter = chapters[chapter_index + 1][0]
        next_chapter_file = f"chapter_{next_chapter}.html"
    
    # Build navigation buttons
    prev_btn = f'<a href="chapter_{prev_chapter}.html" class="nav-btn">← PREV</a>' if prev_chapter else '<button class="nav-btn" disabled>← PREV</button>'
    next_btn = f'<a href="chapter_{next_chapter}.html" class="nav-btn">NEXT →</a>' if next_chapter else '<button class="nav-btn" disabled>NEXT →</button>'
    toc_btn = '<a href="index.html" class="nav-btn toc-btn">📖 TOC</a>'
    
    # Extract chapter number from display name for title
    chapter_num = chapter_display.split('_')[0]
    
    # Build image container - reference images relative to the parent directory
    images_html = ''
    for page in pages:
        image_path = f"../{chapter_folder}/{page}"
        images_html += f'            <img src="{image_path}" alt="Page" class="manga-page">\n'
    
    # Build bottom spacer with message (only if there's a next chapter)
    spacer_html = ''
    if next_chapter:
       spacer_html = '''            <div class="bottom-spacer">
               <div class="spacer-message">scroll down to go to next chapter</div>
           </div>
'''
    
    page_count = len(pages)
    next_chapter_file_json = json.dumps(next_chapter_file) if next_chapter_file else "null"
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{story_name} - {chapter_num}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            background: #000;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow-x: hidden;
        }}
        
        .top-nav {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.8);
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 1000;
            gap: 10px;
            flex-wrap: wrap;
            transition: transform 0.3s ease;
            transform: translateY(0);
        }}
        
        .top-nav.hidden {{
            transform: translateY(-100%);
        }}
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 1000;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .chapter-title {{
            color: #fff;
            font-size: 1.2em;
            flex: 1;
            min-width: 200px;
        }}
        
        .nav-buttons {{
            display: flex;
            gap: 10px;
        }}
        
        .nav-btn {{
            padding: 8px 16px;
            background: #333;
            color: #fff;
            border: 1px solid #555;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s ease;
            font-size: 0.9em;
            white-space: nowrap;
        }}
        
        .nav-btn:hover:not(:disabled) {{
            background: #555;
            border-color: #777;
        }}
        
        .nav-btn:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        
        .toc-btn {{
            background: #1e5a7d;
        }}
        
        .toc-btn:hover {{
            background: #2d7fa6;
        }}
        
        .page-counter {{
            color: #aaa;
            font-size: 0.9em;
            padding: 8px 12px;
            background: #222;
            border-radius: 4px;
            min-width: 60px;
            text-align: center;
        }}
        
        .container {{
            margin-top: 60px;
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
            max-width: 100%;
        }}
        
        .manga-page {{
            display: block;
            width: 100%;
            max-width: 100%;
            height: auto;
            margin: 0;
            padding: 0;
        }}
        
        .bottom-spacer {{
           height: 1000px;
           display: flex;
           align-items: center;
           justify-content: center;
           background: linear-gradient(180deg, #000 0%, #1a1a1a 100%);
           border-top: 1px solid #333;
           margin-top: 20px;
        }}
        
        .spacer-message {{
           font-size: 1.3em;
           color: #888;
           text-align: center;
           font-style: italic;
        }}
        
        .bottom-nav {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.8);
            padding: 10px 20px;
            display: flex;
            justify-content: center;
            gap: 10px;
            z-index: 1000;
            flex-wrap: wrap;
        }}
        
        .progress-bar {{
            position: fixed;
            top: 0;
            left: 0;
            height: 3px;
            background: #ff6b6b;
            z-index: 999;
            transition: width 0.3s ease;
        }}
        
        @media (max-width: 768px) {{
            .top-nav {{
                flex-direction: column;
                gap: 8px;
            }}
            
            .chapter-title {{
                font-size: 1em;
            }}
            
            .nav-btn {{
                padding: 6px 12px;
                font-size: 0.8em;
            }}
            
            .bottom-nav {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="progress-bar" id="progress"></div>
    
    <div class="top-nav">
        <div class="chapter-title">{chapter_display}</div>
        <div class="nav-buttons">
            {prev_btn}
            {next_btn}
            {toc_btn}
        </div>
        <div class="page-counter"><span id="current-page">1</span>/{page_count}</div>
    </div>
    
    <div class="container" id="container">
{images_html}{spacer_html}    </div>
    
    <div class="bottom-nav">
        {prev_btn}
        {next_btn}
        {toc_btn}
    </div>
    
    <script>
        const container = document.getElementById('container');
        const progressBar = document.getElementById('progress');
        const currentPageSpan = document.getElementById('current-page');
       const topNav = document.querySelector('.top-nav');
       const images = document.querySelectorAll('.manga-page');
       const pageCount = {page_count};
       const nextChapterFile = {next_chapter_file_json};
        
       let lastScrollY = 0;
       let lastNavToggleScrollY = 0;
       let imagesLoaded = false;
       let loadedImageCount = 0;
        
       // Wait for all images to load before enabling auto-navigation
       function initializeImageLoading() {{
           if (images.length === 0) {{
               imagesLoaded = true;
               return;
           }}
            
           images.forEach(img => {{
               if (img.complete) {{
                   loadedImageCount++;
               }} else {{
                   img.addEventListener('load', () => {{
                       loadedImageCount++;
                       if (loadedImageCount === images.length) {{
                           imagesLoaded = true;
                       }}
                   }});
                   img.addEventListener('error', () => {{
                       loadedImageCount++;
                       if (loadedImageCount === images.length) {{
                           imagesLoaded = true;
                       }}
                   }});
               }}
           }});
            
           if (loadedImageCount === images.length) {{
               imagesLoaded = true;
           }}
       }}
        
       // Update progress bar and page counter
       function updateProgress() {{
           const scrollTop = window.scrollY;
           const docHeight = document.documentElement.scrollHeight - window.innerHeight;
           const scrollPercent = docHeight ? (scrollTop / docHeight) * 100 : 0;
           progressBar.style.width = scrollPercent + '%';
            
           // Find current page based on scroll position
           let currentPage = 1;
           images.forEach((img, index) => {{
               const rect = img.getBoundingClientRect();
               if (rect.top < window.innerHeight / 2) {{
                   currentPage = index + 1;
               }}
           }});
           currentPageSpan.textContent = currentPage;
            
           // Hide/show toolbar based on scroll direction and distance
           const scrollDelta = scrollTop - lastScrollY;
           const distanceFromLastToggle = Math.abs(scrollTop - lastNavToggleScrollY);
            
           if (scrollDelta > 0 && scrollTop > 400 && distanceFromLastToggle > 100) {{
               // Scrolling down and past threshold
               topNav.classList.add('hidden');
               lastNavToggleScrollY = scrollTop;
           }} else if (scrollDelta < 0 && distanceFromLastToggle > 100) {{
               // Scrolling up
               topNav.classList.remove('hidden');
               lastNavToggleScrollY = scrollTop;
           }}
            
           lastScrollY = scrollTop;
            
           // Auto-navigate to next chapter if scrolled 300px past the end (only after images load)
           if (imagesLoaded && nextChapterFile && scrollTop > docHeight - 300) {{
               window.location.href = nextChapterFile;
           }}
       }}
        
       // Keyboard navigation
       document.addEventListener('keydown', (e) => {{
           if (e.key === 'ArrowRight' || e.key === ' ') {{
               e.preventDefault();
               window.scrollBy(0, window.innerHeight * 0.8);
           }} else if (e.key === 'ArrowLeft') {{
                e.preventDefault();
                window.scrollBy(0, -window.innerHeight * 0.8);
            }}
        }});
        
        window.addEventListener('scroll', updateProgress);
        window.addEventListener('resize', updateProgress);
        
        // Initialize image loading tracking
        initializeImageLoading();
        
        // Initial update
        updateProgress();
    </script>
</body>
</html>'''
    
    return html


def generate_all_html(base_path: str, output_dir: Optional[str] = None) -> None:
    """
    Main function to generate all HTML files.
    """
    base_path = os.path.abspath(base_path)
    
    if not os.path.isdir(base_path):
        print(f"Error: {base_path} is not a valid directory")
        sys.exit(1)
    
    # Create output directory
    if output_dir is None:
        output_dir = os.path.join(base_path, 'html_output')
    
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"📚 Scanning chapters in: {base_path}")
    chapters = get_chapters(base_path)
    
    if not chapters:
        print("❌ No chapters found!")
        sys.exit(1)
    
    print(f"✅ Found {len(chapters)} chapters\n")
    
    # Generate TOC
    print("📖 Generating Table of Contents...")
    toc_html = generate_toc_html(chapters, output_dir)
    toc_path = os.path.join(output_dir, 'index.html')
    with open(toc_path, 'w', encoding='utf-8') as f:
        f.write(toc_html)
    print(f"   ✓ Saved: index.html")
    
    # Generate chapter pages
    print("📄 Generating chapter pages...")
    story_name = os.path.basename(base_path)
    for idx, (folder_name, display_name, chapter_path) in enumerate(chapters):
        pages = get_pages(chapter_path)
        
        if not pages:
            print(f"   ⚠ {display_name}: No images found, skipping")
            continue
        
        chapter_html = generate_chapter_html(
            folder_name,
            display_name,
            pages,
            idx,
            len(chapters),
            chapters,
            story_name
        )
        
        output_file = os.path.join(output_dir, f'chapter_{folder_name}.html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(chapter_html)
        
        print(f"   ✓ {display_name} ({len(pages)} pages)")
    
    print(f"\n✨ Complete! Open {os.path.join(output_dir, 'index.html')} to start reading")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python generate_manhwa_html.py <path_to_manga_folder> [output_dir]")
        print("\nExample:")
        print('  python generate_manhwa_html.py "/path/to/For My Derelict Favorite"')
        print('  python generate_manhwa_html.py "/path/to/manga" "/path/to/output"')
        sys.exit(1)
    
    base_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    generate_all_html(base_path, output_dir)
