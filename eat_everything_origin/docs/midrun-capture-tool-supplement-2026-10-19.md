# currentrun133314Z 中途截图工具补充取证

## 目标与范围

为仍在运行的 `20261019T133314Z` 增补当时实际工具源码字节，不改原始 manifest／source-copy／receipt。root 在约本地22:25（UTC14:25）启动 nrel 校准 worker86592，导入当前 `runtime.py` SHA256 `84b7fdda9489392f5abab5fc71c9bd61bcc5933185a02f7c6c479d703b155ffc`。原运行／既有v3执行源码使用旧 `91b831241440a04ffa55d7226c7e2eb158907ebdc62054a906ff51e9f5e77adf`，必须两者并列，不回填为从启动就用了新工具。

游戏实际加载的 copied Mod 仍为 RC4 tree `06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468`，game PID36912。仓库 working Mod 已是 RC5，但未加载到这个进程；截图枚举工具变更不称 Mod tree 变更。worker86592仅按root交接记录为执行worker／session标识，不冒充Windows游戏PID。

只读复制当前runtime／single-homeworld／1019／1015、共享 `tools/stellaris_acceptance.py`、audit／inspect／check及可静态解析的本仓库Python依赖闭包原字节，保存依赖解析路径和各hash。额外保存旧runtime原字节、release工具线程已封口的枚举／缓存基准、6测试源码及文档，以及nrel导入receipt和已稳定的原生载入／HUD重查图、OCR／动作。只读源码解析，不导入执行UI模块、不重跑游戏或测试、不复制活动logs或整Mod树，不操作UI／Steam，不修改Git状态。

## 工具变更依据与边界

release线程确认本次仅新增 `screenshot_mtimes` 的scandir／DirEntry.stat枚举并替换before／fresh两次扫描，原固定叶目录／jpg／mtime／max／12s与轮询间隔保持。3轮每轮15003路径与mtime逐项相同，6测试PASS；已有OCR缓存复用基准另存，single-homeworld源码hash没有变化。这些是工具静态／基准结果，不等于新native帧或Mod用例通过。

nrel计划为 `docs/native-relic-health-calibration-1019.md`，`nrel-source-import-receipt.json` 只证明原始r4relic6→nrelsrc原字节导入。root补充精确交接：worker86592是 `exec_command` 的内联 PowerShell here-string 经管道传给 Python，没有预先保存脚本文件；流程为将tools加入sys.path、导入runtime1019、从方案正则提取3条commands、调用 `b.r.native_load('nrelsrc', 'nrel-source-load')`。该调用在HUD日期校验异常结束，后续施伤／保存／导出均未运行。两个短worker25428、36308尝试 `b.console` 的play0，都被“控制台未可见打开”的guard拒绝，未输入play0。这里只保存已完成的load／HUD与两次拒绝尝试的固定文件白名单，不编造成功load receipt、失败JSON或实际worker源码路径。

工具封口后导入的时间与流程由root交接说明；源码磁盘SHA及原始动作／OCR可独立核查，但没有进程内存中的loaded-source取证，不宣称磁盘SHA证明所有历史Python进程实际加载了该SHA。较早phase-B checkpoint只保留原工具基线和原始引用，不把边界不明的中间样本回填到新工具。随后root已通知该run于UTC14:34:31.898945正常停止；完整最终日志与其余探针将另建停止后归档，本补充范围保持工具切换与明确失败片段。

## 实施与验收

先落完整工具／基准／证据白名单，再原字节复制，逐源／副本bytes与SHA256复核，生成独立index／verify；旧runtime与新runtime并列，旧manifest引用保持原hash并只作为canonical引用。记录当前工具文件中无法找到旧基线的项，不据“没有旧hash”声称未变。已知有旧canonical对应的依赖逐一比较。

检查点必须声明`midrun UI-capture-tool supplement`、非最终run冻结、非Mod验收；受影响范围只从root明确导入新工具的nrel阶段开始，先前raw checkpoint和receipt不重写。完成后给root路径、payload数、新旧hash及边界，统一由root提交。

复核实现发现Windows Git的 `hash-object --stdin-paths` 传入反斜杠绝对路径时，CRLF文件可能未按相应目录的 `-text` 属性处理，而 `check-attr` 仍显示text unset；因此本补充统一使用正斜杠路径，确认filtered／no-filters对象hash逐项相同。原始文件bytes未改变。

## 已完成结果

归档为 `docs/evidence/1019-rc4-midrun-capture-tool-supplement-v1/`：63个payload、2,645,849字节；index SHA256 `3121471f1b26a7607188e151c8ba979ec1d34fb5948fc211baa9db1ec9230e71`。18个当前源码闭包、1个旧runtime、7个封口工具结果／测试／文档、1个nrel方案、2个原run元数据及34个固定失败片段原字节全部复核。9个有旧canonical的源码只有runtime变更，另8个一致；其余9个没有本补充旧基线。独立verify同时确认19个canonical引用、9个图／OCR绑定及63个Git原字节对象。

首次已归档新工具输出UTC14:25:59.590788；worker启动及导入顺序来自root交接，实际磁盘SHA与图片指纹单独可核，未获取内存loaded-source证明。结果是证据绑定静态复核通过；HUD load FAIL、施伤未运行和两个play0 guard拒绝保持原结论，不构成Mod通过。
