import os
import re
import urllib.request
import time
from urllib.error import URLError, HTTPError

# Create stories directory if it doesn't exist
os.makedirs('stories', exist_ok=True)

# List of stories and their URLs to try
stories = [
    ('airefrance-1267', ['airefrance', 'air', 'france', 'flight', 'flight1267', 'af1267', 'af']),
    ('village-inn', ['village', 'inn', 'villageinn']),
    ('lois', ['lois']),
    ('yamanote', ['yamanote'])
]

# Different timestamps to try from the Wayback Machine
timestamps = [
    '20000116230658',  # Original timestamp
    '20000615000000',  # Mid-2000
    '20001215000000',  # Late 2000
    '19991215000000',  # Late 1999
    '20010115000000'   # Early 2001
]

# HTML template for the stories
html_template = '''<!DOCTYPE html>
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
</html>'''

def clean_title(title):
    """Convert filename to a proper title"""
    return title.replace('-', ' ').title()

def extract_story_content(html_content):
    """Extract the story content from the HTML"""
    # Find the content between the title and the end of the page
    match = re.search(r'<TITLE>.*?</TITLE>.*?<BODY.*?>(.*?)</BODY>', 
                     html_content, re.DOTALL | re.IGNORECASE)
    
    if match:
        content = match.group(1)
        
        # Extract just the story content (after the title)
        title_match = re.search(r'<H1>(.*?)</H1>', content, re.DOTALL | re.IGNORECASE)
        if title_match:
            # Get content after the title
            title_end = content.find('</H1>') + 5
            content = content[title_end:]
        
        return content
    return "Story content could not be extracted."

def download_story(story_filename, url_options):
    """Try to download a story using different timestamps and URL options"""
    output_file = f"stories/{story_filename}.html"
    
    # Check if the file already exists and has content
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        print(f"File {output_file} already exists and has content. Skipping.")
        return True
    
    for timestamp in timestamps:
        for url_option in url_options:
            url = f"https://web.archive.org/web/{timestamp}/http://www.davejenkins.com/{url_option}.html"
            
            try:
                print(f"Trying {url}...")
                with urllib.request.urlopen(url) as response:
                    html = response.read().decode('utf-8', errors='ignore')
                    
                    # Extract the story content
                    story_content = extract_story_content(html)
                    
                    # Get the title
                    title_match = re.search(r'<TITLE>(.*?)</TITLE>', html, re.IGNORECASE)
                    title = clean_title(story_filename)
                    if title_match:
                        title = title_match.group(1).strip()
                    
                    # Create the final HTML
                    final_html = html_template.format(
                        title=title,
                        content=story_content
                    )
                    
                    # Save the file
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(final_html)
                        
                    print(f"Successfully saved {output_file}")
                    return True
            except HTTPError as e:
                print(f"HTTP Error for {url}: {e.code}")
            except URLError as e:
                print(f"URL Error for {url}: {e.reason}")
            except Exception as e:
                print(f"Error downloading {url}: {e}")
            
            # Add a small delay to avoid rate limiting
            time.sleep(1)
    
    print(f"Failed to download {story_filename} after trying all options")
    return False

# Download each story
successful = 0
for story_filename, url_options in stories:
    if download_story(story_filename, url_options):
        successful += 1

print(f"Downloaded {successful} out of {len(stories)} remaining stories.")
