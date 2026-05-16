# Echo Personal Assistant / Personal Memory Database

Language / 语言:

- [English](README.en.md)
- [中文](README.zh-CN.md)

Echo is a local-first personal assistant and personal memory database experiment. It starts with a small, inspectable workflow before adding real ingestion, indexing, UI, or Docker packaging.

这是一个 local-first 的个人记忆库实验项目。当前先把可检查、可追溯的最小工作流跑通，再逐步加入真实导入、索引、UI 或 Docker 打包。

## Quick Start

```powershell
git clone https://github.com/kidzkw/personal_assistant.git
cd personal_assistant
.\runtime\scripts\validate-dry-run.ps1
```

Run the local Docker server / 启动本地 Docker server:

```powershell
docker compose up --build
curl.exe http://localhost:8080/dry-run
```

Browser dashboard / 浏览器面板:

```text
http://localhost:8080/
```

The homepage shows quick capture, the last 3 days of local inbox records, and past-week highlights.

主页会显示快速记录、最近 3 天的本地 inbox 记录，以及过去一周亮点。

Next TODOs / 下一步 TODO:

```text
prepare item -> review queue -> formal schema -> previews -> OCR -> search -> confirmed memory -> weekly summary -> privacy tiers
```

Send a local-only item / 发送本地内容到 inbox:

Open the dashboard and use the Dropbox area. You can paste text directly, drag files/photos in, or choose a file. Title/source/sensitivity are filled automatically.

```text
http://localhost:8080/
```

PowerShell text example:

```powershell
$body = @{
  text = "Remember to review this later."
} | ConvertTo-Json -Compress

Invoke-RestMethod `
  -Uri http://localhost:8080/inbox/text `
  -Method Post `
  -ContentType "application/json; charset=utf-8" `
  -Body $body
```

Expected output / 预期输出:

```text
DRY_RUN_OK
```

For full usage and roadmap, read:

- [English README](README.en.md)
- [中文 README](README.zh-CN.md)

Do not commit real personal evidence, medical records, financial records, credentials, account-security notices, or private relationship data.
