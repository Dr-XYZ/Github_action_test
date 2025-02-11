import requests

# 設定 GitHub API Token（可選，但建議使用，以提高 API 速率限制）
GITHUB_TOKEN = "your_github_personal_access_token"  # 替換為你的 Token
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

def list_github_files(owner, repo, path=""):
    """遞迴獲取 GitHub 儲存庫內所有檔案"""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"錯誤: 無法存取 {url}，HTTP 狀態碼: {response.status_code}")
        return []
    
    files = []
    for item in response.json():
        if item["type"] == "file":
            files.append(item["path"])  # 取得完整檔案路徑
        elif item["type"] == "dir":
            files.extend(list_github_files(owner, repo, item["path"]))  # 遞迴進入資料夾

    return files

# 測試範例：遞迴列出某個 GitHub 儲存庫的所有檔案
owner = "mdn"
repo = "translated-content"
all_files = list_github_files(owner, repo)

# 顯示前 10 個檔案
print("\n".join(all_files[:10]))  # 避免輸出過長