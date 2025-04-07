import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

urls = [
    # "https://docs.openinterx.com/MAVI-API/Search/Search-Metadata/filtering",
    # "https://docs.openinterx.com/MAVI-API/Search/Search-Metadata/pagination",
    # "https://docs.openinterx.com/MAVI-API/Search/Search-video",
    # "https://docs.openinterx.com/MAVI-API/Search/Search-key-clip",
    # "https://docs.openinterx.com/MAVI-API/Video-Chat/Prompt-Examples",
    # "https://docs.openinterx.com/MAVI-API/Transcription-video",
    # "https://docs.openinterx.com/MAVI-API/Code",
    # "https://docs.openinterx.com/MAVI-API/Upload",
    # "https://docs.openinterx.com/MAVI-API/Search/Search-Metadata/",
    # "https://docs.openinterx.com/MAVI-API/Video-Chat/",
    "https://docs.openinterx.com/MAVI-API/Delete-videos"
]


def clean_filename(url):
    """Convert URL path to a clean filename"""
    parts = url.split("/")
    # Use the last two non-empty path segments to create a more descriptive filename
    segments = [
        part
        for part in parts
        if part and part != "https:" and "openinterx.com" not in part
    ]
    if len(segments) >= 2:
        filename = f"{segments[-2]}-{segments[-1]}"
    elif len(segments) == 1:
        filename = segments[0]
    else:
        filename = "index"
    return f"{filename}.md"


def setup_selenium():
    """Set up and return a headless browser"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def extract_content_with_selenium(url, driver):
    """Extract content using Selenium for JavaScript-rendered pages"""
    print(f"Loading {url} with Selenium...")
    driver.get(url)

    # Wait for JavaScript to render content
    time.sleep(3)

    # Get the page source after JavaScript execution
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Look for main content - adjust selectors based on the site structure
    content_selectors = [
        "main",
        "article",
        "div.theme-doc-markdown",  # Common in Docusaurus sites
        "div.content",
        "div.container",
    ]

    main_content = None
    for selector in content_selectors:
        main_content = soup.select_one(selector)
        if (
            main_content and len(main_content.text.strip()) > 100
        ):  # Ensure we got meaningful content
            break

    if not main_content:
        return f"# Content from {url}\n\nCould not extract structured content. Please check the original page."

    # Extract the title
    title = soup.find("h1")
    title_text = (
        title.text.strip() if title else url.split("/")[-1].replace("-", " ").title()
    )

    # Start with the title
    markdown = f"# {title_text}\n\n"

    # Process content elements
    for element in main_content.find_all(
        [
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "p",
            "pre",
            "code",
            "ul",
            "ol",
            "li",
            "img",
        ]
    ):
        if element.name.startswith("h"):
            level = int(element.name[1])
            markdown += f"{'#' * level} {element.text.strip()}\n\n"
        elif element.name == "p":
            markdown += f"{element.text.strip()}\n\n"
        elif element.name == "pre":
            code = element.find("code")
            if code:
                language = (
                    code.get("class", [""])[0].replace("language-", "")
                    if code.get("class")
                    else ""
                )
                markdown += f"```{language}\n{code.text.strip()}\n```\n\n"
            else:
                markdown += f"```\n{element.text.strip()}\n```\n\n"
        elif element.name == "code" and element.parent.name != "pre":
            markdown += f"`{element.text.strip()}`"
        elif element.name == "ul" or element.name == "ol":
            # We'll handle list items individually
            continue
        elif element.name == "li":
            parent = element.find_parent("ol")
            if parent:
                # Check if this is an ordered list item
                index = 1
                for sibling in parent.find_all("li"):
                    if sibling == element:
                        break
                    index += 1
                markdown += f"{index}. {element.text.strip()}\n"
            else:
                # Unordered list item
                # Determine nesting level
                nesting = 0
                parent = element.parent
                while parent and (parent.name == "ul" or parent.name == "ol"):
                    nesting += 1
                    parent = parent.parent
                indent = "  " * (nesting - 1)
                markdown += f"{indent}- {element.text.strip()}\n"
        elif element.name == "img":
            alt_text = element.get("alt", "image")
            src = element.get("src", "")
            if src and src.startswith("/"):
                src = f"https://docs.openinterx.com{src}"
            markdown += f"![{alt_text}]({src})\n\n"

    # Add source URL at the end
    markdown += f"\n\n*Source: {url}*\n"

    return markdown


# Ensure context directory exists
os.makedirs("context", exist_ok=True)

try:
    # Set up Selenium
    driver = setup_selenium()

    # Download each URL and save as markdown
    for url in urls:
        try:
            print(f"Processing {url}...")

            # Extract content using Selenium
            markdown_content = extract_content_with_selenium(url, driver)

            # Create a clean filename
            filename = clean_filename(url)
            filepath = os.path.join("context", filename)

            # Save to file
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(markdown_content)

            print(f"Saved to {filepath}")

        except Exception as e:
            print(f"Error processing {url}: {e}")

    print("Download complete!")

finally:
    # Ensure browser is closed
    if "driver" in locals():
        driver.quit()
