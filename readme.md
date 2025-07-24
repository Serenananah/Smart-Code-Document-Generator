# 智能代码文档生成器

一个基于OpenAI GPT的智能代码文档生成系统，能够自动分析代码并生成专业的技术文档。

## 功能特性

- 🚀 **自动代码分析**：智能识别代码结构和功能
- 📝 **全面的文档生成**：包含函数说明、参数解释、使用示例等
- 🌐 **多语言支持**：支持JavaScript、Python、Java、TypeScript等主流编程语言
- 🎨 **多种文档风格**：全面详细、简洁明了、教程风格、API参考
- 🔧 **灵活配置**：可自定义文档内容和格式
- 📊 **Markdown输出**：生成格式规范的Markdown文档

## 快速开始

### 1. 环境要求

- Python 3.8+
- pip
- OpenAI API密钥

### 2. 安装步骤

```bash
# 克隆项目
git clone https://github.com/yourusername/code-doc-generator.git
cd code-doc-generator

# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置

创建 `.env` 文件并添加您的OpenAI API密钥：

```env
OPENAI_API_KEY=your-openai-api-key-here
```

### 4. 运行服务

```bash
# 开发模式
python app.py

# 生产模式（使用Gunicorn）
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

服务将在 `http://localhost:5000` 启动。

## API文档

### 生成文档

**端点**: `POST /api/generate-documentation`

**请求参数**:
- `file`: 代码文件（必需）
- `language`: 编程语言（可选，默认自动检测）
- `docStyle`: 文档风格（可选）
  - `comprehensive`: 全面详细
  - `concise`: 简洁明了
  - `tutorial`: 教程风格
  - `api-reference`: API参考
- `includeFunctions`: 是否包含函数说明（可选，默认true）
- `includeParams`: 是否包含参数解释（可选，默认true）
- `includeExamples`: 是否包含使用示例（可选，默认true）
- `includeTypes`: 是否包含类型信息（可选，默认false）
- `additionalPrompt`: 额外的文档要求（可选）

**响应示例**:
```json
{
  "success": true,
  "documentation": "# 代码文档\n\n## 函数说明...",
  "metadata": {
    "filename": "example.js",
    "language": "JavaScript",
    "generated_at": "2024-01-01T12:00:00",
    "model": "gpt-4",
    "doc_style": "comprehensive"
  },
  "html": "<h1>代码文档</h1>..."
}
```

### 健康检查

**端点**: `GET /health`

**响应示例**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-01T12:00:00"
}
```

### 获取支持的语言

**端点**: `GET /api/supported-languages`

**响应示例**:
```json
{
  "languages": [
    {"value": "auto", "label": "自动检测"},
    {"value": "javascript", "label": "JavaScript"},
    {"value": "python", "label": "Python"}
    // ...
  ]
}
```

## 使用示例

### Python脚本调用

```python
import requests

# API端点
url = "http://localhost:5000/api/generate-documentation"

# 准备文件和参数
with open("example.py", "rb") as f:
    files = {"file": ("example.py", f, "text/plain")}
    data = {
        "language": "python",
        "docStyle": "comprehensive",
        "includeFunctions": "true",
        "includeParams": "true",
        "includeExamples": "true"
    }
    
    # 发送请求
    response = requests.post(url, files=files, data=data)
    
    # 处理响应
    if response.status_code == 200:
        result = response.json()
        print(result["documentation"])
    else:
        print(f"Error: {response.json()}")
```

### cURL命令

```bash
curl -X POST http://localhost:5000/api/generate-documentation \
  -F "file=@example.js" \
  -F "language=javascript" \
  -F "docStyle=comprehensive" \
  -F "includeExamples=true"
```

## 前端集成

将前端HTML文件中的API配置更新为您的后端地址：

```javascript
const API_CONFIG = {
    endpoint: 'http://localhost:5000/api/generate-documentation',
    // 不需要在前端存储API密钥
};
```

## 部署指南

### Docker部署

创建 `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

构建和运行：

```bash
docker build -t code-doc-generator .
docker run -p 5000:5000 -e OPENAI_API_KEY=your-key code-doc-generator
```

### 云服务部署

#### Heroku

1. 创建 `Procfile`:
```
web: gunicorn app:app
```

2. 部署：
```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your-key
git push heroku main
```

#### AWS/阿里云/腾讯云

使用各平台的容器服务或虚拟机部署，确保：
- 设置环境变量
- 配置安全组/防火墙规则
- 使用HTTPS（推荐）

## 安全建议

1. **API密钥管理**
   - 永远不要在代码中硬编码API密钥
   - 使用环境变量或密钥管理服务
   - 定期轮换密钥

2. **访问控制**
   - 实施API速率限制
   - 添加身份验证（如JWT）
   - 使用HTTPS传输

3. **输入验证**
   - 限制文件大小（默认10MB）
   - 验证文件类型
   - 防止恶意代码注入

4. **错误处理**
   - 不要暴露敏感错误信息
   - 记录错误日志
   - 实施监控告警

## 性能优化

1. **缓存策略**
   - 对相同代码的文档请求进行缓存
   - 使用Redis等缓存服务

2. **异步处理**
   - 对于大文件，使用异步任务队列
   - 实施WebSocket实时更新

3. **模型选择**
   - 根据需求选择合适的模型（GPT-3.5 vs GPT-4）
   - 考虑成本和性能平衡

## 故障排除

### 常见问题

1. **API密钥错误**
   - 检查.env文件是否正确配置
   - 确认密钥有效且有足够的配额

2. **文件上传失败**
   - 检查文件大小是否超过限制
   - 确认文件编码为UTF-8

3. **生成超时**
   - 增加请求超时时间
   - 考虑使用更小的代码片段

### 日志查看

```bash
# 查看应用日志
tail -f app.log

# 查看Gunicorn日志
tail -f gunicorn.log
```

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

- 项目维护者：Your Name
- Email: your.email@example.com
- 项目链接：https://github.com/yourusername/code-doc-generator

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 支持主流编程语言
- 基础文档生成功能
- Web界面

### 计划功能

- [ ] 批量文件处理
- [ ] 项目级文档生成
- [ ] 多语言文档支持
- [ ] PDF导出功能
- [ ] 团队协作功能
- [ ] API文档自动同步