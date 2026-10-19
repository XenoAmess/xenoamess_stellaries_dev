# 旧 public031 受伤夹具运行完整归档

run `20261019T130448Z`／PID5216 于 UTC `2026-10-19T13:32:28.045820+00:00` 正常退出，`forced=false`／`running_after=false`。独立 CIM、复制前后和独立复核均确认该源 PID 不存在；本线程没有停止游戏或操作 UI。

共418个原文件、27,252,632字节：停止后的19日志（含全部5份script_documentation）、3份运行证明、7份原生SAV及其对应UI／actions／receipts／audit、14份稳定分析、3份EEP05候选修复证据和旧运行实际预设。完整原始路径／逐文件bytes／SHA256见 `index.json`，SHA256 `f78fab26099320e7306995a19d25e181b858db520ce63954295efdf7c2833208`。复制前后源集合和原件／副本一致；`verify.json` 再读全部418原件／副本、5份canonical引用，核7组SAV／receipt／audit／gamestate、82组截图OCR绑定和两个别名。`git-byte-verify.json` 证明全部418原文件的Git blob保持原字节。

47文件 public0.3.1 Mod tree `abca9b4195a991d98ca25336ed7807e0306d30e2c33021e4d307f78e1db864d8` 复用 `../1019-analysis/legacy-damage-preparation-v1/` canonical 准备包，不再复制Mod树。十一件已付款队列原件 j13ten 的来源为0.3.0-rc.1；本次载入、施伤、重新保存使用 public0.3.1，两者在原始报告中分开保留。

七份成功原生保存严格为 ld031clean／ld031hurt／ldpaidclean／ldpaidhurt／ldpaidarmor／p031before／ppaidbefore。src031hurt、srcpaidarmor是原字节别名，不是另外的成功阶段；没有ld031armor。最初两个装甲未伤的FAIL（22／23、27／28）、装甲中间态OBSERVATION_ONLY21，以及最后两个partial限定报告PASS_SCOPED28／29，全部原样保存。最后两档的舰体／装甲／护盾均为正值且低于最大值；public严格26项、paid严格20项差异仍为FAIL，未忽略原生缓存／设计索引变化。RC4迁移模板的load／sync／reload仍null，不能称迁移通过。

generic `ld031-hurt-reload` 失败是调用方严格目标标签查找失败：原生列表截图与OCR实际读到 `Id031hurt`／`Id031hurt.sav`（capital I），并非OCR引擎失败。该尝试的load-window／initial-page-0图、OCR及动作完整保留；没有成功load receipt。worker61189异常文字仅在root会话，没有伪造独立failure JSON。随后使用两个raw alias恢复，原始失败没有被覆盖。

EEP05证据包括picker、edit-design、editor-unmodified、completion-hover-basis、error-tooltip等全链。真实未改设计的红色提示是“统治者外观：统治者性别未选定。”，截图与OCR相符。旧userdir预设仍为b3cee；候选单字段`ruler.gender`从not_set改female后的4ce9另存为fixture-before／after／repair报告，不倒填旧输入；修复后新RC4实际可选／开局仍待验证。

完整error.log23行全部与历史baseline仅时间不同：21缺失Workshop发现、1consume覆盖、1portrait_container；game.log3条版本／defines信息；debug.log1条缺建筑类别警告与baseline相同，但未给建筑key，具体对象／影响仍未解释。详见 `review.json` 与 `review-verify.json`。此旧run未见nomads错误，不改变其它run已有nomads因果未解的结论，也不作“无害／整Mod通过”声明。

本归档只证明来源、字节和限定旧档夹具／EEP05提示；未修改Mod、工具、SAV或旧userdir输入，未操作Steam或提交。
