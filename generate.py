from jinja2 import Environment, FileSystemLoader
from urllib3 import request
import jmespath

url = "https://jenskrumsieck.de"

def get_blog_posts():
    endpoint = f"{url}/blog.json"
    res = request("GET", endpoint)
    json = res.json()
    
    posts = jmespath.search("posts.results[:5].[data.title[0].text, url]", json)
    
    return [{"url": post[1], "title": post[0]} for post in posts]

posts = get_blog_posts()

env = Environment(loader=FileSystemLoader("."))
template = env.get_template("template.md")

output = template.render(posts=posts, site_url=url)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(output)