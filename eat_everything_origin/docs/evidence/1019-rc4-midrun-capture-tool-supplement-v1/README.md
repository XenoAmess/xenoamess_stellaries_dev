# Midrun UI-capture-tool supplement

固定run `20261019T133314Z` 的工具源码补充，不是最终日志归档或Mod验收。`selection.json`为完整白名单；`index.json`保存63个原始payload（2,645,849字节），`verify.json`独立复核源／副本SHA、19个canonical引用、9组图片／OCR与Git原字节属性。

新runtime为 `84b7fdda9489392f5abab5fc71c9bd61bcc5933185a02f7c6c479d703b155ffc`，旧runtime为 `91b831241440a04ffa55d7226c7e2eb158907ebdc62054a906ff51e9f5e77adf`。18个当前本地Python依赖中，9个有既有canonical基线：仅runtime改变，其余8个一致；另9个没有本补充可用的旧基线，不能据此声称未变。原manifest／source-copy／gate／receipt及较早phase-B包未改。

worker86592由root内联Python启动，没有保存的worker脚本，也没有进程内存loaded-source证明。首次已归档新工具输出为UTC14:25:59.590788。原生load在HUD日期校验失败；施伤／保存／导出未运行。短worker25428与36308的play0尝试均被guard拒绝，未输入命令。工具既有3×15003枚举等价与6测试PASS只用于工具范围。

游戏PID36912仍加载RC4 tree06485；磁盘工作区RC5没有加载到该进程。原始load／HUD及两次拒绝尝试34个文件被保留，随后直接探针与停止后日志在独立最终run包保存。
