# 2026-10-15 实机证据索引

主结论、范围和执行顺序见[实机验证记录](../../../runtime-feedback-validation-2026-10-15.md)。本目录是精选原始证据，不是所有文件都代表通过。

| 目录/文件 | 来源和含义 |
| --- | --- |
| game-update-offline.json、steam-offline-window.png | Steam public/build/安装验证完成、离线状态；只保留必要客户端窗口 |
| rc1-loading-failure-* | 首次真实加载的三类引擎错误，原始失败不覆盖 |
| static/ | open_kaishek各候选报告、最终107测试及资格/本地化静态报告 |
| rc2/ | run071829Z：修加载后发现NOT真值/候选混层失败，以及旧计数23/24原生档 |
| rc3/ | run074214Z：三选一/重抽/长名修复；envoy、头像及资格失败保持原样 |
| rc4/ | run080652Z：国内迁移修复与3→2→1→0前缀；同日清理误耗尽/R1的失败、原生缓存探针 |
| rc5/ | run084453Z：初始1/.75、普通维护自然进度与完成、白绮维护1.0失败及自然XP20种子 |
| rc6/ | run090720Z：最终候选；个人免维护/XP25重启、实际模板克隆、清理/优化/复发交叉和旧重复层重载 |
| rc6-numeric/ | run094102Z：同一冻结候选补测实际J500/月速0.2与III–V阶段工具提示、跨月预算；含最终离线/退出复核 |

`.sav`由真实游戏中文保存菜单写出，配套`.native-save.json`记录路径、meta和SHA；没有手写期望gamestate。`.jpg`为新生成的Steam F12 GPU帧，`.ocr.json`含匹配帧哈希与识别坐标；OCR/输入失败截图亦按实际失败保留，不能据截图存在判PASS。独立只读审计保留严格缓存FAIL和序列化观察，不能被限定delta比较PASS覆盖。

rc1–3归档error/game/system三份完整日志文件；rc4及之后的`native-logs.zip`保留对应run完整logs目录，末轮另有日志分类。仅简体中文实机，其余九语言是静态校验通过、运行时不在范围内。跨候选复放在各报告明确标注，不伪称同一run从头连玩。真正自然科研、engine complete_special_project、显式复发凭证输入分别记录。

各子目录`evidence-files.json`及根清单按相对文件名/字节数/SHA-256核验归档；清单自身不自哈希。正式生产Mod不包含这些存档、探针或测试工具。
