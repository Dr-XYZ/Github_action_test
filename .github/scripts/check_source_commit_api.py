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
    print(url)
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return [file["name"] for file in response.json() if file["type"] == "file" and file["name"].endswith(".md")]
    except requests.RequestException as e:
        print(f"Error fetching file list from {repo} at {path}: {e}")
    return []

def get_file_content(repo, path):
    """使用 GitHub API 取得檔案內容"""
    url = f"{GITHUB_API}/{repo}/contents/{path}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        download_url = response.json().get("download_url")
        if download_url:
            return requests.get(download_url).text
    except requests.RequestException as e:
        print(f"Error fetching file content from {repo} at {path}: {e}")
    return None

def get_latest_commit(repo, path):
    """使用 GitHub API 取得檔案的最新 commit"""
    url = f"{GITHUB_API}/{repo}/commits?path={path}&per_page=1"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        commits = response.json()
        if commits:
            return commits[0]["sha"]
    except requests.RequestException as e:
        print(f"Error fetching latest commit for {path} in {repo}: {e}")
    return None

def get_yaml_metadata(content):
    """解析 YAML metadata"""
    if content.startswith("---"):
        try:
            yaml_content = content.split("---")[1]
            return yaml.safe_load(yaml_content) or {}
        except yaml.YAMLError as e:
            print(f"YAML 解析錯誤: {e}")
    return {}

def main():
    outdated_files = set()  # 使用 set 去重
    print("開始獲取翻譯檔案列表...")
    
    # 取得所有翻譯檔案
    translated_files = get_file_list(TRANSLATED_REPO, TRANSLATED_PATH)
    if not translated_files:
        print("未找到任何翻譯檔案。")
    
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
            outdated_files.add(f"- {file_name} (sourceCommit: {source_commit} → latest: {latest_commit})")

    # 更新 README.md
    if outdated_files:
        print(f"發現 {len(outdated_files)} 個過時的翻譯檔案，開始更新 README.md...")
        with open(README_FILE, "w", encoding="utf-8") as f:
            f.write("# Outdated Translations\n\n")
            f.write("以下文件的 `sourceCommit` 不是最新的，請更新翻譯：\n\n")
            f.write("\n".join(outdated_files) + "\n")
    else:
        print("未發現過時的翻譯檔案。")

if __name__ == "__main__":
    main()