# RESTful 风格的中文 API 文档

## 评估长文本任务 API

### 接口描述

评估长文本任务 API 包含了对不同数据集的预测结果进行评估，并返回评分结果的功能。

### 接口路径

- `/eval_long_bench.py`

### 请求方式

- POST

### 请求参数

| 参数名 | 类型 | 是否必须 | 描述 |
| ------ | ---- | -------- | ---- |
| model  | 字符串 | 是       | 模型名称 |
| e      | 布尔值 | 否       | 是否在 LongBench-E 上评估 |

### 请求示例

```json
{
    "model": "model_name",
    "e": true
}
```

### 响应示例

```json
{
    "dataset1": 85.6,
    "dataset2": 92.3,
    ...
}
```

### 状态码

- 200 OK：请求成功
- 400 Bad Request：请求参数错误

### 状态码示例

- 成功响应：

```json
{
    "message": "评估完成",
    "scores": {
        "dataset1": 85.6,
        "dataset2": 92.3,
        ...
    }
}
```

- 请求参数错误：

```json
{
    "message": "请求参数错误"
}
```

### Python 代码

```python
import os
import json
import argparse
import numpy as np

from metrics import (
    qa_f1_score,
    rouge_zh_score,
    qa_f1_zh_score,
    rouge_score,
    classification_score,
    retrieval_score,
    retrieval_zh_score,
    count_score,
    code_sim_score,
)

dataset2metric = {
    "narrativeqa": qa_f1_score,
    "qasper": qa_f1_score,
    ...
}

def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default=None)
    parser.add_argument('--e', action='store_true', help="Evaluate on LongBench-E")
    return parser.parse_args(args)

def scorer_e(dataset, predictions, answers, lengths, all_classes):
    ...

def scorer(dataset, predictions, answers, all_classes):
    ...

if __name__ == '__main__':
    args = parse_args()
    scores = dict()
    if args.e:
        path = f"pred_e/{args.model}/"
    else:
        path = f"pred/{args.model}/"
    all_files = os.listdir(path)
    print("Evaluating on:", all_files)
    for filename in all_files:
        ...
```

以上是对评估长文本任务 API 的描述，包括接口路径、请求方式、请求参数、请求示例、响应示例、状态码及状态码示例。