# 0.2.1 正式包程序性检查

日期：2026-10-15。本子任务承接[发布与剩余验收计划](release-0.2.1-and-remaining-acceptance-2026-10-15.md)，只读核验正式版本身份、相对rc.6实机冻结包的变化，以及必要包级/静态合同。不开GUI、不启动游戏或Steam、不发布、不修改生产文件/共享计划、不提交推送；相关动作由主任务负责。

## 目标、范围与验收标准（执行前）

正式唯一版本源为本Mod的 `VERSION=0.2.1`，`mod/descriptor.mod` 必须完全匹配且没有预发布后缀，`supported_version` 保持4.5.*。逐字节比较当前90文件生产包与rc.6真实运行副本 `C:/Users/Administrator/AppData/Local/xenoamess_stellaries_dev/runs/20261015T090720Z/mod/shishan-feedback-local`：文件集合相同，只允许descriptor变动，descriptor也只能version行变化；89个功能/资产/本地化文件必须相同。冻结descriptor实际版本与当前git/文档口径分别记录，不隐去差异。

先运行 `C:/workspace/open_kaishek/tools/accept_stellaris_mod.py`，显式版本源、本机Stellaris4.5.2及固定EXE指纹 `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。G1未PASS或未知域诊断阻塞时暂停，不继续把其他检查当成门禁替代。只覆盖该工具文档声明的语法/包结构、有限人口作用域与被引用script value结构；完整opcode、初始化展开及运行时不在该工具认证范围。

已读取工具README、CONTRIBUTING、包级验收、4.5.2有限scope、资产覆盖和本地化字符丢失说明；工具根没有AGENTS.md。其CLI支持 `--expected-exe-sha256` 和 `--version-file`，本次不使用旧4.5.1默认指纹。所有报告写入 `evidence/v0.2.1/acceptance/`，UTF-8/LF：G1固定 `package-open-kaishek.json`；`release-identity.json` 包含状态、正式版本、90文件路径/bytes/SHA-256清单、树哈希、rc.6比较、EXE实际身份和命令/退出码。

G1通过后执行既有 `validate_feedback_redesign.py --game ...`（六合同及十语本地化）、`audit_reward_contract.py`（149个canonical资格场景/745守卫断言）、`audit_compat_traits.py`（19映射与原版引用）。十语言必须269键，文件头/编码/引用/原始key泄漏与非中文中文占位检查通过。只改变descriptor版本时，不重跑已完成的107项相同功能回归；若发现版本相关新断言或生产额外变化则明确暂停/补充必要验证。

本轮不把前轮实机证据改写成正式版本新实机通过。独立乘算未实现；用户已允许完成调查后按有依据的加算回退验收。自然22新局/长期路线由新计划明确排除，本子任务不标记它们通过，也不扩张到其他语言实机。

## 执行记录

首次对实际运行副本完整目录的比较明确FAIL：运行副本91文件、正式包90文件，原始差异为仅运行副本额外的 `events/shishan_feedback_probe_events.txt` 加descriptor版本行变化；89个非descriptor生产文件完全相同。主任务随后明确授权并要求90文件生产投影：只排除这个已知testing夹具路径，其他任何增删仍失败。依据为 `testing/README.md` 的“生产90原样复制、夹具仅额外一个P文件”和RC6 `final-source-copy-verification.json`。不删除/修改运行副本或证据；保留91原始清单、最初FAIL与raw差异，最终另列90生产投影比较。该范围修正先记录，再继续G1。

首次正式G1、六合同、149组/745资格断言与19映射均exit0，十语269键静态通过，正式树 `ae14f3b665f43d7faad73f9fe4af9f75b2e98602208f98cfccbaa05bb6374f80`。封口时主任务发现十语反馈说明仍写“本预发布”，授权只更正为正式“本版本”对应措辞。所有初次报告已原样复制到 `acceptance/pre-wording/`，当前identity置 `PENDING_TEXT_REVISION`，避免将旧包清单误作最终发布身份。

修订检查范围先记录：生产仍90文件，允许相对rc.6投影变化仅descriptor与十个指定feedback本地化文件；descriptor只改版本行，本地化只改已指定“预发布→本版本”词组，数值、键、BOM与格式token不得改变。其余79文件必须逐字节相同，任何新增/删除或额外diff失败。待主任务通知文本完成后再重跑正式G1和十语静态；逻辑字节未变，不重跑107项无关机制回归。新增需求的后续实机验收仍与本次发布措辞修正分开。

## 最终身份与结果

最终正式 `VERSION` 与descriptor均为 **0.2.1**，supported_version仍4.5.*。90文件树SHA-256为 `835267fa011282b26bc36b4f38202489e9a5dd137bec40de1bd46596706eae94`；[release-identity.json](../evidence/v0.2.1/acceptance/release-identity.json) 为PASS，`content`映射逐项记录90文件的bytes和SHA-256，检查执行后再次重核生产字节与版本没有变化。

实际rc.6运行副本descriptor原始版本为0.2.0-rc.6，未按较新文档口径伪改历史。只排除已授权的探针后，rc.6的90生产投影树为 `566030887c51815361b4a9d3d102258c821f7eaf89b1d219241b9a6b0f597b1d`，与前轮rc.6程序报告的树完全一致。原始91清单和probe哈希保存在identity，首次raw91差异FAIL保留在 `release-identity-raw91-initial-fail.json` 与 `pre-wording/`；没有删除运行文件。

相对该生产投影，最终无新增/删除，差异精确为descriptor的version行及以下十个 `localisation/<language>/shishan_code_feedback_l_<language>.yml`，各词组仅出现并替换1次。检查直接比较原始UTF-8 bytes与预期 `.replace(old,new)` 的结果，未通过重新编码或格式化掩盖额外差异；其余79文件逐字节相同。

| 语言 | 原词组 | 正式词组 |
| --- | --- | --- |
| simp_chinese | 本预发布 | 本版本 |
| english | This prerelease | This version |
| french | Cette préversion | Cette version |
| german | Diese Vorabversion | Diese Version |
| japanese | この先行版は | このバージョンは |
| korean | 이 사전 공개 버전은 | 이 버전은 |
| polish | Ta wersja przedpremierowa | Ta wersja |
| russian | Эта предварительная версия | Эта версия |
| spanish | Esta versión preliminar | Esta versión |
| braz_por | Esta prévia | Esta versão |

## 实际命令、退出码与覆盖

工作目录为 `C:/workspace/xenoamess_stellaries_dev`，下列命令均实际执行、退出0。G1严格先于Mod合同复核；其未知域没有被豁免，最终errors为空。

```powershell
python -B C:/workspace/open_kaishek/tools/accept_stellaris_mod.py --mod shishan_code_origin --version-file shishan_code_origin/VERSION --game 'C:/Program Files (x86)/Steam/steamapps/common/Stellaris' --expected-exe-sha256 400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83 --report shishan_code_origin/evidence/v0.2.1/acceptance/package-open-kaishek.json
python -B shishan_code_origin/tools/validate_feedback_redesign.py --game 'C:/Program Files (x86)/Steam/steamapps/common/Stellaris' --report shishan_code_origin/evidence/v0.2.1/acceptance/feedback-contracts.json
python -B tools/shishan_code/audit_reward_contract.py --game 'C:/Program Files (x86)/Steam/steamapps/common/Stellaris' --report shishan_code_origin/evidence/v0.2.1/acceptance/reward-canonical.json
python -B tools/shishan_code/audit_compat_traits.py --game 'C:/Program Files (x86)/Steam/steamapps/common/Stellaris'
```

| 检查 | 执行阶段 | 结果与报告 |
| --- | --- | --- |
| G1 | 初次正式包及措辞修正后各一次 | PASS、25/25脚本、13DDS、269键；最终[package-open-kaishek.json](../evidence/v0.2.1/acceptance/package-open-kaishek.json) |
| 既有Mod合同与十语静态 | 初次正式包及措辞修正后各一次 | 六合同PASS；[feedback-contracts.json](../evidence/v0.2.1/acceptance/feedback-contracts.json) |
| canonical候选 | 初次正式包一次；修词后未重复 | 44个原版文件、20机械候选、149场景/745守卫断言PASS；`reward-canonical.json` |
| 19兼容映射及原版引用 | 初次正式包一次；修词后未重复 | PASS；`compat-traits.json` |
| 正式版本/清单/差异/EXE身份 | 修词前后及最终稳定性核对 | 最终PASS；`release-identity.json`、`checks-summary.json` |

两个canonical/compat结果明确复用措辞修正前实际执行的exit0报告，对应机制文件及其base/compat引用翻译未改，不伪写为修词后重新执行。四类命令的完整argv、退出码、stdout/stderr分别在 `package-command.json`、`feedback-command.json`、`reward-command.json`、`compat-command.json`；最终identity把后两者列在 `reused_commands`，最初失败诊断另留，不改成成功退出码。身份核对使用只读 `python -B -`：逐路径计算bytes/SHA、核唯一版本行、逐语精确byte替换、排除唯一已授权probe并要求其余路径无增删，结果与执行角色/退出码同时记录。

最终EXE实测SHA-256与固定预期完全相同：`400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`，launcher rawVersion为v4.5.2。有限scope profile检查202处、3文件、零诊断；被引用script-value形状预检按工具原样报告NOT_APPLICABLE/0，并不扩张为完整script-value语义认证。

十语50文件、每语269键、2080引用、154显式脚本键及1引擎自动modifier键静态通过；完整中文名称仍18汉字/54字节。BOM、语言头、键集合、引用/token、原始key泄漏和非中文中文占位检查通过。非简体中文运行时不在范围内。所有新JSON均UTF-8/LF，修词前11份JSON完整留在 `acceptance/pre-wording/`，未覆盖原始身份快照。

前轮107项功能回归不重跑：79个非措辞/descriptor文件字节相同、十语仅经授权人类可读词组更正，受影响G1与本地化已重跑；原有机制测试没有版本身份断言。主任务新建发布适配器自身测试归其独立任务，本子任务不将它们算入107项或宣称已执行。

本结果只说明正式发布输入身份与这些包级/程序检查通过。没有启动游戏、上传Steam、验证远端、操作GUI或修改生产；前轮实机记录保持其真实版本和限制。本轮不将未注册opcode、完整初始化展开、自然长期路线、独立乘算或非中文实机写为通过。
