# RC6 成长原始链：保留失败

固定run `20261019T150008Z`、RC6树 `cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a`。473个payload共27,154,271字节：455个原r6g文件（26,146,209B，22份SAV）、16份原报告／计划、2份工具磁盘快照。18份成长样本、36个原矩阵命令及独立Enter、72组fresh Steam GPU截图／OCR、全部已有repeat／reload／诊断动作与回执完整保留。18个canonical引用复用经济年末锚点、manifest、静态gate、四个事前模型与旧工具来源，未复制整Mod或经济SAV。

| 原九节点报告 | 检查数 | 原失败数 |
|---|---:|---:|
| C0 | 170 | 1 |
| C9 | 170 | 2 |
| C10／19／20／49／50／200（各） | 174 | 2 |
| C10000 | 174 | 9 |

九份报告均保持 `FAIL_OBSERVATION`，合计24项失败原样保留：17项旧government raw跨月比较、7项n08真实modifier导出失败。独立government补充只认证其声明的身份范围，不批量抹掉原失败。n08两份真实账本均R200，104只是旧缓存数值反推，不是已有中间SAV账本。

post-matrix独立只读抽取见 `post-matrix-observation-v1.json`：

- n08 final与两次 `eep_sync_mothership` 后的r6grepeat ZIP完全相同，SHA `5115fb184de72db0afe4ff5baf0b645013275a5a6df572f0d75dc086092243fa`。这不是完整initialize／startup重复初始化case。
- 精确r6gload收据载入r6grepeat，原生日期验证true、原 `state_verified=false` 保留。r6greload SHA `b23e00c98b5bd3ecf5fe3c496e500f0049ba7822ee030e49d102405c39d53c91`，与repeat ZIP不同。所抽日期、country／fleet／ship变量、三防与设计体SHA相同；design ID从1527变为16777235，government原始块SHA改变，均保留为差异／未解释，不声称完整重载通过。
- r6gexport1 SHA `93e3f5826f10873f28a983f0660a446bdfba881d9dd6e82f8231085d5f0f4850` 的十个新导出与原C0截距、事前模型系数相符。它是较晚的独立样本，不能替换n08七个旧导出失败。
- r6gbudget1 SHA `983e06cd8af63e4b5e35b02d1fe8d639e321ea62ebb8ef0c02eaca263ecf3925` 记录C20500／L2050／B410，R200→300、P110、六阶合计300。原设计单次补200的预期为R400／P10，实际仅补100，**FAIL**。不修改预期获得通过。

index SHA256 `0434a330904ce63ffe665cc5e6a207074f144b005efce052958086e89d06c54a`；post-matrix观察 SHA256 `7a251f03f0c7a42bc53a9a78a6e9359c060e13fe78f19e0a5a03eb77bddee6c0`；独立verify SHA256 `40a7e2ed76ce1b77a6e1fdb884c2858f83735158f3f63b7b17f3bee8b75e9ab9`。

独立verify的11项仅认证冻结SHA、原生ZIP完整性、角色和输入绑定。首次复核因两份工作源在复制后推进而停止；该失败与两个新旧SHA已留在verify中：root probe文档10770bd9…→f3f6ebfa…，checker0c31f764…→RC7 a8d70f10…。473冻结副本SHA正确，471份当前source字节一致；另外两份在capture时完成source／copy逐byte核对，保留旧快照，不假称当前source仍相同。原collector快照cab98ce…匹配原receipt，旧a66及修正0c31工具各自保留来源边界；没有历史进程内存证明。

完整停后日志另见 `docs/evidence/1019-rc6-final-logs-v1/`。其完整error.log第24行真实记录while100次中止；历史nomads未解释项继续保留。本包不复制logs、不改旧progress／原样本／原报告，不读取RC7指针或运行，不操作UI／Git／Steam／生产／root工具代码。成长及整Mod验收均未通过，未创建final-result。
