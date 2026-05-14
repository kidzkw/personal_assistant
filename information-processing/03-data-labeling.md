# 03. Data Labeling

Omi 的 labeling 分为五类：系统标签、segment 标签、structured 语义标签、memory/action 标签、vector metadata。

## 1. 系统标签

系统标签是后端字段，不一定由 LLM 生成。

Conversation 级别：

```text
id
uid
created_at
started_at
finished_at
source
language
status
visibility
starred
folder_id
is_locked
data_protection_level
private_cloud_sync_enabled
discarded
```

这些字段负责回答：

- 谁的数据？
- 从哪里来？
- 什么时候发生？
- 处理到哪一步？
- 是否可见？
- 是否锁定？
- 是否加密？

## 2. Segment 标签

Transcript segment 级别：

```text
id
text
speaker
speaker_id
is_user
person_id
start
end
speech_profile_processed
stt_provider
translations
```

这些字段负责 speaker diarization 和人物绑定。

区别：

```text
speaker      = STT 给出的文本标签，例如 SPEAKER_00
speaker_id   = 数字 speaker id，例如 0
person_id    = Omi 识别或用户指定的联系人 id
is_user      = 这句话是否被认为是用户本人说的
```

## 3. Structured 语义标签

conversation 结束后，LLM 生成 `structured`：

```json
{
  "title": "Rent Payment Reminder",
  "overview": "User mentioned needing to pay rent tomorrow.",
  "emoji": "🏠",
  "category": "finance",
  "action_items": [],
  "events": []
}
```

`category` 是 enum，包括：

```text
personal
education
health
finance
legal
philosophy
spiritual
science
entrepreneurship
parenting
romantic
travel
inspiration
technology
business
social
work
sports
politics
literature
history
architecture
music
weather
news
entertainment
psychology
real
design
family
economics
environment
other
```

## 4. Memory 标签

Memory 有自己的 category：

```text
system
interesting
manual
```

含义：

```text
system      = 关于用户的事实、偏好、关系、项目、习惯、观点
interesting = 从对话中提取的有长期价值的信息或建议
manual      = 用户手动创建的 memory
```

Memory 还带：

```text
conversation_id
tags
reviewed
user_review
visibility
manually_added
edited
scoring
app_id
data_protection_level
is_locked
kg_extracted
```

## 5. Action Item 标签

Action item 字段：

```text
description
completed
created_at
updated_at
due_at
completed_at
conversation_id
is_locked
sync_requested
exported
```

它们用于：

- 查询未完成任务。
- 查询今天/本周 due 的任务。
- 回溯任务来自哪段 conversation。
- 同步到 Apple Reminders 等外部任务系统。

## 6. Vector Metadata

Omi 会为 conversation 提取检索 metadata：

```text
people
topics
entities
dates
created_at
uid
```

这部分不是用户直接看到的 label，而是给 semantic search 用。

## 7. Labeling 关键点

- `source/status/time/security` 是系统标签。
- `speaker/person` 是 segment 标签。
- `title/overview/category` 是 LLM 语义标签。
- `memory category` 和 `action item status` 是派生对象标签。
- `people/topics/entities/dates` 是检索标签。

