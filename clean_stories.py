import os
import re
import glob

# HTML template for the stories
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #006666;
            text-align: center;
            border-bottom: 2px solid #006666;
            padding-bottom: 10px;
        }}
        .story-content {{
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            line-height: 1.8;
        }}
        a {{
            color: #006666;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .back-link {{
            margin-top: 20px;
            display: block;
            text-align: center;
        }}
        p {{
            margin-bottom: 1em;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="story-content">
{content}
    </div>
    <div class="back-link">
        <a href="../index.html">Back to Stories</a>
    </div>
</body>
</html>"""

def clean_title(filename):
    """Convert filename to a proper title"""
    base = os.path.basename(filename)
    name = os.path.splitext(base)[0]
    return name.replace('-', ' ').title()

def extract_story_content(html_content):
    """Extract just the story content from the HTML"""
    # Try to find the actual story content
    # Look for common patterns in the stories
    story_patterns = [
        r'<font size="1" face="Arial">(.*?)</font>',
        r'<FONT SIZE="1" FACE="Arial">(.*?)</FONT>',
        r'<p>(.*?)</p>',
        r'<P>(.*?)</P>'
    ]
    
    for pattern in story_patterns:
        matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
        if matches:
            # Join all matches with paragraph tags
            content = ""
            for match in matches:
                # Clean up any HTML tags within the content
                clean_match = re.sub(r'<[^>]+>', '', match).strip()
                if clean_match:
                    content += f"<p>{clean_match}</p>\n"
            
            if content:
                return content
    
    # If no patterns matched, try to extract content between specific markers
    start_markers = [
        "Just before little Jack",
        "KJ Heisenberg",
        "Monsieur Ashe",
        "The lie detector"
    ]
    
    for marker in start_markers:
        if marker in html_content:
            start_idx = html_content.find(marker)
            if start_idx != -1:
                # Extract from marker to end or next major HTML tag
                content = html_content[start_idx:]
                # Find the end of the content (before major closing tags)
                end_markers = ["</body>", "</html>", "BEGIN WAYBACK TOOLBAR"]
                for end_marker in end_markers:
                    end_idx = content.find(end_marker)
                    if end_idx != -1:
                        content = content[:end_idx].strip()
                
                # Format as paragraphs
                paragraphs = re.split(r'<p>|<P>|<br>|<BR>|\n\n', content)
                formatted_content = ""
                for para in paragraphs:
                    # Clean up any HTML tags
                    clean_para = re.sub(r'<[^>]+>', '', para).strip()
                    if clean_para:
                        formatted_content += f"<p>{clean_para}</p>\n"
                
                if formatted_content:
                    return formatted_content
    
    # If all else fails, return a placeholder
    return "<p>Story content could not be extracted properly. Please check the original source.</p>"

def get_title_from_filename(filename):
    """Get a proper title from the filename"""
    base = os.path.basename(filename)
    name = os.path.splitext(base)[0]
    
    # Map of filenames to proper titles
    title_map = {
        'jack-the-railroad-and-shiva-the-destroyer': 'Jack, The Railroad, and Shiva The Destroyer',
        'kj-heisenberg-and-the-third-category': 'KJ Heisenberg and The Third Category',
        'jacks-tour-abroad': 'Jack\'s Tour Abroad',
        'airefrance-1267': 'Airefrance #1267',
        'lie-detector': 'Lie Detector',
        'village-inn': 'Village Inn',
        'lois': 'Lois',
        'yamanote': 'Yamanote',
        'silent-observer': 'Silent Observer'
    }
    
    return title_map.get(name, name.replace('-', ' ').title())

def clean_story_file(filepath):
    """Clean up a story file to extract just the content"""
    print(f"Cleaning {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
        
        # Extract the story content
        story_content = extract_story_content(html_content)
        
        # Get the title
        title = get_title_from_filename(filepath)
        
        # Create the final HTML
        final_html = html_template.format(
            title=title,
            content=story_content
        )
        
        # Save the cleaned file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_html)
            
        print(f"Successfully cleaned {filepath}")
        return True
    except Exception as e:
        print(f"Error cleaning {filepath}: {e}")
        return False

# Clean all story files
story_files = glob.glob('stories/*.html')
successful = 0

for filepath in story_files:
    if clean_story_file(filepath):
        successful += 1

print(f"Cleaned {successful} out of {len(story_files)} story files.")
