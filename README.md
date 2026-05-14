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

Expected output / 预期输出:

```text
DRY_RUN_OK
```

For full usage and roadmap, read:

- [English README](README.en.md)
- [中文 README](README.zh-CN.md)

Do not commit real personal evidence, medical records, financial records, credentials, account-security notices, or private relationship data.
