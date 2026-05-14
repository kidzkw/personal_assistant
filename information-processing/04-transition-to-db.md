# 04. Transition To DB

Omi 的 transition to DB 不是一次性写一个大对象，而是分阶段写入 conversation、memory、action item 和 vector index。

## 1. Firestore 主结构

Omi 的主要 Firestore 路径：

```text
users/{uid}/conversations/{conversation_id}
users/{uid}/memories/{memory_id}
users/{uid}/action_items/{action_item_id}
```

其中：

```text
conversations = primary storage
memories      = extracted long-term facts
action_items  = standalone tasks
```

## 2. Conversation 写入

WebSocket 开始时创建：

```json
{
  "status": "in_progress",
  "source": "omi",
  "created_at": "...",
  "started_at": "...",
  "transcript_segments": []
}
```

转录过程中持续更新：

```text
update_conversation_segments()
```

静音 timeout 或结束后：

```text
status = processing
send process_conversation request
```

LLM 处理完成后：

```text
structured = title + overview + category + action_items + events
status = completed
upsert_conversation()
```

## 3. Structured 写入

`structured` 直接写在 conversation 文档里：

```json
{
  "structured": {
    "title": "Budget Discussion",
    "overview": "User discussed rent and bill payments.",
    "emoji": "💸",
    "category": "finance",
    "action_items": [
      {
        "description": "Pay rent tomorrow",
        "completed": false,
        "due_at": "..."
      }
    ],
    "events": []
  }
}
```

这让 conversation list 可以快速显示摘要和类别。

## 4. Memory 写入

Memory 是从 conversation 派生出来的，不是原始数据。

处理步骤：

```text
delete old memories for this conversation if reprocessing
 -> extract new memories from transcript/text
 -> search similar memories
 -> resolve conflict: keep existing / merge / keep both
 -> save memories
 -> upsert memory vectors
```

Memory 保存结构：

```json
{
  "id": "memory-id",
  "uid": "user-id",
  "content": "User prefers handling bills before due dates.",
  "category": "system",
  "tags": ["finance"],
  "conversation_id": "source-conversation-id",
  "reviewed": true,
  "visibility": "public",
  "is_locked": false
}
```

## 5. Action Item 写入

Action item 先被 LLM 放在 `conversation.structured.action_items` 里。

之后 Omi 会复制到独立 collection：

```text
structured.action_items
 -> users/{uid}/action_items/{action_item_id}
```

写入步骤：

```text
delete old action items for this conversation
 -> create new action items batch
 -> send due-date notification payload if due_at exists
 -> upsert action item vectors
 -> auto sync to task integration
```

独立 action item 示例：

```json
{
  "description": "Pay rent tomorrow",
  "completed": false,
  "created_at": "...",
  "updated_at": "...",
  "due_at": "...",
  "completed_at": null,
  "conversation_id": "source-conversation-id",
  "is_locked": false
}
```

## 6. Vector DB 写入

Omi 使用 Pinecone namespace：

```text
ns1 = conversations
ns2 = memories
ns3 = screen activity
ns4 = action items
```

Conversation vector：

```text
generate_embedding(str(conversation.structured))
```

也就是说主要 embed：

```text
title
overview
category
action_items
events
```

不是默认 embed 完整 transcript。

同时保存 metadata：

```text
uid
created_at
people
topics
entities
dates
```

## 7. Encryption / Protection

Omi 支持 `data_protection_level`：

```text
standard
enhanced
```

enhanced 下会加密：

```text
conversation.transcript_segments
memory.content
photo/audio sensitive payloads
```

注意：即使 transcript 加密，structured summary、metadata、vectors 仍可能泄露语义信息。

## 8. Transition 总结

完整 DB transition：

```text
audio/text input
 -> in_progress conversation
 -> transcript_segments appended
 -> processing
 -> structured written into conversation
 -> memories collection
 -> action_items collection
 -> vector namespaces
 -> completed conversation
```

