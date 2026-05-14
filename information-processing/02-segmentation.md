# 02. Segmentation

Omi 的 segmentation 有四层：audio packet、transcript segment、conversation、derived object。

```text
audio packets
 -> transcript segments
 -> conversation
 -> memories / action_items / events / vectors
```

## 1. Audio Packet

设备通过 BLE 或 app 把音频切成小包上传。

设备协议支持多种 codec：

```text
PCM 16kHz 16-bit mono
PCM 8kHz 16-bit mono
Mu-law 16kHz 8-bit mono
Mu-law 8kHz 8-bit mono
Opus 16kHz 16-bit mono
```

这层只是传输单位，还不是语义单位。

## 2. Transcript Segment

STT provider 把音频流变成 transcript segments。

典型 segment：

```json
{
  "id": "segment-id",
  "text": "明天提醒我交房租。",
  "speaker": "SPEAKER_00",
  "speaker_id": 0,
  "is_user": true,
  "person_id": null,
  "start": 12.3,
  "end": 15.8,
  "speech_profile_processed": true,
  "stt_provider": "deepgram"
}
```

segment 的切分来自 STT 的语音边界、speaker diarization 和时间戳。

Omi 还会合并某些相邻 segments：

- 同一个 speaker 连续说话。
- 两段像是同一句话的延续。
- speaker profile / STT provider 条件兼容。

## 3. Conversation

conversation 是 Omi 的核心语义容器。

实时录音时，conversation 的边界通常由：

- WebSocket session 开始。
- 静音超时。
- 手动结束。
- 新 conversation 被创建。

默认 `conversation_timeout` 文档中为 120 秒。超过一段静音后，当前 conversation 进入 processing，并创建新的 stub conversation。

状态流：

```text
in_progress
 -> processing
 -> completed
```

其他状态：

```text
merging
failed
```

## 4. Derived Object

conversation 处理后会被继续拆成派生对象：

```text
structured summary
memories
action_items
calendar events
vector metadata
trends
app results
```

这些 derived objects 都可以回溯到原始 `conversation_id`。

## 5. 关键点

- Omi 不按“每天”做原始 segmentation。
- Omi 的原始语义单位是 `conversation`。
- 每天的信息是按 date range 拉 conversations 后生成的 view。
- transcript segment 用于保留原文，conversation 用于组织事件，derived object 用于长期查询和自动化。

