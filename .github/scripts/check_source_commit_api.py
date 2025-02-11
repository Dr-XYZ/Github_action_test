import os
import requests
import yaml

TRANSLATED_REPO = "mdn/translated-content"
CONTENT_REPO = "mdn/content"
TRANSLATED_PATH = "files/zh-tw"
CONTENT_PATH = "files/en-us"
README_FILE = "README.md"

GITHUB_API = "https://api.github.com/repos"
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
}

def get_file_list(repo, path):
    """使用 GitHub API 取得指定目錄下的檔案列表"""
    url = f"{GITHUB_API}/{repo}/contents/{path}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return [file["name"] for file in response.json() if file["type"] == "file" and file["name"].endswith(".md")]
    return []

def get_file_content(repo, path):
    """使用 GitHub API 取得檔案內容"""
    url = f"{GITHUB_API}/{repo}/contents/{path}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return requests.get(response.json()["download_url"]).text
    return None

def get_latest_commit(repo, path):
    """使用 GitHub API 取得檔案的最新 commit"""
    url = f"{GITHUB_API}/{repo}/commits?path={path}&per_page=1"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200 and response.json():
        return response.json()[0]["sha"]
    return None

def get_yaml_metadata(content):
    """解析 YAML metadata"""
    if content.startswith("---"):
        yaml_content = content.split("---")[1]
        return yaml.safe_load(yaml_content)
    return {}

def main():
    outdated_files = []

    # 取得所有翻譯檔案
    translated_files = get_file_list(TRANSLATED_REPO, TRANSLATED_PATH)

    for file_name in translated_files:
        translated_file_path = f"{TRANSLATED_PATH}/{file_name}"
        original_file_path = f"{CONTENT_PATH}/{file_name}"

        # 取得翻譯檔案內容
        translated_content = get_file_content(TRANSLATED_REPO, translated_file_path)
        if not translated_content:
            continue

        metadata = get_yaml_metadata(translated_content)
        source_commit = metadata.get("sourceCommit", "")

        # 取得對應的原始英文檔案最新 commit
        latest_commit = get_latest_commit(CONTENT_REPO, original_file_path)

        if source_commit and latest_commit and source_commit != latest_commit:
            outdated_files.append(f"- {file_name} (sourceCommit: {source_commit} → latest: {latest_commit})")

    # 更新 README.md
    if outdated_files:
        with open(README_FILE, "w", encoding="utf-8") as f:
            f.write("# Outdated Translations\n\n")
            f.write("以下文件的 `sourceCommit` 不是最新的，請更新翻譯：\n\n")
            f.write("\n".join(outdated_files) + "\n")

if __name__ == "__main__":
    main()