# 白绮凝聚力维护修正的显示键补全

日期：2026-10-15。实施前记录。主任务在本轮真实日志中发现 `mod_leaders_unity_upkeep_mult modifier is used but not localized!`。正式特质已使用原生 `leaders_unity_upkeep_mult=-1`，但十语言没有对应修正名称，可能导致提示显示原始 key。

目标与范围：只在十份 `mod/localisation/<language>/shishan_code_feedback_l_<language>.yml` 各新增同一个 `mod_leaders_unity_upkeep_mult` 显示键。简中为「领袖凝聚力维护费」，英文为「Leader Unity Upkeep」，其余语言使用对应翻译，不放简中占位。只补维护资源及领袖范围的名称，不增加或修改维护机制、数值、特质、脚本、VERSION 或 CHANGELOG。

原版 `megacorp_l_<language>.yml` 的 `mod_leaders_upkeep_mult` 可提供各语言的领袖/维护术语参照；本次补充 Unity 资源限定，避免显示为所有领袖资源维护费用。修正百分比仍由引擎按照原数值显示，不在名称中硬编码 `-100%` 或保证最终费用为零。

静态验收：十文件都恰有一次新键且值非空；保留 UTF-8 BOM、语言头、现有键值及名称正文修复；全语言键集一致、引用与格式完整、没有简中占位或原始 key 泄漏。运行既有本地化静态检查。主任务统一执行重启前 G1，并以新运行日志和简中领袖提示复核，静态检查不能代替实机通过；其它语言运行时不在范围内。

本任务只修改上述十本地化文件及本独立记录，不操作游戏、Steam、桌面或正在使用的冻结候选。实施与静态结果随后补充。

## 实施与静态结果

十语言新键已补全。只读执行既有 `check_localisation`（带本机原版目录）通过：50 个文件、每语 269 键、2080 处引用、154 个脚本使用键；新增引擎修正显示键 `mod_leaders_unity_upkeep_mult` 已进入校验清单。十语言的新键都恰好一次、非空，中文逐字为「领袖凝聚力维护费」，英文为「Leader Unity Upkeep」，其余使用各自翻译。现有完整机制名正文引用与分段保留，UTF-8 BOM、语言头、引用及 whitespace 检查通过。

开发过程中首轮通过 Windows PowerShell 管道传递非 ASCII Python 源码时，管道默认 ASCII 曾把新标签转成问号；发现后立即撤换为纯 ASCII 源码中的 Unicode 转义，并逐一按 UTF-8 读回比对精确标签。最终十标签均无问号替代，原有文件内容仍保持。本次经验用于文本工具：不能仅凭 Python 无异常就判断非 ASCII 写入正确，必须读回核对字符或码点。

九种外语为**静态校验通过，运行时不在范围内**。新候选的 G1、真实日志与简中白绮提示复核由主任务统一执行，当前本项实机结果仍为 **NOT RUN**。没有改变 `leaders_unity_upkeep_mult=-1` 的数值或其作用域，也不因此宣称所有其它正倍率下都严格零维护。
