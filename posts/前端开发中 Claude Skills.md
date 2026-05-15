# 推荐两个前端必装的 Claude Skill：一个管颜值，一个管性能

> 原文地址：https://mp.weixin.qq.com/s/kel5C0_qvs8iaxg4WcH0Jw

## 🔍 问题背景

让 AI 写前端页面常见的问题：

- **风格单一**：紫蓝渐变、圆角卡片、居中大标题高度雷同，千篇一律
- **性能不佳**：useEffect 嵌套过多，请求串行，冗余重复
- **代码可维护性差**：逻辑上能跑，但同事看了想重写

> 这是 AI 的“统计惯性”——训练数据里出现频繁的风格和写法，AI 倾向于模仿，而非学习最佳实践。

---

## 💡 解决方案：Claude Skills

给 AI 装上特定的 Skill = 提供一本 **“风格手册”** 或 **“工程规范”** ，按高标准约束 AI 的输出。

---

## 🎨 Skill 1：frontend-design —— 告别“模板脸”

**开发者**：Anthropic 官方
**来源**：https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md
**解决的问题**：AI 生成的页面千篇一律，缺乏品牌感

### 核心规则
- ❌ 禁止使用 Inter、Roboto、Arial 等默认字体
- ❌ 禁止使用紫色+白色的经典搭配
- ✅ 动笔前必须先确定明确的美学方向

### 支持的风格方向
- 粗野主义风格排版
- 轻量拟物风格
- 像 90 年代游戏说明书风格

> AI 会生成一整套自洽的设计体系，而非拼接流行元素。

### 📊 效果对比

| 维度 | 使用前 | 使用后 |
|------|--------|--------|
| 设计风格 | 随机组合流行元素，千篇一律 | 方向明确、风格自洽 |
| 字体选择 | 依赖系统默认字体 | 规避常见默认字体，意图明确 |
| 开发流程 | 直接写代码 | 先定美学方向，再动手 |
| 整体观感 | 一眼 AI 味 | 告别模板脸，有独特风格 |

### 🔧 安装方式

> 前提：先安装 SkillHub 商店（仅 CLI 版本）

未安装 SkillHub → 按 https://skillhub.cn/install/skillhub.md 安装 CLI，再安装 `frontend-design-3`
已安装 SkillHub → 直接安装 `frontend-design-3`

---

## ⚡ Skill 2：react-best-practices —— AI 的“虚拟架构师”

**开发者**：Vercel 工程团队
**来源**：https://github.com/vercel-labs/agent-skills/tree/react-best-practices/skills/react-best-practices
**解决的问题**：AI 写的 React/Next.js 代码性能差、反模式多

### Vercel 团队发现的典型“坑”
- 不必要的客户端组件
- useEffect 滥用导致性能下降
- 缺失缓存策略，重复请求
- 缺少错误边界
- 组件拆分和复用不合理

### 安装方式

> 前提：先安装 SkillHub 商店（仅 CLI 版本）

未安装 SkillHub → 按 https://skillhub.cn/install/skillhub.md 安装 CLI，再安装 `react-best-practices`
已安装 SkillHub → 直接安装 `react-best-practices`

---

## 📌 附：笔记编辑补充说明

### 一、文章亮点
1. **定位精准**：直接切中前端开发者使用 AI 写代码的两大痛点——设计同质化 + 性能隐患
2. **解决方案可落地**：给出了具体的 Skill 名称、来源和安装方式，不是空谈概念
3. **来源权威**：frontend-design 来自 Anthropic 官方，react-best-practices 来自 Vercel 工程团队
4. **量化对比**：用表格对比使用前后的差异，说服力强

### 二、适用人群
- 日常用 AI（尤其是 Claude）辅助编写前端代码的开发者
- 对 AI 生成的 UI 风格不满意，希望定制化设计方向的开发者
- 关注 React/Next.js 性能和最佳实践的工程团队

### 三、进一步行动建议

1. **立即安装测试**：按照文中的安装方式，在 Claude 环境中安装两个 Skill，用一个小型前端组件实测效果
2. **纳入团队规范**：将这两个 Skill 作为前端团队的 AI 辅助编码推荐配置，统一输出标准
3. **探索更多 Skill**：登录 SkillHub 商店搜索其他场景的 Skill（如测试、文档生成等），扩展 AI 辅助能力
4. **建立反馈机制**：在使用过程中记录 AI 生成代码的改进点与不足，反哺给团队作为 prompt 优化依据
