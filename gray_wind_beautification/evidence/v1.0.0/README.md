# 1.0.0 验收证据索引

- 游戏：Steam Stellaris `Pegasus v4.4.6 (fdde)`
- 语言：简体中文
- 显示：2560×1440，无边框全屏
- 启用内容：仅 `[XenoAmess的灰风美化]`
- 运行 ID：`20260913T093054Z`
- 候选包树 SHA-256：`35609a568a8add1f12eb979b5e4a620f7469d06d0dbe5c6b600caf7255172c2d`
- 正式版发布前包树 SHA-256：`5a3b29c31ab84ca7f08e88b962abd5bb0db971f80c982d2321846bee00d02350`
- 游戏 EXE SHA-256：`bc451c72d9654c8901f1bb0bee1dd78d76f415465c2fbf746e9f98ade333173a`

## 核心截图

| 文件 | 场景 |
| --- | --- |
| `gray-first-contact-effect-clean.png` | `graygoo.400` 第一次接触专用图 |
| `gray-dialogue-clean.png`、`gray-dialogue-402-clean.ocr.json`—`gray-dialogue-406-clean.ocr.json` | `graygoo.401`—`406` 对话链与透明肖像 |
| `gray-official-clean.png` | 灰风官员肖像 |
| `gray-defeated-clean.png` | `graygoo.511` 战败图 |
| `gray-return-post-reload-clean.png` | 存档重载后的 `graygoo.512` 回归图与肖像 |
| `load-game-screen.png` | 验收存档重载入口 |
| `vanilla-shared-sprite-clean.png` | 原版共享事件图未被替换 |

`clean-error.log` 与 `clean-game.log` 来自第二次干净启动。`exploratory-error.log` 保留初次探索时的无效 scope 命令错误，便于区分测试夹具错误与 Mod 运行错误。完整结果与解释见 `docs/gray-wind-beautification-release-and-test-plan.md` 第 9 节。

## Workshop 展示素材

`workshop/media/` 中的 JPEG 由本目录同名 PNG 实机截图等比例转换而来，只做有损压缩，不改变界面内容。发布时优先上传第一次接触、对话、战败、回归和官员五张；共享原版事件图是回归证据，不作为宣传图。
