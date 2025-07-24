# generator/documentation.py
from openai import OpenAI
from pathlib import Path
import traceback

class DocumentationGenerator:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def get_language_from_extension(self, filename):
        ext = Path(filename).suffix.lower()
        language_map = {
            '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript', '.java': 'Java',
            '.cpp': 'C++', '.c': 'C', '.cs': 'C#', '.php': 'PHP', '.rb': 'Ruby',
            '.go': 'Go', '.rs': 'Rust', '.swift': 'Swift', '.kt': 'Kotlin',
            '.scala': 'Scala', '.r': 'R', '.m': 'Objective-C', '.pl': 'Perl',
            '.sh': 'Shell', '.sql': 'SQL', '.html': 'HTML', '.css': 'CSS',
            '.vue': 'Vue.js', '.jsx': 'React JSX', '.tsx': 'TypeScript React'
        }
        return language_map.get(ext, '未知语言')

    def generate_documentation(self, code, filename, lang='zh', style='manual'):
        try:
            language = self.get_language_from_extension(filename)
            if style == 'tutorial':
                prompt = self.create_tutorial_prompt(code, language, filename, lang)
            elif style == 'api':
                prompt = self.create_api_prompt(code, language, filename, lang)
            elif style == 'comment':
                prompt = self.create_comment_prompt(code, language, filename, lang)
            elif style == 'insight':
                prompt = self.create_insight_prompt(code, language, filename, lang)
            else:
                prompt = self.create_manual_prompt(code, language, filename, lang)

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional documentation generator AI. Write clean, accurate, readable documentation." if lang == 'en'
                        else "你是一个专业的技术文档编写专家，擅长为各种编程语言的代码生成清晰、全面、实用的技术文档。请用中文回答，并且格式要清晰易读。"
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"生成文档时出错: {str(e)}")

    def create_manual_prompt(self, code, language, filename, lang):
        return self.create_documentation_prompt(code, language, filename, lang)

    def create_tutorial_prompt(self, code, language, filename, lang):
        if lang == 'en':
            return f"""
Write a beginner-friendly tutorial for the following {language} code.

Filename: {filename}
Language: {language}

Code:
{code}

Explain each function/module in plain English, with practical use-cases, step-by-step guidance, and example usages.
"""
        else:
            return f"""
请为以下{language}代码生成适合初学者的中文教程。

文件名: {filename}
语言: {language}

代码:
{code}

要求包含每个函数/模块的详细解释，使用步骤、用途说明和使用示例。
"""

    def create_api_prompt(self, code, language, filename, lang):
        if lang == 'en':
            return f"""
Generate RESTful API style documentation for the following {language} code.
Include endpoint descriptions, parameters, request/response examples, and status codes if applicable.

Filename: {filename}
Language: {language}

Code:
{code}
"""
        else:
            return f"""
请为以下{language}代码生成 RESTful 风格的中文 API 文档，包括接口描述、参数说明、请求/响应示例及状态码（如适用）。

文件名: {filename}
语言: {language}

代码:
{code}
"""

    def create_comment_prompt(self, code, language, filename, lang):
        if lang == 'en':
            return f"""
Add inline comments to the following {language} code to explain the logic clearly.
Avoid changing the original structure.

Filename: {filename}
Language: {language}

Code:
{code}
"""
        else:
            return f"""
请为以下{language}代码添加中文注释，解释每个关键步骤的作用，避免改动代码结构。

文件名: {filename}
语言: {language}

代码:
{code}
"""

    def create_insight_prompt(self, code, language, filename, lang):
        if lang == 'en':
            return f"""
Provide a deep architecture-level analysis and optimization suggestions for the following {language} code.
Explain performance trade-offs, scalability, and refactoring opportunities.

Filename: {filename}
Language: {language}

Code:
{code}
"""
        else:
            return f"""
请对以下{language}代码从架构层面进行深入分析，分析地越详细越好，内容尽可能详细丰富多样化，并提出性能优化、可扩展性建议及重构思路。

文件名: {filename}
语言: {language}

代码:
{code}
"""

    def create_documentation_prompt(self, code, language, filename, lang='zh'):
        if lang == 'en':
            return f"""
Generate a full technical documentation for the following {language} code in Markdown format.

**Filename**: {filename}
**Language**: {language}

**Code**:
{code}

The documentation should include:
- Overview
- Architecture
- Functions and Methods (name, params, return, usage)
- Classes (if any)
- Best Practices
- External Dependencies

Write clear, accurate and helpful documentation.
"""
        else:
            return f"""
请为以下{language}代码生成全面的技术文档。文档应该包含以下几个部分：

**文件名**: {filename}
**编程语言**: {language}

**代码内容**:
{language.lower()}
{code}

请按照以下格式生成文档：

# 📋 代码文档

## 📖 概述
[简要描述这个文件/模块的主要功能和用途]

## 🏗️ 整体架构
[描述代码的整体结构和设计思路]

## 📚 函数/方法详解

### 函数名称
**功能描述**: [详细说明函数的作用]
**参数说明**:
- 参数名 (类型): 参数描述

**返回值**: [返回值类型和说明]
**使用示例**:
{language.lower()}
[提供具体的使用示例]

---

## 🔧 类详解 (如果有类的话)

### 类名
**功能描述**: [类的主要功能]
**属性**:
- 属性名 (类型): 属性描述

**方法**:
- 方法名(): 方法功能描述

**使用示例**:
{language.lower()}
[类的使用示例]

---

## 💡 使用建议
[提供代码使用的最佳实践和建议]

## ⚠️ 注意事项
[列出使用时需要注意的问题]

## 🔗 依赖关系
[列出代码的外部依赖]

请确保文档详细、准确，并提供实用的示例。对于每个重要的函数和类都要有清晰的说明。
"""
