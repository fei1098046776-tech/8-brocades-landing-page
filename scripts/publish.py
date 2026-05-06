import os, shutil, re, glob
from datetime import datetime

base_url = "https://8-brocades-landing-page.vercel.app"

# Simple publication script for 8-Brocades
drafts_dir = "drafts"
blog_dir = "blog"
today = datetime.now().strftime("%B %d, %Y")

if not os.path.exists(blog_dir):
    os.makedirs(blog_dir)

drafts = sorted([f for f in os.listdir(drafts_dir) if f.endswith(".html")])

if not drafts:
    print("No drafts to publish.")
    exit(0)

next_article = drafts[0]
src = os.path.join(drafts_dir, next_article)
clean_name = re.sub(r"^\d+-", "", next_article)
dst = os.path.join(blog_dir, clean_name)

with open(src, "r") as f:
    content = f.read()

# Extract title
title_match = re.search(r'<title>(.*?)</title>', content)
title = title_match.group(1).replace(" | 8-Brocade Mastery", "") if title_match else clean_name

content = content.replace("[DATE]", today)

with open(dst, "w") as f:
    f.write(content)

# Update blog/index.html
index_path = os.path.join(blog_dir, "index.html")
if os.path.exists(index_path):
    with open(index_path, "r") as f:
        index_content = f.read()
    
    new_li = f"            <li><a href='{clean_name}'>{title}</a> - Published: {today}</li>"
    index_content = index_content.replace("<ul>", f"<ul>\n{new_li}")
    
    with open(index_path, "w") as f:
        f.write(index_content)

# Update Sitemap
files = glob.glob("**/*.html", recursive=True)
xml_urls = []
for f in files:
    if f.startswith("drafts/") or f.startswith("node_modules/"):
        continue
    url_path = f.replace("index.html", "").strip("/")
    if url_path:
        url_path = "/" + url_path
    else:
        url_path = "/"
    xml_urls.append(f"  <url>\n    <loc>{base_url}{url_path}</loc>\n    <changefreq>weekly</changefreq>\n  </url>")

sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(xml_urls)}
</urlset>"""

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap)

os.remove(src)
print(f"Successfully published {next_article} and updated sitemap.")
