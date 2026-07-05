# 案例标准格式 v1.0

每个案例为一个JSON文件，存放在案例库中。结构如下：

```json
{
  "id": "case-002",
  "title": "案例名称",
  "type": "技术决策 | 管理决策 | 投资决策 | 人生决策 | 资源分配",
  "version": "1.0",

  "scenario": {
    "background": "场景背景描述。只给事实和约束条件，不加判断，不引导方向。",
    "constraints": ["约束条件1", "约束条件2", "约束条件3"],
    "time_pressure": "时间压力描述（如有）"
  },

  "three_knives": {
    "time_fold": {
      "short_term": "3天后看，这个判断会怎样？",
      "mid_term": "3个月后看，这个判断会怎样？",
      "long_term": "3年后看，这个判断还重要吗？"
    },
    "perspective_shift": {
      "boss": "上级会怎么看？",
      "executor": "执行者会怎么看？",
      "opponent": "反对者会怎么攻击这个判断？"
    },
    "counterfactual": {
      "key_assumption": "这个判断依赖的核心假设是什么？",
      "if_false": "如果假设不成立会怎样？",
      "if_reverse": "如果假设的反面成立呢？"
    }
  },

  "socratic_questions": {
    "clarify": "澄清类追问——针对概念定义的提问",
    "hypothesis": "假设检验类追问——针对隐含前提的提问",
    "evidence": "证据检验类追问——针对依据的提问",
    "perspective": "视角转换类追问——针对盲区的提问",
    "consequence": "后果追踪类追问——针对后续推演的提问"
  },

  "bindings": {
    "weighted_knife": "加重哪把刀（time_fold / perspective_shift / counterfactual / socratic）",
    "enhanced_questions": ["追加追问1", "追加追问2"]
  },

  "common_blind_spots": [
    "常见盲区1",
    "常见盲区2",
    "常见盲区3"
  ],

  "related_cases": [
    {"id": "case-001", "reason": "关联理由——结构相似性说明"},
    {"id": "case-003", "reason": "关联理由"}
  ],

  "source": {
    "origin": "案例来源描述",
    "date": "2026-07-05",
    "note": "来源说明"
  }
}
```

## 字段说明

| 字段 | 必填 | 说明 |
|:-----|:----:|:------|
| id | ✅ | 唯一标识，case-001开始 |
| title | ✅ | 案例名称，一句话说清 |
| type | ✅ | 五种决策类型之一 |
| scenario.background | ✅ | 场景描述，**只给事实，不加判断** |
| scenario.constraints | ✅ | 至少2条约束条件 |
| three_knives | ✅ | 三把刀的预置分析，各三级追问 |
| socratic_questions | ✅ | 五类苏格拉底追问各一条 |
| bindings | ✅ | 案例-模型绑定信息 |
| common_blind_spots | ✅ | 至少3条常见盲区 |
| source | ✅ | 案例来源说明 |
