# 01. Information Inflow

Omi 的信息入口不是单一硬件，而是多 source 输入。设备、手机、桌面、外部集成都可以进入同一套后端处理链路。

## 1. 输入来源

Omi 后端的 `ConversationSource` 包括：

```text
friend
omi
fieldy
bee
plaud
frame
friend_com
apple_watch
phone
phone_call
desktop
openglass
screenpipe
workflow
sdcard
external_integration
limitless
onboarding
unknown
```

这说明 Omi 的 ingestion 层不是绑定某个 device，而是把 device 当作 `source` 标签。

## 2. 实时音频入口

实时音频主要进入 `/v4/listen` WebSocket。

典型参数：

```text
uid
language
sample_rate
codec
channels
include_speech_profile
conversation_timeout
source
custom_stt
```

流程：

```text
device/app opens WebSocket
 -> backend authenticates uid
 -> backend opens STT WebSocket, normally Deepgram
 -> audio bytes stream in
 -> transcript segments stream out
 -> backend writes segments into current conversation
```

## 3. 外部文本入口

Omi 也支持 `external_integration` / `workflow` 类型的数据。

外部文本会带一个 `text_source`：

```text
audio_transcript
message
other_text
```

不同 `text_source` 会走不同 structured extraction：

```text
audio_transcript -> get_transcript_structure + extract_action_items
message          -> get_message_structure
other_text       -> summarize_experience_text
```

## 4. Inflow 的第一步落点

实时链路中，WebSocket 一开始会创建一个 stub conversation：

```json
{
  "status": "in_progress",
  "source": "omi",
  "created_at": "...",
  "started_at": "...",
  "transcript_segments": []
}
```

后面所有 segments 都追加到这个 conversation。

## 5. 关键点

- Omi 先统一成 `conversation`，再处理业务含义。
- `source` 是一等字段，用于记录信息来自哪里。
- 实时音频是 streaming ingestion，外部文字是 batch ingestion。
- 入口不决定最终分类，最终分类由后面的 LLM structured processing 决定。

