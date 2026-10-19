# RC6停止后非while错误：来源与发行边界

## 目标与范围

本次独立只读核查已封存RC6 final `error.log` 的21条Mod发现失败、1条原生决议重定义和1条帝国选择页`portrait_container`错误。while缺省100导致的真实EEP错误已由主线程确认并在RC7另修，本页不重审或回填RC6通过。目标是为之后RC7停止日志建立可复核的来源分类，不能只因为旧日志存在就当白名单。

只读封存日志、封存manifest/包源、当前精确原版定义及既有0.3.1基线。核对每条原文/位置/哈希、所属VFS文件和当前包覆盖边界；需要同构证据时比较移除时间戳后的完整记录，不能模糊关键对象/路径。若原版源、基线或包结构不能解释完整因果，明确保留未知影响。

本页仅新增调查文档和来源报告，不修改生产、工具、包、既有日志、SAV或Git，不运行UI、原生effects或游戏进程。不把源分类或启动成功当作Mod功能验收。

## 输入与判据

封存输入为`docs/evidence/1019-rc6-final-logs-v1/logs/error.log`，3195字节，SHA256 `b8a0cc17158bf05ebde64f42ed71ec17bd12687d5488fb8d6e7d462ceaf740f6`；第1–21行发现失败、第22行决议重定义、第23行portrait、第24行真实while错误。归档代理已封存原始字节，本页不会改写它的UNKNOWN_IMPACT/UNEXPLAINED原结论。

判据：每条分类必须有实际源或精确基线支持；区分环境发现、Mod有意覆盖、原版UI调用/结构以及真正未解释缺陷。来源可解释不等于所有影响无害；最终RC7必须独立完整审查新停止日志，不能直接继承RC6分类数量或任何通过状态。

## 结果

23条非while记录均与公开0.3.1基线中的对应记录完全同构：只将首个`[HH:MM:SS]`替换为固定时间占位，其余完整文本、对象名、路径及顺序逐字相同。基线原件SHA256为`f467f81b914d803795eb328ce56464c72d9b320cc25b7c6edf216a367173eb56`，其原始归档索引也记录同一SHA；两个manifest绑定同一EXE `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`、简体中文和单一EEP启用项。此处的基线比较只是来源支持，以下另核源结构，不能据此称错误无害。

| RC6行 | 数量 | 有依据的来源分类 | 仍未证明 |
| --- | ---: | --- | --- |
| 1–21 | 21 | 原生`dlc.cpp:1847`对Steam登记物品的发现失败 | 引擎何种内部条件拒绝这些实际存在的目录/文件，以及影响 |
| 22 | 1 | Mod有意覆盖一个原生决议键，引擎明确选中适配器 | 非EEP实机回归及其它同键Mod的兼容性 |
| 23 | 1 | 原版窄版帝国条目缺少引擎请求的container | 完整头像子功能影响、无Mod控制中是否必现 |

RC6的真实while失败仍保持第24行原样，不属于上述来源分类；本页未作RC6或未来RC7通过判断。

## 21条Workshop发现消息：环境来源已绑定，内部失败条件未解

只读本机`C:/SteamLibrary/steamapps/workshop/appworkshop_281990.acf`，SHA256 `073a3ad2f0b123d0cbe8764fa389009fa20cde7ce0b29476850acfbed0aa1792`。`WorkshopItemsInstalled`与`WorkshopItemDetails`各登记22个ID；日志21个ID均精确落在两组登记中，唯一未列入这21条错误的是当前公开物品3815707212。新报告保留全部21个ID和原始完整记录，不用泛化正则吞掉其它Workshop错误。

**不能把这些消息解释成“21个目录不存在”。** 调查时21个目录全部存在，也全部有`descriptor.mod`，抽检3710613857、3797257579、2660548454还实际包含common等内容。目录/登记状态是RC6停止后的当前只读观察，并不倒填为启动当时状态。原生消息虽然说`Could not find files for mod`，本次没有引擎`dlc.cpp`内部实现或反汇编控制流，无法证明其确切拒绝条件；不猜权限、旧注册、加载器兼容或缺文件为根因。

可以独立确认启用边界：RC6封存manifest只有`mod/ugc_eep-1019.mod`，0.3.1基线只有`mod/ugc_eep-single-homeworld.mod`。RC6冻结59个生产文件逐件匹配manifest；包文本没有这些发现路径，descriptor无`replace_path`或Workshop路径。登记/发现某物品不等于该物品已被启用。这足以将21条定位到本机原生Workshop发现环境，而非将它们算作本次EEP脚本堆栈；仍不足以宣布其影响无害或称本机“日志零错”。

## 决议重定义：有意的单键适配，存在同键兼容边界

精确原版`common/decisions/02_special_decisions.txt:1704`定义`decision_lithoid_swarm_consume_world`；冻结RC6的`common/decisions/zz_eep_native_decision.txt:2`再次定义该键，且该文件只有这一个根键。原始日志明确表示采用后者。包没有覆盖整份`02_special_decisions.txt`，不是不明对象冲突。

原版完整文件SHA256 `4f3c79276393854943b0c386a69dbff8cae9146537475309b0a48bfbe1ab77cf`，RC6适配器SHA256 `afb47a2cf28b88cfc80e8b46fc81860178aaf544b6f7bffba785cd8ab37fad9c`，与封存manifest一致。只忽略注释和空白，非EEP `effect.else`的95个token与原版完整`effect`完全相同，归一token SHA256均为`629c43c41eb709cc87c47d887b2a7fae87f694a815dd6628adb45e9ffff6ac7f`；AI权重也逐token相同。icon、sound、important、resources、owned_planets_only五项共同字段相同。

非EEP owner下的潜在条件也可明确约简：第一个新增OR只剩原生`can_have_habitable_deposits=yes`；第二个OR只剩原生`is_capital=no`；原生lithoid/nomadic、being_devoured和nanotech条件仍在。新增allow的EEP if不执行，effect走上述原生else。这解释了适配目的和静态非EEP路径，不是非EEP实机验收。其它Mod若也重定义该键，仍需按实际加载顺序重新验证，不能承诺无冲突。

## portrait_container：原版窄条目与引擎请求不一致

本机原版`interface/select_empire_design.gui` SHA256为`cae19bbf01d126b6ec317861eeae2b9bd4ab268ac46246fb6d51137d696d4b18`。逐个解析实际GUI定义：

- `prescripted_empire_design_entry`（name行318）在行339有`containerWindowType portrait_container`。
- `user_empire_design_entry`（name行408）在行464有同名container。
- `user_empire_design_entry_narrow`（name行501）没有该container；它在行556直接定义`iconType portrait`。

封存日志恰好要求第三个条目中不存在的`containerWindowType portrait_container`，因此有直接的原版结构证据，而非仅靠历史重复。RC6包无任何`.gui`文件，也没有`portrait_container`或`user_empire_design_entry_narrow`文本；唯一interface文件`eep.gfx`只定义GFX_eep_* sprites，没有覆盖上述原版GUI。

这支持“原版GUI窄条目缺少引擎请求子container”的来源分类。没有做无Mod控制或完整头像替代指示器等子功能测试，不能反推任何原版操作都必现、头像UI完全无影响，或一概归为无害。当前范围不改原版GUI，不将此来源调查扩大成新功能修复。

## RC7最终日志和发行说明的使用规则

1. 必须等待RC7正常停止并读取完整封存日志，逐条独立审查。不能按21/1/1的旧数量直接通过。
2. 决议仅在原始日志仍明确采用同一适配器，且本次冻结的键/非EEP分支绑定仍成立时，归入“有意原生单键覆盖”；同键兼容边界保留。
3. portrait仅在文件名、window名、container名精确一致且新包仍不覆盖该GUI时，使用本原版结构解释；UI影响未穷尽的限制保留。
4. Workshop发现仍是环境问题。可列明Steam登记/原生发现/基线对应和单Mod启用边界，不能写“目录不存在”“已证明无害”“零错误日志”。其内部失败条件没有在本轮解决。
5. 新增EEP堆栈、对象/路径/作用域变化或未匹配记录必须独立保留为未解决项；真实while错误不能进入baseline类别。基线另有的nomads本地化错误也不是未来日志的通用豁免。

## 新证据

[独立来源报告](evidence/1020-rc6-nonwhile-source-review-v1/source-review.json)，SHA256 `d20101677bd7797a853ef720ab600a14106a9c9bbb5f0728a91c5d0c8daf5e63`。报告逐条保存23组原文/精确归一比较、来源类别与限制、59文件源绑定、完整Steam ID/当前目录状态、决议token比较和GUI实际子节点；6份新source副本保持原始字节，另复用已封存的baseline VERSION/descriptor源。所有source都有根相对路径和完整SHA。

原始RC6归档的UNKNOWN_IMPACT/UNEXPLAINED状态未被改写；本报告是在独立新文件中增加来源证据与限定。未修改任何代码、包、日志、SAV或Git，未操作桌面/进程。
