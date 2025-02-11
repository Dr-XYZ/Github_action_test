import os
import requests
import yaml

# 常數設定
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

def join_path(a, b):
    """
    用來以正斜線合併路徑（確保 repo 內路徑格式正確）
    """
    return a + "/" + b if a else b

def get_file_list(repo, base_path, relative_path=""):
    """
    遞迴取得 GitHub repo 指定目錄下所有檔案的相對路徑
    :param repo: GitHub repository (例如 "mdn/translated-content")
    :param base_path: 基底路徑 (例如 "files/zh-tw")
    :param relative_path: 遞迴用的相對路徑
    :return: 檔案相對路徑列表
    """
    full_path = join_path(base_path, relative_path) if relative_path else base_path
    url = f"{GITHUB_API}/{repo}/contents/{full_path}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"取得 {repo} 在 {full_path} 的檔案列表時發生錯誤: {e}")
        return []
    items = response.json()
    file_list = []
    for item in items:
        if item.get("type") == "dir":
            new_rel = join_path(relative_path, item.get("name"))
            file_list.extend(get_file_list(repo, base_path, new_rel))
        elif item.get("type") == "file":
            file_rel = join_path(relative_path, item.get("name"))
            file_list.append(file_rel)
    return file_list

def get_file_content(repo, file_path):
    """
    透過 GitHub API 取得檔案內容
    :param repo: GitHub repository (例如 "mdn/translated-content")
    :param file_path: 檔案在 repo 內的完整路徑 (例如 "files/zh-tw/some/file.md")
    :return: 檔案內容字串，若發生錯誤則回傳 None
    """
    url = f"{GITHUB_API}/{repo}/contents/{file_path}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        download_url = data.get("download_url")
        if download_url:
            file_response = requests.get(download_url)
            file_response.raise_for_status()
            return file_response.text
    except requests.RequestException as e:
        print(f"取得 {repo} 在 {file_path} 的檔案內容時發生錯誤: {e}")
    return None

def get_latest_commit(repo, file_path):
    """
    使用 GitHub API 取得指定檔案的最新 commit SHA
    :param repo: GitHub repository (例如 "mdn/content")
    :param file_path: 檔案在 repo 內的完整路徑 (例如 "files/en-us/some/file.md")
    :return: 最新 commit 的 SHA 字串，若無法取得則回傳 None
    """
    url = f"https://api.github.com/repos/{repo}/commits"
    params = {"path": file_path, "per_page": 1}
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        commits = response.json()
        if commits:
            return commits[0].get("sha")
    except requests.RequestException as e:
        print(f"取得 {repo} 在 {file_path} 的最新 commit 時發生錯誤: {e}")
    return None

def get_yaml_metadata(content):
    """
    解析檔案內容中 YAML 格式的 metadata
    預期檔案內容開頭會有 YAML front matter (以 --- 分隔)
    :param content: 檔案內容字串
    :return: 解析後的 dictionary，若解析失敗則回傳空 dict
    """
    if content.startswith("---"):
        try:
            # 根據 YAML front matter 的格式，第一個 '---' 之後即是 YAML 內容
            parts = content.split("---")
            if len(parts) >= 3:
                yaml_content = parts[1]
                return yaml.safe_load(yaml_content) or {}
        except yaml.YAMLError as e:
            print(f"YAML 解析錯誤: {e}")
    return {}

def main():
    outdated_files = set()  # 使用 set 去除重複項目
    print("開始獲取翻譯檔案列表...")
    
    # 取得所有翻譯檔案（取得的是從 TRANSLATED_PATH 目錄下的相對路徑）
    translated_files = get_file_list(TRANSLATED_REPO, TRANSLATED_PATH)
    print(f"共找到 {len(translated_files)} 個翻譯檔案。")
    
    for file_name in translated_files:
        # 組合完整路徑（注意：檔案在 repo 中的完整路徑為 base_path + relative path）
        translated_file_path = join_path(TRANSLATED_PATH, file_name)
        original_file_path = join_path(CONTENT_PATH, file_name)
        
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
            print(f"檔案 {file_name} 過時：sourceCommit {source_commit} != latest {latest_commit}")
    
    # 更新 README.md 檔案，列出所有過時的翻譯檔案
    if outdated_files:
        print(f"發現 {len(outdated_files)} 個過時的翻譯檔案，開始更新 {README_FILE}...")
        try:
            with open(README_FILE, "w", encoding="utf-8") as f:
                f.write("# Outdated Translations\n\n")
                f.write("以下文件的 `sourceCommit` 不是最新的，請更新翻譯：\n\n")
                # 排序後寫入每個檔案資訊
                f.write("\n".join(sorted(outdated_files)) + "\n")
            print(f"{README_FILE} 更新完成。")
        except Exception as e:
            print(f"更新 {README_FILE} 時發生錯誤: {e}")
    else:
        print("未發現過時的翻譯檔案。")

if __name__ == "__main__":
    main()
