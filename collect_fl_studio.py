import json
import csv
import random

POSTS_FILE = "FL_Studio2.json"
COMMENTS_FILES = [
    "FL_Studio_comments.json",
    "FL_Studio_comments2.json"
]
OUTPUT_FILE = "fl_studio_dataset.csv"

TARGET_POSTS = 100
TARGET_COMMENTS = 100


def clean_text(text):
    if not text:
        return ""

    text = text.strip()

    if text in ["[deleted]", "[removed]"]:
        return ""

    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")

    return text


def extract_posts(data):
    posts = []

    for item in data.get("data", {}).get("children", []):
        post = item.get("data", {})

        title = clean_text(post.get("title", ""))
        body = clean_text(post.get("selftext", ""))

        if not title and not body:
            continue

        if body:
            text = f"{title}\n\n{body}"
        else:
            text = title

        posts.append(text)

    return posts


def extract_comments(data):
    comments = []

    for item in data.get("data", {}).get("children", []):
        if item.get("kind") != "t1":
            continue

        comment = item.get("data", {})
        body = clean_text(comment.get("body", ""))

        if body:
            comments.append(body)

    return comments


def main():
    print("Reading comments...")

    comments = []

    for comments_file in COMMENTS_FILES:
        with open(comments_file, "r", encoding="utf-8") as file:
            comment_data = json.load(file)
    comments.extend(extract_comments(comment_data))

    print("JSON files loaded successfully.")

    with open(POSTS_FILE, "r", encoding="utf-8") as file:
        post_data = json.load(file)

    posts = extract_posts(post_data)

    # Remove duplicate entries
    posts = list(dict.fromkeys(posts))
    comments = list(dict.fromkeys(comments))

    print(f"Usable posts found: {len(posts)}")
    print(f"Usable comments found: {len(comments)}")

    if len(posts) < TARGET_POSTS:
        print(f"WARNING: Only {len(posts)} usable posts were found.")

    if len(comments) < TARGET_COMMENTS:
        print(f"WARNING: Only {len(comments)} usable comments were found.")

    # Select the requested number
    selected_posts = posts[:TARGET_POSTS]
    selected_comments = comments[:TARGET_COMMENTS]

    dataset = []

    for text in selected_posts:
        dataset.append({
            "text": text,
            "label": "",
            "notes": ""
        })

    for text in selected_comments:
        dataset.append({
            "text": text,
            "label": "",
            "notes": ""
        })

    # Shuffle posts and comments together
    random.shuffle(dataset)

    # Write final CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["text", "label", "notes"]
        )

        writer.writeheader()
        writer.writerows(dataset)

    print("\nDataset created successfully!")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Total examples: {len(dataset)}")
    print(f"Posts: {len(selected_posts)}")
    print(f"Comments: {len(selected_comments)}")


if __name__ == "__main__":
    main()