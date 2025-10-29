
import json
import requests
from bs4 import BeautifulSoup

def scrape_linktree_data(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    script_tag = soup.find('script', {'id': '__NEXT_DATA__'})

    if not script_tag:
        raise ValueError("Could not find the __NEXT_DATA__ script tag.")

    json_data = json.loads(script_tag.string)

    account_data = json_data['props']['pageProps']['account']

    profile_picture_url = account_data['profilePictureUrl']
    username = account_data['username']
    social_links = account_data['socialLinks']
    links = account_data['links']

    return {
        'profile_picture_url': profile_picture_url,
        'username': username,
        'social_links': social_links,
        'links': links
    }

def download_profile_picture(url, filename='profile_picture.jpg'):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    else:
        print(f"Failed to download profile picture. Status code: {response.status_code}")

def generate_html(data):
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['username']} | Linktree Clone</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div id="container">
        <img src="profile_picture.jpg" alt="Profile Picture" id="profile-picture">
        <h1>@{data['username']}</h1>
        <div id="social-icons">
"""
    for social in data['social_links']:
        html_content += f'            <a href="{social["url"]}" target="_blank"><img src="https://cdn.simpleicons.org/{social["type"].lower()}" alt="{social["type"]}"></a>\n'

    html_content += """
        </div>
        <div id="links">
"""
    for link in data['links']:
        html_content += f'            <a href="{link["url"]}" class="link" target="_blank">{link["title"]}</a>\n'

    html_content += """
        </div>
    </div>
</body>
</html>
"""
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

def generate_css():
    css_content = """
body {
    background-color: #5C2023;
    color: white;
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

#container {
    text-align: center;
    background-color: #B13834;
    padding: 2em;
    border-radius: 10px;
    width: 80%;
    max-width: 600px;
}

#profile-picture {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    border: 3px solid white;
}

#social-icons {
    margin: 1em 0;
}

#social-icons a {
    margin: 0 0.5em;
}

#social-icons img {
    width: 32px;
    height: 32px;
    filter: invert(1);
}

#links {
    display: flex;
    flex-direction: column;
    gap: 1em;
}

.link {
    background-color: white;
    color: #5C2023;
    padding: 1em;
    text-decoration: none;
    border-radius: 5px;
    font-weight: bold;
    transition: background-color 0.3s;
}

.link:hover {
    background-color: #ddd;
}
"""
    with open('style.css', 'w', encoding='utf-8') as f:
        f.write(css_content)

if __name__ == '__main__':
    scraped_data = scrape_linktree_data('linktree.html')
    download_profile_picture(scraped_data['profile_picture_url'])
    generate_html(scraped_data)
    generate_css()
    print("Successfully generated index.html and style.css")
