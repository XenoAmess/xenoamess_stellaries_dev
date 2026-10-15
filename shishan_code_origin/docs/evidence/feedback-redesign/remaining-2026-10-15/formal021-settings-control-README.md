# 正式重载、无Mod设置对照与1280正文证据

2026-10-15。三个run均由主任务实际操作并正常停止后归档，`forced=false/running_after=false`。归档者只读原始文件、逐字节复制证据和核对哈希，没有操作GUI、切换current-run、启停进程或修改原日志/存档/生产。

[对照JSON](localization-settings-control-comparison.json)记录两个实际加载集、完整原始8行和只去掉首个`[HH:MM:SS]`后的逐行比较。结果为**8/8按序逐字相同**，包括game_text.cpp行号、promotion/property名、中文及U+0011。两份原始error.log各29行：21条已有descriptor提示及8条本地化诊断，全部保留；完整停机logs各19文件另存zip并逐entry核SHA。

| 样本 | 实际输入与范围 | 核心原始证据 |
| --- | --- | --- |
| 正式0.2.1 run103709Z | 简中、固定4.5.2 EXE、唯一启用正式90文件Mod；windowed1600×900/请求0.75/debug。8条在读档前打开设置同秒产生；随后真实重载两份旧种子并保存。 | [manifest](formal021-no-fixture-run103709/manifest.json)、[实际dlc_load](formal021-no-fixture-run103709/userdir-dlc_load.json)、[正常停止](formal021-no-fixture-run103709/stop.json)、[完整29行error.log](formal021-no-fixture-run103709/error.log)、[完整logs.zip](formal021-no-fixture-run103709/logs.zip) |
| 无Mod run110858Z | 同EXE/简中，实际enabled_mods=[]，no-debug、borderless1280×720；菜单9776，首次原生设置显示默认1.0x，仅主菜单/设置，没有加载游戏或新原生SAV。 | [manifest](vanilla-settings-control-run110858/manifest.json)、[实际dlc_load](vanilla-settings-control-run110858/userdir-dlc_load.json)、[正常停止](vanilla-settings-control-run110858/stop.json)、[完整29行error.log](vanilla-settings-control-run110858/error.log)、[完整logs.zip](vanilla-settings-control-run110858/logs.zip) |
| 正式1280 run111512Z | 正式90文件无夹具，同EXE/简中/no-debug，实际backbuffer1280×720/scale1.0；两政体真实首都决议打开正文。此run没有打开通知设置，error.log仅21条descriptor提示、其它0。 | [manifest](formal021-min1280-run111512/manifest.json)、[独立显示核对](formal021-min1280-run111512/independent-formal1280x1-display-check.json)、[完整21行error.log](formal021-min1280-run111512/error.log)、[完整logs.zip](formal021-min1280-run111512/logs.zip) |

该实际无Mod样本证明这8条同一签名诊断的出现不以本Mod、debug_mode或其奖励/物种状态为必要条件，支持先前原版文案来源定位。两run分辨率/缩放/debug等输入不同，所以这不是严格只改变一个变量的效应大小试验，也不等于完整引擎因果轨迹；不能扩称所有配置均无间接影响、没有其它错误或未执行UI/功能矩阵通过。8条仍是真实诊断，作为本构建可无Mod复现的设置本地化签名单列，任何新增或不同诊断继续单独调查。

## 正式重载及来源调查

- [新保存的普通领取档](formal021-no-fixture-run103709/formal021_claim_reload.sav)和[原生来源记录](formal021-no-fixture-run103709/formal021_claim_reload.native-save.json)：同日2209.11.28，对[rc.6真实源](../runtime-2026-10-15/rc6/fb456_natural_claim.sav)；[独立raw审计](formal021-no-fixture-run103709/independent-formal021-claim-reload-audit.json)保留核心状态PASS与严格raw不变9PASS/3FAIL，未隐藏rights去重、外国人口就业转移和预算缓存变化。
- [新保存的高R旧档](formal021-no-fixture-run103709/formal021_legacy25_reload.sav)、[原生来源记录](formal021-no-fixture-run103709/formal021_legacy25_reload.native-save.json)及[额外种子来源](formal021-no-fixture-run103709/extra-seed-saves.json)逐字节归档。源为[rc.6真实高R重载档](../runtime-2026-10-15/rc6/fb456_legacy25_reload.sav)，后补[architecture独立高R审计](formal021-no-fixture-run103709/independent-formal021-high-r-reload-audit.json)原字节SHA5d963809…73915ad；核心14PASS、U43/R25/T68/B3.4/scale68及旧k保留，国内领袖含白绮/全478领袖raw一致，整体原始区段差异仍保留。本索引不据保存行为宣称其它未执行分支通过。
- [原始8条来源调查JSON](formal021-no-fixture-run103709/independent-formal021-localization-diagnostics.json)按四个原版简中通知键定位原文件/行号/SHA，保留当时“only source attribution, not yet causal reproduction”的历史边界；后续实际对照结果以本目录新的对照JSON为准，不重写旧报告。
- [正式普通架构正文原图](formal021-no-fixture-run103709/formal021-normal-architecture-body.jpg)、[OCR](formal021-no-fixture-run103709/formal021-normal-architecture-body.ocr.json)及[高R正文原图](formal021-no-fixture-run103709/formal021-high-r-architecture-body.jpg)、[OCR](formal021-no-fixture-run103709/formal021-high-r-architecture-body.ocr.json)保留主任务实际可见证据。分辨率/缩放循环的所有现有原图、OCR、操作和原始JSON均在同目录，不因界面疑问或失败而筛掉。

## 无Mod可见证据

| 原生画面 | 图与OCR |
| --- | --- |
| 菜单版本Cygnus v4.5.2（9776） | [原图](vanilla-settings-control-run110858/vanilla1280-menu-first.jpg)、[OCR](vanilla-settings-control-run110858/vanilla1280-menu-first.ocr.json) |
| 首次设置的1.0x默认缩放 | [原图](vanilla-settings-control-run110858/vanilla1280-default-settings.jpg)、[OCR](vanilla-settings-control-run110858/vanilla1280-default-settings.ocr.json) |
| 通知设置页 | [原图](vanilla-settings-control-run110858/vanilla1280-notification-settings.jpg)、[OCR](vanilla-settings-control-run110858/vanilla1280-notification-settings.ocr.json) |

## 归档完整性

正式目录保留295个选定顶层原始文件（初次293加后补独立高R审计JSON及其既有一次性审计Python来源副本，包括2SAV、51图、51OCR、全部action、审计、manifest、extra-seed、settings/dlc_load快照及原始error/logs.zip；Python只复制取证、没有执行或加入Mod）；无Mod目录保留28个（包括6图、6OCR及action/manifest/停止/设置/日志）；正式1280目录保留108个（包括27图/27OCR、独立显示审计和全部action/manifest/extra-seed/设置/日志，没有新增SAV）。各目录另有[正式归档清单](formal021-no-fixture-run103709/archive-manifest.json)、[无Mod归档清单](vanilla-settings-control-run110858/archive-manifest.json)及[1280归档清单](formal021-min1280-run111512/archive-manifest.json)，记录每个复制文件的bytes/SHA及zip内部19个日志的bytes/SHA。它们只枚举本次快照，不假定后续其它agent新生成文件已经收录。

[总文件哈希清单](formal021-settings-control-file-manifest.json)覆盖上述三个独占目录、本索引和对照JSON；清单本身不递归自哈希。所有复制文件逐byte相同、SAV未经编辑，原始JSON中的绝对来源路径保留其原始provenance；新的导航引用均为仓库内相对路径。本档案不包括任何新P语言夹具或生产修改，不需要把旧验收输出改写为新语义PASS。

## 1280×720/1.0正文子样本

独立直接查看[个体机械原图](formal021-min1280-run111512/formal1280x1-individual-architecture-body.jpg)与[机器智能原图](formal021-min1280-run111512/formal1280x1-machine-architecture-body.jpg)，并核对应[个体OCR](formal021-min1280-run111512/formal1280x1-individual-architecture-body.ocr.json)/[机器OCR](formal021-min1280-run111512/formal1280x1-machine-architecture-body.ocr.json)的原图SHA及实际1280×720尺寸。两张正文均可逐字读到18字完整名称，统计和“关闭”按钮没有互相遮挡；个体P5474/U7/R0/T7/B0.35，机器P5567/U43/R25/T68/B3.4。原生紧凑标题依然省略，正常首都决议到全文正文路径可达，省略事实没有隐去。

个体关闭有实际click和随后画面；机器这里只证明关闭按钮完整可见，不补造实际关闭动作。该run只有这两份来源和这一显示组合，没有新原生保存，不把图中文字当成新的全部raw状态审计，也不把1280正文两样本改成UI-04全分辨率/全状态矩阵PASS。
