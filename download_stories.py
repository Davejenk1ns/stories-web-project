import os
import re
import urllib.request
from urllib.error import URLError, HTTPError

# Create stories directory if it doesn't exist
os.makedirs('stories', exist_ok=True)

# List of stories and their URLs
stories = [
    ('jack-the-railroad-and-shiva-the-destroyer', 'jack'),
    ('kj-heisenberg-and-the-third-category', 'kj'),
    ('jacks-tour-abroad', 'tour'),
    ('airefrance-1267', 'airefrance1267'),  # Try alternative URL
    ('lie-detector', 'liedetector'),        # Try alternative URL
    ('village-inn', 'villageinn'),          # Try alternative URL
    ('lois', 'lois'),
    ('yamanote', 'yamanote')
]

# Alternative URLs to try if the first ones fail
alternative_urls = {
    'airefrance-1267': ['airefrance', 'air', 'france', 'flight1267', 'flight'],
    'lie-detector': ['lie', 'detector', 'liedetector'],
    'village-inn': ['village', 'inn', 'villageinn']
}

# Base URL for the Wayback Machine
base_url = 'https://web.archive.org/web/20000116230658/'

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
    # This is a simple approach and might need adjustment
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

def download_story(story_filename, story_url):
    """Download a story from the Wayback Machine"""
    url = f"{base_url}http://www.davejenkins.com/{story_url}.html"
    output_file = f"stories/{story_filename}.html"
    
    try:
        print(f"Downloading {url}...")
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
        
        # Try alternative URLs if available
        if story_filename in alternative_urls:
            for alt_url in alternative_urls[story_filename]:
                alt_full_url = f"{base_url}http://www.davejenkins.com/{alt_url}.html"
                print(f"Trying alternative URL: {alt_full_url}")
                try:
                    with urllib.request.urlopen(alt_full_url) as response:
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
                            
                        print(f"Successfully saved {output_file} using alternative URL")
                        return True
                except (HTTPError, URLError) as e:
                    print(f"Alternative URL {alt_full_url} also failed: {e}")
                except Exception as e:
                    print(f"Error with alternative URL {alt_full_url}: {e}")
    except URLError as e:
        print(f"URL Error for {url}: {e.reason}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    
    return False

# Download each story
successful = 0
for story_filename, story_url in stories:
    if download_story(story_filename, story_url):
        successful += 1

print(f"Downloaded {successful} out of {len(stories)} stories.")
