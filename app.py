from flask import Flask, request, jsonify, render_template, send_file
from generator.documentation import DocumentationGenerator
import threading
import webbrowser
import time

app = Flask(__name__)

# 设置OpenAI API密钥
OPENAI_API_KEY = ""

# 初始化文档生成器
doc_generator = DocumentationGenerator(OPENAI_API_KEY)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate-docs', methods=['POST'])
def generate_docs():
    try:
        data = request.get_json()
        filename = data.get('filename')
        content = data.get('content')
        lang = data.get('lang', 'zh')
        style = data.get('style', 'manual')  # 默认 manual

        if not filename or not content:
            return jsonify({'success': False, 'error': '文件名和内容不能为空'})

        documentation = doc_generator.generate_documentation(content, filename, lang, style)

        # 保存为 Markdown 文件
        with open("output.md", "w", encoding="utf-8") as f:
            f.write(documentation)

        return jsonify({
            'success': True,
            'documentation': documentation,
            'download': '/download-md'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download-md')
def download_markdown():
    return send_file("output.md", as_attachment=True)

def open_browser():
    """延迟打开浏览器"""
    time.sleep(1.5)
    webbrowser.open('http://localhost:9001')

if __name__ == '__main__':
    print("🚀 智能代码文档生成系统启动中...")
    print("\n🌐 服务地址: http://localhost:9001")
    print("📋 使用说明:")
    print("   1. 上传代码文件（支持拖拽）")
    print("   2. 选择语言与想要的风格")
    print("   3. 点击生成文档按钮")
    print("   4. 等待AI分析并生成文档")
    print("   5. 复制或保存生成的文档，支持md和pdf文件导出格式")
    print("\n⚠️  注意: 请确保您的OpenAI API密钥有效且有足够额度")
    print("=" * 60)
    
    # 在后台线程中打开浏览器
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # 启动Flask应用
    app.run(debug=False, host='0.0.0.0', port=9001)
