// 所有 JS 逻辑（上传、调用API、模拟进度条、预览、导出）
let selectedFile = null;

const uploadSection = document.getElementById('uploadSection');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const generateBtn = document.getElementById('generateBtn');

uploadSection.addEventListener('dragover', (e) => {
  e.preventDefault();
  uploadSection.classList.add('dragover');
});

uploadSection.addEventListener('dragleave', () => {
  uploadSection.classList.remove('dragover');
});

uploadSection.addEventListener('drop', (e) => {
  e.preventDefault();
  uploadSection.classList.remove('dragover');
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    handleFileSelect(files[0]);
  }
});

fileInput.addEventListener('change', (e) => {
  if (e.target.files.length > 0) {
    handleFileSelect(e.target.files[0]);
  }
});

function handleFileSelect(file) {
  selectedFile = file;
  document.getElementById('fileName').textContent = file.name;
  document.getElementById('fileSize').textContent = `文件大小: ${(file.size / 1024).toFixed(2)} KB`;
  fileInfo.classList.add('show');
  generateBtn.disabled = false;
}

async function generateDocumentation() {
  if (!selectedFile) {
    alert('请先选择一个文件');
    return;
  }

  const loading = document.getElementById('loading');
  const resultSection = document.getElementById('resultSection');
  const docEditor = document.getElementById('documentationEditor');
  const progressBar = document.getElementById('progressBar');

  // 初始化状态
  loading.classList.add('show');
  generateBtn.disabled = true;
  generateBtn.textContent = '生成中...';
  resultSection.classList.remove('show');
  progressBar.style.width = '0%';

  // 启动模拟进度
  let progress = 0;
  const interval = setInterval(() => {
    if (progress >= 95) return;
    progress += Math.random() * 5;
    progressBar.style.width = `${Math.min(progress, 95)}%`;
  }, 300);

  try {
    const fileContent = await readFileContent(selectedFile);
    const response = await fetch('/generate-docs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        filename: selectedFile.name,
        content: fileContent,
        lang: document.getElementById('lang').value,  // ✅ 新增语言传参
        style: document.getElementById('style').value   // ✅ 新增风格传参
      })
    });

    const result = await response.json();

    if (result.success) {
      const nameWithoutExt = selectedFile.name.split('.').slice(0, -1).join('.');
      const mdLink = document.getElementById('downloadMdBtn');
      mdLink.setAttribute('download', `${nameWithoutExt}-docs.md`);
      mdLink.href = 'data:text/markdown;charset=utf-8,' + encodeURIComponent(result.documentation);

      docEditor.value = result.documentation;
      resultSection.classList.add('show');
      resultSection.scrollIntoView({ behavior: 'smooth' });
    } else {
      throw new Error(result.error || '生成文档失败');
    }

    // 立即进度到 100%
    progressBar.style.width = '100%';
  } catch (error) {
    alert('生成文档时出现错误: ' + error.message);
    progressBar.style.width = '100%';
  } finally {
    clearInterval(interval);
    setTimeout(() => {
      loading.classList.remove('show');
      progressBar.style.width = '0%';
    }, 500); // 停顿后隐藏
    generateBtn.disabled = false;
    generateBtn.textContent = '🔄 生成文档';
  }
}

function readFileContent(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => resolve(e.target.result);
    reader.onerror = () => reject(new Error('文件读取失败'));
    reader.readAsText(file);
  });
}

function copyDocumentation() {
  const documentation = document.getElementById('documentationEditor').value;
  navigator.clipboard.writeText(documentation).then(() => {
    const copyBtn = document.querySelector('.copy-btn');
    const originalText = copyBtn.textContent;
    copyBtn.textContent = '已复制!';
    copyBtn.style.background = 'var(--success-color)';
    setTimeout(() => {
      copyBtn.textContent = originalText;
      copyBtn.style.background = 'var(--warning-color)';
    }, 2000);
  }).catch(() => {
    alert('复制失败，请手动选择文本复制');
  });
}

function renderAndExportPDF() {
  const rawMarkdown = document.getElementById('documentationEditor').value;
  const renderedDiv = document.getElementById('renderedPreview');

  // 渲染 Markdown
  const md = window.markdownit({ html: true, linkify: true, typographer: true });
  renderedDiv.innerHTML = md.render(rawMarkdown);

  // 触发 paged.js 渲染预览并导出
  const tempWindow = window.open('', '_blank');
  const doc = `
    <html>
      <head>
        <meta charset="utf-8">
        <title>导出预览</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown-light.min.css" />
        <style>
          body {
            padding: 30px;
            font-family: 'Noto Sans', sans-serif;
          }
          .markdown-body {
            max-width: 800px;
            margin: auto;
          }
        </style>
      </head>
      <body>
        <article class="markdown-body">
          ${renderedDiv.innerHTML}
        </article>
        <script src="https://unpkg.com/pagedjs/dist/paged.polyfill.js"></script>
      </body>
    </html>
  `;
  tempWindow.document.write(doc);
  tempWindow.document.close();
}

function simulateProgress(callback) {
  const progressBar = document.getElementById('progressBar');
  let progress = 0;
  const interval = setInterval(() => {
    if (progress >= 95) {
      clearInterval(interval);
      return;
    }
    progress += Math.random() * 5; // 模拟速度不均匀
    progressBar.style.width = `${Math.min(progress, 95)}%`;
  }, 300);

  callback(() => {
    clearInterval(interval);
    progressBar.style.width = '100%';
  });
}
