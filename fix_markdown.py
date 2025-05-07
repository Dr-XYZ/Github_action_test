import re
import os
import glob

def correct_spacing(text):
    # 先提取所有 Markdown 超連結，保存原始格式
    link_pattern = r'\[([^\]]*)\]\(([^\)]*)\)'
    links = []
    
    def store_link(match):
        links.append(match.group(0))  # 保存原始超連結
        return f'__LINK_{len(links)-1}__'  # 替換為臨時標記
    
    # 將超連結替換為臨時標記
    text = re.sub(link_pattern, store_link, text)
    
    # 定義中文字符的正則範圍（簡化為常用漢字範圍）
    chinese_char = r'[\u4e00-\u9fff]'
    # 定義英文字符（包括字母和數字）
    english_char = r'[a-zA-Z0-9]'
    
    # 修正中英之間的空格：確保有 1 個空格
    text = re.sub(f'({chinese_char})({english_char})', r'\1 \2', text)
    text = re.sub(f'({english_char})({chinese_char})', r'\1 \2', text)
    
    # 修正中文之間的空格：移除多餘空格
    text = re.sub(f'({chinese_char})\s+({chinese_char})', r'\1\2', text)
    
    # 恢復超連結並處理顯示文字
    for i, link in enumerate(links):
        # 提取超連結的顯示文字和 URL
        match = re.match(r'\[([^\]]*)\]\(([^\)]*)\)', link)
        if match:
            display_text = match.group(1)
            url = match.group(2)
            # 修正顯示文字的空格
            corrected_display = re.sub(f'({chinese_char})({english_char})', r'\1 \2', display_text)
            corrected_display = re.sub(f'({english_char})({chinese_char})', r'\1 \2', corrected_display)
            corrected_display = re.sub(f'({chinese_char})\s+({chinese_char})', r'\1\2', corrected_display)
            # 重新構建超連結
            corrected_link = f'[{corrected_display}]({url})'
            # 替換回臨時標記
            text = text.replace(f'__LINK_{i}__', corrected_link)
    
    # 額外處理超連結前後的中文間空格
    # 情況1：中文[超連結]中文
    text = re.sub(f'({chinese_char})\s*\[([^\]]*)\]\(([^\)]*)\)\s*({chinese_char})', r'\1[\2](\3)\4', text)
    # 情況2：中文 [超連結]中文
    text = re.sub(f'({chinese_char})\s+\[([^\]]*)\]\(([^\)]*)\)\s*({chinese_char})', r'\1[\2](\3)\4', text)
    # 情況3：中文[超連結] 中文
    text = re.sub(f'({chinese_char})\s*\[([^\]]*)\]\(([^\)]*)\)\s+({chinese_char})', r'\1[\2](\3)\4', text)
    
    return text

def process_markdown_files():
    # 查找所有 .md 文件
    markdown_files = glob.glob('**/*.md', recursive=True)
    modified = False
    
    for file_path in markdown_files:
        # 讀取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # 修正內容
        corrected_content = correct_spacing(original_content)
        
        # 如果內容有變化，則寫回文件
        if corrected_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(corrected_content)
            print(f"已修正文件：{file_path}")
            modified = True
        else:
            print(f"文件無需修正：{file_path}")
    
    return modified

if __name__ == "__main__":
    # 執行批量處理
    modified = process_markdown_files()
    if modified:
        print("有文件被修正，請檢查 git 變更。")
    else:
        print("所有文件均符合格式要求，無需修正。")