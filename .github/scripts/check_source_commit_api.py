def get_file_content(repo, path):
    """使用 GitHub API 取得檔案內容"""
    url = f"{GITHUB_API}/{repo}/contents/{path}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        download_url = response.json().get("download_url")
        if download_url:
            return requests.get(download_url).text
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
            outdated_files.add(f"- {file_name} (sourceCommit: {source_commit} → latest: {latest_commit})")

    # 更新 README.md
    if outdated_files:
        with open(README_FILE, "w", encoding="utf-8") as f:
            f.write("# Outdated Translations\n\n")
            f.write("以下文件的 `sourceCommit` 不是最新的，請更新翻譯：\n\n")
            f.write("\n".join(outdated_files) + "\n")