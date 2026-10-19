# RC7普通吞噬月初人口独立控制

## 目标、范围与设计（实施前）

2026-10-20，root实际m04为2201.09.28、Situation16777231 progress4；候选FF29的Oct27存档已拆毁，不能作precomplete。该失败候选原件保留，不能从其完成后人口残差拟合返回R或core其他增长。root将真实重载m04，推进至Sep30并保存新的原生precomplete2；当前该前缀未封口，本线程不读。

本项只为最终Sep30→Oct1自然完成结算建立独立人口预期，不新增生产功能，不修改Mod／工具，不当作巨像guard正反例。复用root随后封口的同一原始precomplete2作为control before和真实实验before，不额外制造重复ready。root独占简中原生UI、输入、FF、保存与重载。

控制支路唯一脚本变动：对实际`eep_reg_owned_source`（须在该checkpoint重新核实typeplanet／物理1）设置`eep_destroy_done`。原生FF1到Oct1，独立保存control after；检查source仍有owner／colony／活人口，且EEP结算／成长／制造／危机积分未增加。实际命令input＋Enter与after旗互证，不把静态解析当实际执行。

生产`eep_settle_source`外层第11行要求NOT eep_destroy_done，因此此旗阻止整段返回／制造／积分／摧毁；普通`eep_task_operational`／`eep_task_ready`不读此旗，Situation仍能自然到达完成并由外围`eep_settle`销毁。单独`eep_credit_done`只跳过积分段，后续仍返回人口与拆毁，故不能用作该控制。

控制测量只采用该独立支路实际source合格主体group总量与core群组变化。为平衡onload缓存／就业影响，control与experiment两支都各自真实load同一原始precomplete2，再各自FF1；control仅多一项设置destroy_done，不省略control的reload。无需新增control-ready SAV：原始checkpoint＋control真实load回执＋唯一flag输入＋control after足够。root随后再次真实load原始precomplete2，核实destroy_done不存在、实际source/core／Situation恢复；在读取真实完成after前，把control推导的R、other及其适用假设写为固定期待，再自然FF1实验。不得使用真实完成after.eep_last_return或完成后残差反求参数。

## 验收与边界

1. 单命令长度不超过1000字符，P正文仅设置一面旗；独立离线fixture由open_kaishek现有包级入口静态检查，不注册到实机Mod列表。
2. 原始Sep30 checkpoint确实未完成、q2／T5／Situation4、source/core身份与合格群组真实可核；只接收root明确封口的角色。
3. control after日期Oct1、源未拆毁、旗存在、source/core群组与自然增长原字段完整保留，EEP奖励账本与worlds／empires未增；Situation可消失，不能要求全存档严格不变。
4. 实际load原始checkpoint去除控制旗后再实验，固定预期先于真实完成after；保留严格差异、失败与调度时序局限。
5. 此控制通过源码隔离结算与原生测量校准增长，尚不证明引擎在“源持续存在”与“当日拆毁／返回”两支路中的所有月初调度完全相同。必须比较可见growth／month_start_size／group身份，若真实结果不符先保留FAIL再调查，禁止调整R追平after。

## 静态调查结论

已只读run20261019T164112Z冻结copied_mod全目录的eep_credit_done／eep_destroy_done引用。destroy_done只用于shared settlement外层拒绝／摧毁段receipt，以及巨像目标拒绝；无岗位、人口成长、物种权利或modifier公式引用。外围eep_settle仍执行通知／母舰同步／destroy_situation，与该支路完成状态分开记录。原生人口增长字段未提供经引擎认证、可直接推导下一月精确整数增量的通用公式，因此本次采用原生独立控制，不臆造更短公式。

预定新静态夹具目录`testing/normal_population_control_1020/`，报告`docs/evidence/1019-analysis/rc7-normal-population-control-open-kaishek-1020.json`；实际control与恢复证据另由normal runtime包接收。本文先于夹具创建。

root另报告：尝试固定候选Oct27预期时，先访问`d['situations']['16777231']`，已完成Situation缺失触发KeyError，程序在write_json／write_text之前停止。未创建`r7normal-precompletion-expectations.json`或预期文档，未把已完成SAV声明为合法pre、未合成回执。Oct27诊断中的人口数值不预填控制结果。

## 实施与静态结果

唯一命令81字符，`command.json` SHA `03417a97c25f1b92e6aa2664944010f23041f62b967ee3d8f644bf5584f78cb2`。open_kaishek现有入口首次未显式传入锁定4.5.2 EXE指纹，默认身份检查报GAME_EXE_IDENTITY；语法2／2通过但整包FAIL原报告保留。随后只修正调用参数，明确使用本run EXE SHA `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`，v2报告EXIT0／PASS、P脚本2／2，SHA `912613768f10d5fcacddc36c79620ff83b9e10923305fafeee10d8d8fe7b4b7c`。未改夹具P正文、生产或工具；此PASS只限语法／包结构，运行时仍PENDING。

首次追加本节的PowerShell管道造成中文字符丢失，已在封口前用apply_patch恢复；静态命令JSON／P正文与报告未受影响。

## 完成日仍待原生验证

上述Oct1为独立控制的候选观测日期，不是已认证的自然完成日期。root另提出旗日期差2976若为小时可对应124日／Oct2，仅为待验证推断。本线程不将旗编码推断当引擎时间证明；若控制Oct1仍Situation4／未完成，则该支路只测月度人口，不能声称成功阻断了结算。真实实验Oct1若仍活，可由实际SAV成为新的precomplete3，随后以同月Oct2真实末日人口及独立增长字段固定R／other；不得把Oct1先写死为完成日。

## 收尾时已闭合的原生结果

Oct1控制实际Situation仍在progress5／未killed，source112／core5150，仅证月度增长2／5；Oct2控制仍source112／core5150，Situation原生killed=yes／progress5，源活且destroy_done／pending存在、共享结算账本未增，独立同月日增长为0／0。随后真实load同Sep30原始checkpoint再自然FF1，Oct1无控制旗pre3实际source112／core5150、Situation5未killed、source仍active且无pending／done，成为安全恢复锚点。

用户要求度假前平稳收尾，真实无旗Oct2没有执行，normal完成与原结算／幂等仍PENDING。交接候选期待由无旗pre3主体112＋独立控制日增长0得到R112、core other0、候选core5262，未使用旧Oct27或任何真实自然完成after残差；恢复时须先核实际load后的状态。本页与夹具静态工作到此封口，不继续实机。
