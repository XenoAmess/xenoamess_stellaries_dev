# 剩余加算经济与外部特质的最小受控实机设计

## 目标与边界

依据[乘算调查结论](trait-multiplication-investigation-2026-10-15.md)及用户允许的加算回退，设计可由主任务执行的最小受控矩阵：已有真实 rc6 存档、原版引擎、独立测试包中 +40% 岗位产出输入，以及正面/负面/隐藏外部特质输入。证明每新增一个正式特质使岗位产出经济加算增加 0.05；不改变维护、实际劳动力和局势 J；本国非岗位收入及外国岗位不受该架构增益。

**本回合只写设计。** 不新增测试包文件、不改生产、验收工具或运行现场，不启动游戏/GUI，不提交推送。正式 0.2.1 发布结束后，主任务另行实施已设计夹具、对实际组合包先运行 G1，再执行简体中文实机。既有自然维护成功存档只是种子，受控输入不算新的自然完成项目；不恢复已排除的 22 个自然新局或长期路线。

## 种子、已核对字段与先决条件

首选 `run20261015T094102Z/save games/acceptance-fixtures/fb456_natural_claim.sav`，完整运行目录前缀为 `C:/Users/Administrator/AppData/Local/xenoamess_stellaries_dev/runs/20261015T094102Z/`：

- SHA-256 `9ddcb31ce9dab6843758ac2f71e786b43a8242d1cdda4da3cb89e4d5844bbc4d`，日期 2209.11.28，玩家 country=0，n=1，R=0，实际主体人口 5474，同谱系实际模板特质数均为 7，U/T=7、B=0.35；现有只读存档审计无诊断。
- 首都 colony=0，维护员岗位对象 33554621：workforce=100、bonus_workforce=10、automated_workforce=0；原版 biologist 对象 16：workforce=60、bonus_workforce=6、automated_workforce=0。两者都由 pop group 13 供给，不能将一个人口组视为一个岗位。
- 两类岗位同属 `planet_biologists`。源当前预算中该类别社会学 8.90192、凝聚力 1.85456、消费品支出 1.98；这些是源档缓存锚点，不是新夹具分支的目标输出。
- `country_base` 源当前收入包括能量 25、矿物 25、三系科研各 12.5、影响力 3.75 等，可用作已有非岗位阳性来源的阴性对照。不要用库存净变化代替毛收入。

备选 `fb456_floor_j500.sav`，SHA-256 `1f254e6090af681e3c5bf399f46456bfb38a2301843379b2f844ca3c07492cc5`、2210.02.22；U/T 同为 7、B=0.35。只读审计发现实际人口 5492，而统计缓存人口 5486、分子 38402（实际 38444）；现有审计因此报告人口/分子不匹配，不能把整个源审计登记 PASS。比例 U 恰好仍为 7。若选此源，起点调用生产 refresh 再审计；归一化仍只用原生实际人口/岗位字段，不能用旧缓存人口作分母。首选一所研究所分支较简单。

共同基线 S 必须暂停，确认无 pending 奖励、无正在完成的维护/优化项目，R/n 不会因其它链变化；没有科研 boost、资源注入或建造加速。先完成外国哨兵设置（若需要），等待一次完整预算刷新，保存所有分支共用的 S。既有源的局势 I 在短期内不会跨阶段，但每份样本仍检查阶段不变、无短缺、新科技、政策、传统、官员/政府或殖民地修正变化。不能通过归一化掩盖这些变更。

## 月脉冲自动刷新：用等效关闭，避免覆盖生产

直接 `remove_modifier=shishan_code_architecture_jobs` 后跨月不可靠：生产 `.60` 会重新调用架构 refresh，重新添加 B。测试 on_action 在它之前还是之后执行也没有本轮证据，禁止依赖文件顺序碰运气。

本方案新增测试包专用**反向控制修正** `planet_jobs_produces_mult=-0.05`，一次按当前真实 T 添加 multiplier=T。这样仍保留、执行完整生产 refresh；月脉冲重新添加 +0.05T 时，持久反向实例仍在，两者在同一原生修正键内抵消。这里的 OFF 是「架构增幅的等效数值关闭」，不是删除起源或关闭生产脚本，报告必须明确。

只在每个分支测量前设置一次反向实例，不接月脉冲、不自动修正它。记录设置时实际 T；测量每个快照须独立从实际模板/人口重算 T，核对生产实例 multiplier、反向实例 multiplier 均等于它。测试固定单模板或所有主体模板同特质数，R=0；正常人口增长不改变 U/T。若 T 漂移或 counter multiplier 失配，该 OFF 样本无效，回共同基线重新准备，不能悄悄调 counter 或直接写 U/T/B 让结果符合。

额外 +40% 修正只含 `planet_jobs_produces_mult=0.40`，作用于测试国家。两种测试修正都不包含 upkeep、workforce、资源补发或人口字段。原生语法依据为最新 `effects.log:480–488` 的 `add_modifier`、动态 multiplier、永久 days=-1；生产本身正使用同型调用。源 T=7，抵消量 -0.35，不触及 -90% 的负倍率边界；T=8 的单特质案例同样不触及。

测试包拟新增两个静态修正，以下只是设计草案：

```text
shishan_econ_probe_other_output = { planet_jobs_produces_mult = 0.40 }
shishan_econ_probe_counter = { planet_jobs_produces_mult = -0.05 }
```

事件入口拟为隐藏、仅触发的 `shishan_econ_probe.10`（OFF）、`.11`（ON）、`.20`（A40）、`.21`（A0）。每个 immediate 再检查本起源、无 pending、真实正人口；初次刷新由生产计算，不写任何预期统计。OFF 的核心为：

```text
# Country scope; inside the guarded hidden fixture event.
shishan_code_architecture_refresh_effect = yes
remove_modifier = shishan_econ_probe_counter
add_modifier = {
    modifier = shishan_econ_probe_counter
    days = -1
    multiplier = this.shishan_code_architecture_total
}
```

ON 只移除 counter 并调用生产 refresh；A40 先移除旧同名输入实例再添加一个 multiplier=1 的永久 other_output；A0 只移除 other_output。可以存一项 `probe_counter_t` 作为「本次实际控制输入」审计值，但不能将它当独立数学 oracle。没有合格对象/重放条件不满足时只输出 BLOCKED marker，不强行建立结果。

## 外部特质输入：仅添加正式注册键，不附经济效果

测试包独立注册三个不在生产特质清单中的键，分别 cost=1/tags positive、cost=-1/tags negative、cost=0/hidden=yes。三者都不声明 modifier、resources、岗位效率或维护效果，避免把特质自带的经济变化混入架构增幅。示例：

```text
trait_external_econ_probe_positive = {
    cost = 1
    category = robotic
    allowed_archetypes = { ROBOT MACHINE }
    tags = { machine positive }
    initial = no
    randomized = no
    icon = "gfx/interface/icons/traits/trait_shishan_refactored.dds"
}
```

负面键使用 cost=-1、tags={machine negative}；隐藏键使用 cost=0、tags={machine}、hidden=yes；都复用现有 Mod 图标。测试本地化按组合包键集契约补齐十语言，九种外语只静态、不启动游戏。`hidden=yes` 的原版依据为 `common/traits/000_documentation_species_traits.txt:25–26`，它隐藏模板改造窗口中的特质，不意味正式键不计数。`allowed_archetypes` 与 cost 字段同见该文档；当前原版也有隐藏的 `trait_adaptive_minerals`。后续实施时检查测试本地化与 G1，不把无标签/原始 key 泄漏当作隐藏特质的正常表现。

拟用 `.30/.31/.32` 分别添加一个正/负/隐藏键。每次从 S 单独分支，以当前国家保存 `shishan_code_reward_country`，遍历实际正人口主谱系组，外层 limit 与执行前 if 重新检查目标特质尚不存在，进入其 species 调用现有 `shishan_code_modify_domestic_template_effect={ADD_TRAIT=实际键}`，再调用生产 refresh。复用的生产 clone helper 只迁移国内精确旧模板，避免直接修改共享 species 定义和外国哨兵；不使用 `every_owned_species` 缓存。此输入不是奖励池选择，不增加 n/R/CD、不发成功凭证。

三种键的共同效果草案（正面示例，其它两项只替换字面 trait key）：

```text
save_event_target_as = shishan_code_reward_country
every_owned_pop_group = {
    limit = {
        is_same_species = prev
        pop_group_size > 0
        species = { NOT = { has_trait = trait_external_econ_probe_positive } }
    }
    if = {
        limit = {
            is_same_species = prev
            pop_group_size > 0
            species = { NOT = { has_trait = trait_external_econ_probe_positive } }
        }
        species = {
            shishan_code_modify_domestic_template_effect = {
                ADD_TRAIT = trait_external_econ_probe_positive
            }
        }
    }
}
shishan_code_architecture_refresh_effect = yes
```

三种单键输入均应由实际存档重算 U=8、R=0、T=8、B=0.40；全主谱系添加一个键，不能只给 20% 人口添加后仍期待 U+1。无人口、非起源、重复输入不应再新增模板或层数。该夹具验证外部注册正式键、cost 正负与 hidden 属性的通用计数，不冒充某个已发布第三方 Mod 的整包兼容；也不证明有害特质的原经济负效果被保留，后者另按已有真实特质用例处理。

## 最小执行矩阵：同一共同基线的七个分支

| 分支 | +40% 输入 A | counter | 外部特质 | 期望生产 B（只读核对，不写入） |
| --- | --- | --- | --- | --- |
| F00 | 无 | 有，T=7 | 无 | +0.35，净架构控制为 0 |
| F10 | 有 | 有，T=7 | 无 | +0.35，净架构控制为 0 |
| F01 | 无 | 无 | 无 | +0.35 |
| F11 | 有 | 无 | 无 | +0.35 |
| FP | 有 | 无 | 正面一键 | +0.40 |
| FN | 有 | 无 | 负面一键 | +0.40 |
| FH | 有 | 无 | 隐藏一键 | +0.40 |

每个分支重载 S，在暂停日期设置相应输入并保存 setup；不串行沿上一分支继续。经过一次完整月结让缓存刷新，保存 warm 快照；再经过完整一个月，在同一日暂停保存 measured。三个特质分支沿同样日历运行，不能用不同完工日期或不同阶段的样本互相比值。测量期间不取消项目冒充完成，不直接修改资源输出、统计值或原生存档。

以 measured 的 `budget.last_month` 为已完整经历控制输入的收入/支出期间，原生岗位量需在该期间起止两快照保持稳定；同时记录 current_month 作缓存交叉核对。若第一暖月与 measured 仍显示不同状态，要明确预算时间对应关系并延长一个稳定窗口；若期间就业、额外产出、短缺或政策变化无法排除，样本 FAIL/INVALID 并保留证据，不能挑看似符合的一列。允许正常人口增长，但必须确认它没有改变被测岗位、特质平均数或产出修正。

## 原生数据读取与劳动力归一化

读取 `country[actor].budget.{last_month,current_month}.income/expenses` 的**分类毛额**，不把 balance 再相加。岗位从顶层 `pop_jobs` 解析 type/planet/workforce/bonus_workforce/automated_workforce/pop_groups；归属经 `colony -> carrier -> physical planet.owner`，不得把 colony=0 当恒星 planet=0。用人口组 size、key.species、species_db 的实际 traits 和谱系重算 U，不能用 owned_species_refs 或 UI 图标数。组 ID 可能因克隆/合并变化，按 species、类别、分配量与实际归属核对，不强求 ID 不变。

**J 与产出分母不同：** J 只合计两类维护员实际 workforce，当前应保持 100；产出归一化还须记录 bonus_workforce。本最小种子自动劳动力为 0，要求全程保持 0，于是有效资源工作量 `W_eff=workforce+bonus_workforce`。出现自动劳动力时先扩充其资源成本/产出证据再使用，不能凭字段名猜它是否已包含在 workforce 内。

优先测 `income.planet_biologists.unity`：先核实其它该类别岗位没有额外凝聚力资源表或 `_add`。满足时唯一来源为维护员，每 100 有效工作量的基础凝聚力 q=1；初始 W_eff=110。定义归一化产出 `y=该分类凝聚力收入/(W_eff/100)`，应满足：

- `y10-y00=0.40`，`y11-y01=0.40`，确认额外输入本身是同一个 +40% 经济通道。
- `y01-y00=0.35`，`y11-y10=0.35`，确认架构 +35% 加算不被 A=40% 再乘大。
- 交互差分 `D=(y11-y10)-(y01-y00)=0`，结合固定基值下上述绝对增量，验证当前同键 +40% 与架构系数属于加算。本 counter 专为当前同键实现构造，不能拿它充当任意未知最终乘算实现的真正开关；若未来改成其它最终层，需重新设计 OFF 控制，不能沿用本四格宣称否定所有乘算方式。
- `yP-y11=yN-y11=yH-y11=0.05`。在 W_eff=110 固定时，实际凝聚力差分别为 0.055，但这只是由真实分母推导的期望，不写入游戏。

若同类别还存在其它凝聚力追加来源，不能把分类总额只除维护员 J；应选择可独立识别的其它资源，或逐个岗位/资源表建实际基值加权分母。社会学可作为第二资源：当前原版 biologist 基础为 3，维护员基础也为 3，若没有 zookeeper 条件追加或其它 `_add`，其合并 W_eff 为 66+110=176，每 100 工作量 q=3；每特质带来的分类收入差预期为 `3*1.76*0.05=0.264`。先审计实际条件，再使用该数值，不能将社会学类别毛额只除 J=100。

固定误差规则在执行前登记：原生资源字段常保留五位小数，归一化差分使用 `epsilon=max(0.0001,0.000001*最大被比较绝对值)`，同时保留原始 Decimal 数据；不能在见到失败后放宽。若资源来自多种异质表或未知基值修正，使用四分支的 +40% 差分推导 q，或将该资源判为暂不能隔离，不伪造基值。

## 维护、就业、非岗位与外国阴性对照

1. 维护从 `expenses.planet_biologists.consumer_goods` 合计维护员与原版 biologist 两者，并按相应总有效工作量归一化；不能只用维护员分母。源工作量 1.76、I 阶段岗位维护修正 -25%，单个基础消费品投入 1.5，对应源 1.98，仅作为初始算术交叉核对。最小夹具无特质自身经济效果，故 F00/F01、F10/F11 与 FP/FN/FH 相比的维护系数应相同；其它实际存在的岗位维护资源也逐项检查。库存净消费不是岗位维护 oracle。
2. 每份快照维护员实际 J=100、岗位容量/限制、bonus_workforce、自动劳动力及其人口组分配均保持；n=1 时局势月速仍为 1。A40 或 dummy trait 导致原生重新分配而无法保持时，应报告该状态影响，经济样本不通过，不能只用人口增长解释掉。
3. 以相同阶段下真实非零的 `income.country_base` 能量/矿物/三系科研/凝聚力等行做阴性对照；应不随 A40/架构开关或 dummy trait 改变。现存且可固定来源的 station/building/deposit 分类另作对照；某来源在本种子为零或不存在时记录 NOT COVERED，零等于零不能算该来源验收通过。
4. 需要外国对照时，先于 S 使用既有 `.1` 哨兵，或选已共享旧主模板且有真实岗位的固定外国国家，记录其 country ID、主/实际物种、岗位量、分类毛收入和 modifiers。只给本国输入 A/counter/traits；原始共享 species 定义和外国模板保持，外国不得出现架构/测试修正。四个无 clone 的 F 分支相同日历内，外国相同岗位与修正下归一化收入应相同。AI 建设、权利、战争、岗位或修正发生变化则该外国经济比值不能作阴性证明，保留其结构隔离结果并另选稳定窗口；不能给外国写固定收入或停用其经济来伪造无影响。
5. 国内存在非主体谱系岗位时也应获得国家架构加成；它们不进入 U 分母，不等于被排除收益。此单模板种子若没有这类人口，该覆盖是 NOT COVERED，另用已有 mixed 种子，不把本最小矩阵扩成新局或假填该项。

## 实施门禁、恢复与可交付结果

后续实施只在 `testing/mod/` 新增事件、三 traits、两 static modifiers、所需测试本地化；独立复制正式生产包后叠加，记录生产 90 文件逐字节相同、额外夹具清单和 G1 报告。夹具不改生产 helper、on_action、预期统计或存档文件；所有事件 immediate 均有前提守卫与可观察 BLOCKED marker。G1 未通过则暂停实机；工具缺陷先按仓库规则修工具，不绕过门禁。

所有分支以原生另存、SHA、实际参数、时间线、完整 error/game 日志和必要简中岗位/UI 提示归档。只读审计产出每项 MATCH/MISMATCH/INVALID/NOT COVERED，保留 native 字段和推导式。每个分支重载 S，自然消除前支 counter/A/dummy traits；夹具从未进入生产包或 Workshop，最终回到无夹具正式包并核对生产字节。

本设计不能自动覆盖所有 22 资源、其它政体、全部 `_add` 组合或真实第三方整包。它能用最少七个同源短分支检验核心加算交互、三种外部键计数与增量、已有维护/J及可取得的阴性来源；其它矩阵由对应剩余用例继续，不把本次草案登记实机 PASS。

## 后续实施授权与具体门禁（实施前记录）

主任务已审阅并授权实施本设计，前文「本回合只写设计」为最初设计阶段的边界。当前只新增 `testing/mod/` 的一个 lab events 文件、一个包含三 traits 的文件、一个包含两 static modifiers 的文件与十语言测试本地化，追加 testing README；复用原有 foreign_probe，正式 90 文件不变。构建新的 `_runtime/shishan_code/20261015-remaining/additive-fixture/mod`，保留正式 0.2.1 descriptor 身份，记录逐文件生产/夹具清单和哈希，再按 `C:/workspace/open_kaishek` 当前说明执行组合包 G1。

本机原生 `triggers.log:443–445` 支持国家 `is_researching_special_project`，事件守卫可据此拒绝进行中的维护/清理/优化；同时拒绝 pending 和未消费成功凭证。OFF 拒绝已存在 counter 的重放，避免自动校准或改写失配 counter；ON/A0 只有存在对应输入时才移除，A40 拒绝重复叠加。三个 trait 入口拒绝已有任一 lab trait、存在 counter、非机械主谱系及零实际主谱系人口；各自克隆前重检、克隆后检查所有实际主谱系组具有目标键，再记录 READY，否则记录 BLOCKED_POSTCONDITION。不伪写预期 U/R/B/收入。

这是开发和静态门禁授权，不包含由本代理启动游戏、操作屏幕或提交推送。若 G1 发现工具缺陷，按仓库规则暂停并向主任务报告，不绕过；本轮实机仍由主任务独占。

## 已实施与 G1 结果

新增 lab events/traits/static modifiers 三个 P 文件及十语本地化共 13 文件，原 foreign_probe 一文件保持。组合包实际为 90 个生产文件加 14 个额外文件，共 104 文件；正式 descriptor 与独立 VERSION 副本都是 0.2.1。拷贝前后、G1 后都逐一核对原生产 90 文件 SHA-256，一致；没有覆盖生产资源或改 on_action。新增文件完整清单与每文件哈希见[开发及复制合同报告](evidence/feedback-redesign/remaining-2026-10-15/additive-static/additive-fixture-development-contract.json)，其 SHA-256 为 `aaf0fc8fdad5cc86ded92ee875cf059b5fbf099298080efb858d5faf82d0c442`。

只读开发结构检查通过：7 个事件 ID 唯一，隐藏且仅触发，immediate 有 origin/正人口/pending/成功票据/在研项目守卫；3 个 trait 真实字段及无固有效果；2 个纯产出静态修正；生产克隆前重复 guard、国内精确模板 helper 和 postcondition 保留。三项有意义的静态负例确定拒绝「删除克隆前内层 guard」「删除 hidden 属性」「删除 pending/凭证守卫」。静态检查不执行 Stellaris，不当作事件运行通过。

完整组合包 G1 **PASS，退出 0：29/29 P 脚本、13 DDS、279 本地化键/语**，报告为 [additive-fixture-open-kaishek.json](evidence/feedback-redesign/remaining-2026-10-15/additive-static/additive-fixture-open-kaishek.json)，SHA-256 `16cc1c5fd696e4c92d7a6561ecebce9093dfc6366f4eb44110e87b8c9b642c13`。工具仓库 HEAD=`2b559966c72f4e845111e3e15652ae2354aaed57`，实际 CLI JAR SHA-256=`6ac143ebf03f3e1a041dff01b2d808e60de8e289d18cebf9855682f0a80b6d82`。按已核实 4.5.2 EXE SHA=`400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83` 执行：

```powershell
python -B tools/accept_stellaris_mod.py `
  --mod C:/workspace/xenoamess_stellaries_dev/_runtime/shishan_code/20261015-remaining/additive-fixture/mod `
  --version-file C:/workspace/xenoamess_stellaries_dev/_runtime/shishan_code/20261015-remaining/additive-fixture/VERSION `
  --game 'C:/Program Files (x86)/Steam/steamapps/common/Stellaris' `
  --expected-exe-sha256 400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83 `
  --report C:/workspace/xenoamess_stellaries_dev/_runtime/shishan_code/20261015-remaining/additive-fixture-open-kaishek.json
```

工作目录为 `C:/workspace/open_kaishek`。检查范围按报告为语法/包级及已注册有限人口作用域、脚本值结构；不认证所有 opcode、克隆实际效果或原生经济。另运行既有完整本地化静态检查：60 文件、每语 279 键、2080 引用及原版引用解析通过；九种外语为**静态校验通过，运行时不在范围内**。

所有实验事件实际执行、原生经济、成本/J、外部键与隐藏计数、外国对照仍为 **NOT RUN**；后续由主任务独占 GUI，按本设计同源七分支逐项取证。本轮没有修改正式包或工具，没有启动游戏、GUI、Steam，也没有提交推送。

## 只读矩阵审计器实施设计（先行）

主任务授权新增 `tools/audit_additive_runtime_matrix.py` 与独立负例测试；不改已封口的 14 文件夹具、生产或验收工具。复用 `audit_feedback_runtime_save.py` 的原生 ZIP 数据解析器与谱系/计数逻辑，逐份读取 input/warm/measured，提取数值、归属、工作量、预算和身份小快照后释放整个 gamestate/Document，不同时保留 21 份完整存档对象。输出必须含每份原生路径、SHA、日期与严格计数缓存检查，不能将人工期望写进存档或当观察值。

manifest 的固定七分支为 `F00/F10/F01/F11/FP/FN/FH`，每支映射 `{input,warm,measured}` 的原生 `.sav` 路径，相对路径以 manifest 父目录解析。缺 manifest、缺任何快照或未提供实际数据则报告 **NOT RUN**，不拿开发夹具或其它源档补位。输入无法明确解释或期间/就业/版本不稳定则 **INVALID**；资源来源不能分离或缺来源则 **NOT COVERED**。这些状态不能被兜底的零或常数隐藏。

凝聚力主合同以 `budget.last_month.income.planet_biologists.unity` 除实际维护员 `(workforce+bonus_workforce)/100`，并明确仅适用于已登记的有限岗位/来源范围。四格先由实际 `Q0=(y10-y00)/0.4`、`Q1=(y11-y01)/0.4` 推导响应系数；要求正且彼此吻合，然后核对两组架构 ON-OFF 都为 `0.35Q`，三类外部键相对 F11 都为 `0.05Q`。不硬编码凝聚力差 0.44/0.055，也不预设其它产出分区、岗位或国家渠道都与它加算；Q 包括本样本中未变化的公因子。社会学采用原版生物学家与维护员合并工作量的独立次级差分，不用 J=100 作整个类别的分母；不能明确其额外输出表时保留 NOT COVERED。

所有快照独立要求基线实际 U=7、三个单键分支实际 U=8、R=0、n=1、相应唯一 modifier/counter/input 状态正确、counter multiplier=T。主谱系每模板都具有正确的 dummy 键集，不能只看 U 恰好等于整数；岗位 J=100、容量、限制、bonus 和自动量按有限源档范围审计，期间和跨分支匹配。预算实际完整月份及各分支共同日历必须能成立；科研进度可变，已完成科技、政策、阶段、稳定度等会影响经济的状态变化则标明无效或来源未隔离。

严格人口 P/分子 W 缓存不匹配单列 **FAIL** 并保留原诊断，不能抹成一致；若实际与缓存 U/T/B 及 R 均稳定正确，P/W 的月内增长滞后不阻断有明确范围的经济差分。报告分别给 `strict_cache_audit` 与 `limited_economy`，最终不把有限经济 PASS 写成全部严格审计 PASS。维护使用同类别各供给岗位合并工作量；country_base 以真实非零来源作阴性，缺失或零来源不给 PASS。外国没有可用稳定岗位来源时保留 NOT COVERED，不将国内证据替代外国证据。

数值 epsilon 保持前述 `max(0.0001,0.000001*比较绝对值)`；测试至少覆盖非 1 的 Q 正例、独乘交互负例、错误 counter、漏 trait/R 变化、就业/期间变化、缺来源、P/W 严格 FAIL 而有限差分独立成立、缺快照 NOT RUN 及逐档释放。测试替身明确为审计器开发输入，不当作实机结果；实际原生输入由主任务后续提供。

源表范围进一步限定为本个体机械种子的已读七键：`trait_machine_unit`、`trait_shishan_code`、`trait_robot_luxurious`、`trait_robot_high_bandwidth`、`trait_robot_high_maintenance`、`trait_wet_planet_preference`、`trait_robot_power_drills`。参与该类别岗位的实际分配组去除本次唯一 dummy 后必须仍为这些键；其它输入或其它实际 `planet_biologists` 岗位不能沿用此凝聚力来源证明，标 NOT COVERED。来源路径与哈希由 manifest 声明的游戏目录及冻结组合包读取，并保留「声明的隔离包源表，未自动求解所有原版动态资源追加」边界，不把当前文件等同于存档历史的字节证明。

## 只读矩阵审计器已实施，原生矩阵尚未运行

已新增[审计器](../../tools/audit_additive_runtime_matrix.py)及[独立开发测试](../../tests/test_additive_runtime_matrix.py)。没有修改正式包、14 文件冻结经济夹具、既有 native parser 或 open_kaishek。`extract_snapshot` 顺序读取单份 ZIP：哈希按块读取，gamestate 使用原有浅层解析器；返回 compact 数值/身份/预算后不保留 Document、Block 或完整文本。21 次载入的弱引用测试不调用强制 GC，确认下一次读取前上份两个 Document（meta/gamestate）均已释放。

调用路径如下，相对路径以仓库根工作目录为准：

```powershell
python -B tools/audit_additive_runtime_matrix.py `
  --manifest _runtime/shishan_code/20261015-remaining/additive-matrix-manifest.json `
  --report _runtime/shishan_code/20261015-remaining/additive-matrix-native.json
```

完整[manifest 模板](evidence/feedback-redesign/remaining-2026-10-15/additive-static/additive-matrix-manifest-template.json)包含七支和 `input/warm/measured` 三键，路径目前为 `null`。填入真实原生 `.sav` 路径后另存为命令中的 manifest；绝对路径可用，相对路径相对 manifest 所在目录。`sources.game_root` 指向本机 4.5.2 游戏，`sources.mod_root` 指向冻结的 `additive-fixture/mod`。源表审计记录岗位脚本与实际 researcher_output inline 的哈希，检查维护员直接资源表及生物学家不产凝聚力，枚举其它同类别岗位；出现未知源表、额外实际同类别岗位、未审阅特质组合或非单 Mod 加载集合时标 NOT COVERED。

每份 input 也核对实际控制输入、U/R/T、modifier 倍率及真实 J。三个阶段的就业/容量/限制/分配/bonus/自动量须不变；克隆合并导致 ID 变化时，按类别、基础特质键集和分配量合计，不将人口组 ID 当经济身份。各支 input 经济环境须相同，允许共同暖机阶段在正式测量前稳定；warm 与 measured 经济环境必须一致。读取阶段/政策/已完成科技、稳定度、建筑缓存、其它国家修正、领袖等级/特质/职位及耗尽资源状态等观察字段，变化报告 INVALID，保留算术结果但不给验收 PASS。此端点检查不能证明每一中间 tick 从未有过变化，也不自动解释所有原版触发修正，运行日志及来源审阅仍须归档。

日历要求各支的三个日期分别相同，input 早于 warm 且处于前一个或更早月份；warm/measured 为相邻月同一日，日须在每月 1–3 日。测量用 measured.last_month，warm/measured 因此围住同一个完整 30 日窗口。测量端点有 0–30 天内过期国家 modifier 时保守标 INVALID；有 active 特殊项目亦无效，不能在维护/科研完工跨状态时取样。原生源 `fb456_natural_claim` 存有 game_start 剩余 33 天，直接照两个月路线会进入到期窗口；主任务应先取得其消失且来源稳定的共同基线，不能忽略该原生事实。

初版执行开发测试 **23 项 PASS**（后续边界/门禁修订另记）：

```powershell
python -B -m unittest discover -s tests -p test_additive_runtime_matrix.py -v
```

正例使用 Q=1.23、社会学响应 Q=3.69，明确不依赖草案的 0.44/0.055；另有独乘交互、counter 倍率、漏隐藏键、R/T、就业/容量/期间/稳定度、维护/非岗位变动、缺来源、未审阅特质/岗位、自动量、epsilon、组拆分/合并、错误 manifest、缺快照及逐档释放负例。开发 ZIP 和 compact snapshot 均明确为替身，不计入实机验收。只读提取器对既有真实 `fb456_natural_claim` 与 `fb456_floor_j500` 做了读取冒烟：两者实际 U 均为 7，前者严格缓存 PASS，后者严格 P/W 缓存 FAIL 被原样保留；没有将它们拼成七支实验。[读取报告](evidence/feedback-redesign/remaining-2026-10-15/additive-static/additive-matrix-reader-smoke.json) SHA-256=`8c92b1baeb8f9674fd0853a7b5ea908084cd3b72124341596399624c220f1008`。

实际执行当前空模板得到 [pending 报告](evidence/feedback-redesign/remaining-2026-10-15/additive-static/additive-matrix-pending.json)：**NOT RUN**，列明 21 个缺快照，CLI 退出 2；任何非 PASS 同样退出 2，供自动化不误吞失败。实机矩阵的经济差分、三类外部键原生效果、维护/J/非岗位阴性仍为 **NOT RUN**。外国经济与 station/deposit/building 阴性未纳入此有限工具时分别为 **NOT COVERED**，不会用国内 country_base 替代。严格 P/W 审计与有限经济状态独立，报告顶层可能因严格缓存 FAIL 而 FAIL，同时有限经济 PASS；引用结果时必须同时交代两者。

## 静态证据归档方案（先行）

主任务要求将上述经济夹具 G1、开发及静态本地化合同、manifest 模板、pending、reader-smoke 与 23 项开发测试记录复制到本 Mod 文档的 `evidence/feedback-redesign/remaining-2026-10-15/additive-static/`。复制前后逐文件比较 SHA-256 和大小，保留原文件字节，建立来源/归档/哈希清单；生成开发测试结果时保存实际执行日志及工具/测试/native parser 源码哈希，不将替身测试列为原生经济运行。

不复制完整 104 文件组合包，夹具源码仍在 testing，生产身份和 90 文件完整哈希由原合同报告证明。只修本文指向临时报告的 Markdown 链接为已归档的仓库相对路径，历史命令中的 runtime 执行路径保留；不改源报告内历史绝对路径或哈希。此归档不会改变 NOT RUN/NOT COVERED 边界，也不接触 balance 管理的 formal 证据目录。

归档已完成，六份来源报告全部逐字节相同；[清单](evidence/feedback-redesign/remaining-2026-10-15/additive-static/evidence-files.json) SHA-256=`4875785b4f2c4c173881b2ed424d71589a5a708feafebd544cfceb0ec3987e52`，记录原路径、复制前后源 SHA、归档 SHA、大小及相等结果。原开发合同、G1 与 reader-smoke 哈希均保持本文登记值；新[23 项测试日志报告](evidence/feedback-redesign/remaining-2026-10-15/additive-static/additive-matrix-development-tests.json) SHA-256=`116e629670a906a6a5547de6e349228b0ee39074d60b41198a90b63828ff214d`。本文五处原临时报告链接均已替换为真实仓库文档相对路径，[归档索引](evidence/feedback-redesign/remaining-2026-10-15/additive-static/README.md)说明每份证据的边界。没有复制游戏存档、完整组合包或任何 GUI 操作；矩阵仍为 NOT RUN。

## 原生共同基线预检范围

主任务在冻结 104 文件包 run112046Z 使用原生 fast_forward 64 日并经简中 Save UI 保存 `econ104_common_0202.sav`，要求独立只读核验其 `2210.02.02` 状态。复用封口的 extract_snapshot，检查 game_start 是否消失、U7/R0/T7/B.35/n1/真实 J100、bonus/容量/稳定度/科技和潜在两月窗口干扰，另保留队列与领袖原生数据。报告写入本 run；只证明共同基线当前状态，不预言未来两月一定稳定，也不修改审计规则、生产、夹具或 GUI。七分支仍需未来 input/warm/measured 实际证据。

预检已确认 game_start 消失、无其它 60 天内到期国家修正，U7/R0/T7/B.35/n1、维护员100+bonus10、biologist60+bonus6、两者自动量0；没有分支控制输入或 active 项目。实际 P5491/W38437，缓存 P5485/W38395，严格 FAIL 单列。当前稳定度72.6918，对原源72.672已经上升0.0198，不能预言未来月窗不漂移。科技完成名单不变，在研社会学 progress589.63109；领袖等级/traits 当前未变。就业全表随普通人口增长可能变化，不能从布尔不等反推架构改了岗位。原生基线只读报告位于 run112046Z 的 `independent-econ104-common-baseline-precheck.json`；其后追加来源对照，最终 SHA=`f78ea2d20eafc986093be32a225d789df8dc38d16233de45c028557c243e7c43`。

## v2 独立稳定环境夹具设计（实施先行）

保留原运行中 104 文件包及自然 F01 三档，原审计规则得到的 INVALID/FAIL 报告也保留。另建 `additive-stable-fixture/mod`：逐字节复制已冻结104文件，只叠一个独立事件文件、一个独立 static modifier 文件与十语独立本地化文件，共新增12文件；不从后来加了其它夹具的 testing 全量覆盖，不改生产90文件或原14文件。测试身份仍为正式0.2.1，禁止把此包发布Workshop。

新增隐藏触发事件 `shishan_econ_probe.40`，要求本起源/default country、有实际主谱系人口、首都存在且归本国、无在研维护/清理/优化、无待领/成功票据/复发凭证；首次只给真实 `capital_scope` 添加永久测试 modifier `shishan_econ_probe_stability_control`，其唯一数学项为 `planet_stability_add=100`。重复输入以 has_modifier 拒绝并记 BLOCKED，成功有 READY；不写预算、U/R/T/B/J、预期输出、资源库存或领袖。全部七支先从同一个已加控制的共同基线分出，避免给不同支使用不同稳定度输入。

本机4.5.2原生依据：`common/defines/00_defines.txt:654` 为 `MAX_PLANET_STABILITY=100`；同文件655另有额外上限规则，故不能把读取常量等同于任意环境实际100。run094102Z生成 `modifiers.log:152` 将 `planet_stability_add` 列为 Colony，`scopes.log:82–84` 明示 country 的 capital_scope 输出 colony，`effects.log:480`起说明 add_modifier 可施加到 scoped object、永久days=-1，其支持列表含 colony；原版 static modifier 实际使用该数值项。G1核对同一EXE SHA及完整新包语法/本地化/有限scope；工具不证明实际clamp。只有主任务实机保存显示 capital实际stability=100、唯一正确modifier、三档/七支窗口稳定且无非预期就业/经济状态变化后，才能登记控制有效。未取得这些档前为 NOT RUN。

验收包括：原104/正式90逐文件哈希保持；新事件只能操作资本殖民地，含重复输入和所有前提守卫；static modifier不得夹带岗位产出或维护项；10语BOM/header/键一致且无简中占位；删除modifier重复守卫、将capital_scope错误换为country/无关scope、夹带产出数学项的开发负例应拒绝。新包先完整G1，工具缺陷则暂停而非绕过。成功后主任务换包并实际运行 `.40`，保存控制共同源，再重新七分支；本代理不GUI。

v2 已按此设计实施并封口：新包116文件，原104及其正式90的逐文件哈希全部保持；完整G1退出0，**31/31 P、13 DDS、280键/语、有限人口scope预检230处零诊断**。7项结构/负例开发测试 PASS，包含改错施加scope、移除重复/pending守卫、夹带产出/维护项、直接变量写入及十语文件验证；这些不执行Stellaris。在静态报告生成时，原生资本稳定度100、控制实例唯一性与七支矩阵均为 NOT RUN，后续原生结果另记，不改历史报告。原生依据及EXE/tool/hash、G1、复制合同和测试日志以[四报告索引](evidence/feedback-redesign/remaining-2026-10-15/additive-static/v2-stability-control/README.md)原字节归档，源报告保持在 runtime；没有修改运行中的104包。[清单](evidence/feedback-redesign/remaining-2026-10-15/additive-static/v2-stability-control/evidence-files.json) SHA=`d8f316de083f43d5b933ffb2ecbe57c4cf28a7eb35b8ea4b56d754852923bb1f`；G1报告 SHA=`be2f0167eaa86656c20fd74e1b6abd413ca3008c20fb54bac4e87dbe262949b7`。

## 就业审计边界修订设计（先行）

主任务复核指出，初版工具将每份 input/warm/measured 的全部国内岗位都同 F00 measured 比较，错误地把不参与测量的 civilian 正常人口增长也当作失控；这与本文允许正常人口增长的原设计不一致。先保存自然 F01 三档按原规则计算的完整结果与审计器源码哈希，再修改工具，不改 epsilon 或抹去稳定度漂移 INVALID。

修订后将就业证据拆为三层：实际 `planet_biologists` 分类的各岗位（不仅维护员，包含原版biologist以及任何未知同分类实际岗位）其 workforce/bonus/automation、容量/限制与分配键集在 input→warm→measured 均保持；所有其它国内岗位只要求同 phase、同日期跨分支一致。manifest可额外声明 `common` 原生存档，每支 setup input 的全岗位与该共同源比较，拒绝输入造成的同日非测量岗位变化。未提供共同源时 setup 相对S核验明记 NOT COVERED，不能自动假定已证明；原生输入的同日跨支核对仍照常执行。

共同自然增长只可发生在非测量类别且各分支同日一致；任何被测岗位跨月改变、某支非测量岗位同日异常改变，仍 INVALID。稳定度、已完成科技、领袖等级/traits、阶段、其它经济修正的测量窗口控制不变，未知经济影响仍不得 PASS。测试新增「其它岗位共同自然增长可接受」「同日非测量岗位分支变化INVALID」「被测工作量跨月变化INVALID」，并保存更新后的源码/开发测试哈希，旧23测试报告不覆盖。

此修订已实施，最终工具 SHA=`d6948a5d874b6684912df3e53f69bb3db5e65b925956b5a9068733d0da152787`，测试 SHA=`bd5beb7b10315e62b7ee762eb68ef84ed248a3f9d9d94e8bda2afdf2da7896e2`，共 **32 项 PASS**（原23+8就业/common边界+1 carrier原生ZIP读取）。common与21支快照顺序读取、释放全Document；capital carrier modifier 的 name/multiplier现进入严格环境观察，不把逐日剩余days变化误当经济变化。缺common时setup单列NOT COVERED并影响顶层，有限数学可独立列结果；不擅自补共同源。最终测试报告为 run112046Z `independent-employment-carrier-development-tests.json`，SHA=`6cb339751be1cecb669ad15ab8cb05a6001017249ca48b2f4999b1ef3a8258d4`；新旧源文件、原23、中间31记录均保留，未覆盖。

自然 F01 的原规则结果 `independent-natural-F01-window-audit.json` SHA=`80dd96ca6d7efbff442e2f50c65e72157b2e6a94d4b4a2e5f96efa705198af2e` 保持 INVALID。只有 civilian 正常增长（workforce2390→2396→2402、bonus240.1→240.7→241.3、分配2391→2397→2403），被测 biologist60+6/维护员100+10及容量/限制/自动量不变；不把此无关增长称为架构改就业。修订边界复核 `independent-natural-F01-final-boundary-context-check.json` SHA=`f25519688b36515e69573feb8e1f16ffffd9af5e73527b794411276e2db501ed` 中被测就业 PASS，但稳定度warm72.7026→measured72.714、差0.0114仍超过原epsilon0.0001，故窗口仍 INVALID；strict P/W仍FAIL，完整七支仍NOT RUN。原件由主任务归档自然run证据，不用新规则抹旧报。

## v2 原生共同源首次核验

主任务run113522Z实际执行`.40`得到READY，settle30天，经原生简中SaveUI保存 `econstable_common_0302.sav`，SHA=`88ea13308bc5e4a73667938e22f126bafba666126a2f831df27e04583bb89710`，日期2210.03.02。独立extract_snapshot及carrier原字段读取确认：country capital指向colony0→physical planet8，保存的实际stability=100；carrier只有一个 `shishan_econ_probe_stability_control`，multiplier=1、days=-1，其静态唯一数学项为+100。没有给预算、U/J或期望输出写值。

当前受控基线U7/R0/T7/B.35/n1，维护员100+bonus10、biologist60+bonus6、容量/限制正确且自动量0；没有game_start、60天内到期国家修正或分支counter/A40。全部有限基线守卫PASS。实际P5497/W38479与月内缓存的严格差异仍记FAIL，不挡固定U的有限经济。报告 `run113522Z/independent-econstable-common-precheck.json` SHA=`0d4317a9881670468ce356f9583f6e7def7ebb0a9826198e1681609b009e8011`，状态为 **PASS_CURRENT_CONTROLLED_BASELINE**；这只证明当前control真实有效，F00三档与余下七支实际期间尚待采样，不能先登记整矩阵PASS。

## 独立复核发现的两项审计门禁缺口与修复设计（先行）

programmatic对冻结`d6948a5...`审计器提交了明确开发反例，原输入/输出保存在其独占 `programmatic/additive-matrix-review/development-counterexamples.json`，不代表实际116原生档已经出现这些错误。第一项只把FP measured社会学改为999，社会学分项FAIL却未进入limited_checks，可能顶层PASS；第二项在已登记同分类的额外岗位保持workforce0但bonus100或automation100，active只看workforce>0，错误漏过来源隔离。先保存此版源码和反例，再修工具/负例，不改116包、已有存档、旧原生结果或epsilon。

修复应使来源已隔离的任何被测资源算术FAIL/INVALID都阻断有限经济，而不是仅报告在次级字段里。显式记录社会学来源隔离范围；缺失/未知的次级资源可按NOT COVERED单列，不能称其通过，也不得用未知来源的算术冒充可靠oracle。Unity主合同和维护/非岗位阴性继续必需，社会学不再有独立失败仍总PASS的漏洞。

同分类岗位的实际参与判定检查workforce、bonus_workforce、automated_workforce各通道，任一非零即纳入来源隔离；字段缺失或无法解释时fail-closed报NOT COVERED。不能把0基本workforce当没有产出，更不能只检查已知JOBS的自动量而遗漏其它同分类岗位。至少新增社会学999、额外岗位仅bonus/仅automation、未知通道字段等负例，当前所有审计器与稳定度夹具测试共同执行一次；保存修复前后源码/测试哈希和结果。此前23/32与自然INVALID证据不覆盖，最终原生七支使用修复后的版本。

修复已完成，工具 SHA=`2bee9c8460e07a228d8d0f577aa8245792e2ecc936497c975e6bd422be0173a1`，测试 SHA=`e0bd358fc407cd68639715487fb846a5f073f00df69d51fd43801263d0131132`。当前相关 **43项测试PASS（36工具+7稳定夹具）**，包括新增4组门禁测试及其变体；精确重放programmatic原三组完整输入后，社会学999从原top/limited PASS改为FAIL，额外同分类zero-base+auto100/bonus100从PASS改为NOT COVERED。没有改反例输入或用新规则覆盖旧报告。

来源有限已隔离社会学的FAIL/INVALID现参与有限经济门禁；次级资源缺失或未隔离仍明确NOT COVERED，并保留其原始算术状态，不能当作通过。所有分支/阶段的同分类各工作量通道参与检查，unknown字段不能默认为零。完整开发日志 SHA=`0df7be9f4976205efd05cbd71d58584e5a3b9029811d2a73de9e081de6c1201f`，精确重放报告 SHA=`cd846500b7a682dde4b6830b653496e625d55091b9db4423c7e1c3a9ea699dee`；修复前后源码/测试与报告见[门禁修复证据](evidence/feedback-redesign/remaining-2026-10-15/additive-static/runtime-audit-gate-fix/README.md)。原d694/旧23/32/自然窗口记录保留；116包及已有存档未改。

programmatic随后对原JSON三组输入/profile逐字段不改再次独立重放，与本次repaired_observed完全匹配，并核对修后源码/原反例及测试回执身份；其[修后独立报告](evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-matrix-review/after-fix/independent-after-review.json)仅确认这两类门禁，未重复执行43测试或宣称整个工具/原生矩阵已通过。

## v2 F00 先行窗口结果

主任务run113522Z原生保存F00 input/warm/measured三档，SHA依次为`a0961b09e72d2347b8d7b7db2a53abe01e12e6dbba3e025657f64a053f8ca3b8`、`292e6ea82054b1d62c15485b845e614efa678c4112950102fe6c04679d9d419a`、`19b6253460722e88bb28618ce40a3b8d006c210954322cc7d44c6d38eecd8f09`，日期2210.03.02→04.02→05.02。独立单支必要守卫PASS、无INVALID：稳定度全100、capital永久控制唯一，U7/R0/T7/B.35/n1，counter唯一scale7且无A40；维护员100+10/biologist60+6及容量/limits/auto/分配固定。input全就业相对共同S匹配，warm→measured全部已观察环境零diff，期间完整。

严格P/W仍单列FAIL：warm缓存5497/38479、实际5503/38521；measured缓存5503/38521、实际5509/38563；U固定7未受影响。measured last_month与current的实际社会学8.184、凝聚力1.705、CG维护1.98；warm last_month仍为先前10.032/2.09，current已为新输入8.184/1.705，暖机数据原样保留，不选择较符合期望的一列。独立报告`independent-econstable-F00-window-precheck.json` SHA=`eb370252933d0209952ddbcedca49d9fa5f4c018c3298a7e4eeccae730f4a580`采用冻结d694的只读提取/必要守卫，不调用其两处正修的算术门禁。此结果只支持继续采样其它分支，不替代四格Q或完整七支验收；最终矩阵必须使用修复后版本。

## v2 前三支的真实差异与当前门禁

F00/F10/F01各三档齐备后，用冻结2bee版只读逐档检查，没有构造缺失F11或其它四支。报告`independent-econstable-first-three-branches-precheck.json` SHA=`b381be6f1f5460464120659a4628db6bc00dce249b67dc8523574344b2d4280f`为 **INVALID**：F01其它civilian在同日比F00/F10少1工作量。warm为2401/bonus241.2/分配2402，对照2402/241.3/2403；measured为2407/241.8/2408，对照2408/241.9/2409。所有input相对共同S一致，被测类别、完整context、日期及core均无差异，稳定度100；P/W严格FAIL另列。不能把这项差异径直归因架构改变就业，也不能擅自删除已约定的同日跨支控制门禁。

真实measured凝聚力F00/F10/F01为1.705/2.145/2.09，社会学8.184/10.296/10.032，CG全部1.98、country_base相同；按真实工作量归一后的两边差分别为凝聚力.4/.35、社会学1.2/1.05。这里只记录三个角的观测，F11未提供时不算交互项，不声称四格或完整矩阵PASS。

补充只读原版来源边界：`common/pop_jobs/00_other_jobs.txt`中的civilian资源类别是planet_civilians，主要产trade且享乐分支可产unity，其triggered_planet_modifier还能增加amenities；它与测量的planet_biologists类别分开，但不能由此推断所有间接影响均不存在。本机`02_specialist_jobs.txt:1889`起的roboticist资源表为合金upkeep，`:1931`组装来自`triggered_planet_modifier planet_pop_assembly_add=2`，该处未显式调用job_total_output_modifier。此源码观察不足以认定少1人口/就业的完整原因，不改变原生记录或工具阈值。

## 下一组原生人口控制的调查目标（先行）

既有v2窗口严格INVALID与余下分支原始观测全部保留，继续原门禁及epsilon。主任务在个体机械样本首都的原生中文决议列表见到「停止组装机器人」；本轮只读核实其本机4.5.2精确decision key、适用物种/政体、实际modifier/规则以及是否阻止当前MACHINE/ROBOT新人口，同时检查是否仍有生物自然增长、已有组装进度或队列在停用后完成的路径。不实现新fixture，不改审计工具或旧样本。

先以F00/F01同日actual P与每个国内pop_group的原始size差异区分真实人数变化和岗位重分配，再提出仅使用原生游戏操作的可执行控制。若来源证实该决议可停止唯一增长渠道，主任务可以在同116包加载共同S、正常决议停组装，并成熟两个月另存新共同源；但必须由真实存档确认增长/组装数值零、已有完成队列消退、人口各组/所有岗位与经济环境稳定后再重跑七支。若决议只针对其它archetype或仍有自然增长，明确未隔离，不用猜测规则宣称有效。游戏操作与实际成熟期只由主任务执行。

### 本轮只读调查结果

真实人口差已确认：两支input同为P5497、civilian group1 size2397；warm F00为P5503/group2403、F01为P5502/group2402；measured分别P5509/group2409与P5508/group2408。其它三组始终ruler200/specialist1500/worker1400，均为species48。故少1工作量伴随真实人口组人数少1，不能仅解释为同人数的岗位重分配；这仍不能单凭快照确定差额的全部原因。

本机原版精确入口是`decision_enact_robot_assembly_control`（简中「停止组装机器人」，`common/decisions/01_political_decisions.txt:147–185`），花费250凝聚力，只添加永久`planet_robot_assembly_control`。potential的OR明确允许`is_individual_machine=yes`，不要求该分支通过普通帝国的tech_robotic_workers路线。恢复入口`decision_end_robot_assembly_control`。`08_static_modifiers_megacorp.txt:443–449`该modifier自身仅显示停止tooltip并给`planet_pop_assemblers_upkeep_mult=-0.75`；真正停组装来自`00_rules.txt:1945`起`can_pops_assemble_on_colony`的NOR直接排除此modifier，未区分ROBOT/MACHINE，不能因为静态modifier没有`assembly_mult=-1`就误称它无效。

当前国内实际仅species48、class=MACHINE，`00_species_archetypes.txt:56–65`定义robotic=yes；`species_can_grow_on_colony`（`00_scripted_triggers_pop.txt:189–203`）要求is_robotic=no，bonus自然增长同样先经该条件。因此此样本现有机械人口不具备有机自然增长路径。共同源last_month_growth_data实际记录唯一增长明细`GROWTH_CAT_ASSEMBLY=6`，species_information只含48；没有观察到有机增长项。没有将这种观察推广为永远不会有移民/事件引入新物种。

建议正常操作顺序为：同116包加载S并暂停→首都「决议」点停止组装、支付真实250凝聚力→立即另存控制输入→自然30日、60日各另存。核验carrier同时有唯一永久稳定度控制及原生停止组装modifier，实际stability仍100；两次完整last_month的各来源增长/衰减和各原始population group size均稳定，被测J/bonus/容量/维护及其它环境也稳定，才使用第二成熟档作为新共同S。原生停组装修正会改变assembler维护，不可沿用旧预算当新控制的oracle；全部七支共用新环境即可。`army_build_queue=1`是军队队列指针，不是人口组装队列；当前/上月growth缓存也不是所有引擎内部队列已清空的证明，必须保留成熟期实际观测。未找到116包覆盖这些原版decision/modifier/组装game rule定义。

来源行号/文件哈希、真实组人数对照与共同源增长原字段见run113522Z的`independent-native-population-control-source-plan.json`，SHA=`e18654698122eb087868573938b4e78d5b6a8510eb9ed51cdff8c162d2bc4c15`。此时原生决议效果仍待主任务实际执行确认，未改工具、fixture或旧INVALID数据。

## 稳定度100、仍自然增长的首次完整七支结果

run113522Z首次七支共21份原生档已齐全，使用冻结工具`2bee9c8460e07a228d8d0f577aa8245792e2ecc936497c975e6bd422be0173a1`、真实共同源和实际源表逐份只读提取。FP使用`econstable_FP_attempt2_*`，其余使用标准分支前缀；没有以重复档填补分支。完整报告`additive-stable-growth-native-audit.json`（SHA=`19d63e304dd186abb1d76d782faf0b1aeb8c3b14dea81882207615e6a105e33d`，1543131字节）和派生数值摘要`additive-stable-growth-native-numeric-summary.json`（SHA=`33cea2d81f3b908660d567c707e79c9187f4c7917e87baab59e9fe624a7993b8`）保存在该run，原件不改写。

顶层与有限经济均为 **INVALID**，setup相对共同源为PASS。有限守卫有6项失败：F01、F11、FN在warm和measured各一次同日非被测civilian就业差异。其余四支warm为P5503/civilian workforce2402、bonus241.3、实际分配2403，measured为P5509/2408/241.9/2409；这三支分别为P5502/2401/241.2/2402和P5508/2407/241.8/2408。所有input一致，被测维护员100+10、biologist60+6及容量/分配、稳定度100、期间和已观察经济环境均符合守卫。严格P/W缓存审计另保留32项FAIL，不覆盖有限经济结论。

下表是measured.last_month的真实原生数值；归一分母来自实际workforce与bonus，凝聚力为1.1，社会学合并两种岗位为1.76。这里只报告算术观测，不把失控样本升级为验收PASS。

|分支|实际U|原生凝聚力|归一凝聚力|原生社会学|归一社会学|类别CG维护|
|---|---:|---:|---:|---:|---:|---:|
|F00|7|1.705|1.55|8.184|4.65|1.98|
|F10|7|2.145|1.95|10.296|5.85|1.98|
|F01|7|2.090|1.90|10.032|5.70|1.98|
|F11|7|2.530|2.30|12.144|6.90|1.98|
|FP|8|2.585|2.35|12.408|7.05|1.98|
|FN|8|2.585|2.35|12.408|7.05|1.98|
|FH|8|2.585|2.35|12.408|7.05|1.98|

四格实际推导凝聚力Q0=Q1=1、社会学Q0=Q1=3；A0和A40下架构差值分别均为`.35Q`，交互项为0。正面、负面、隐藏第三方dummy各增加`.05Q`，两资源各7项算术检查PASS；R0、n1、T等于实际U、架构modifier唯一且multiplier=T。维护归一全为1.125，非零country_base各资源不变，其算术检查亦PASS。来源表仅在已登记本样本范围内完成隔离；外国经济与station/deposit/building收入继续NOT COVERED。因civilian人口/就业边界不同，这些算术吻合仍不构成有限经济验收通过。随后原生停止组装控制必须另建共同源并实际确认零增长，再采完整七支；不改本轮阈值、规则、存档或结论。

## 正常停止组装后的实际共同源前置验收

主任务在同一冻结116文件包中经正常简中决议支付凝聚力并停止组装，实际保存`ecng_control_input_0302.sav`、`ecng_warm_0402.sav`、`ecng_common_0502.sav`。只读报告`run113522Z/independent-ecng-native-population-control-precheck.json`已封口，SHA=`00a76065d22cfb7fb4cefcd4f802c8bc61f1d588ecced3de45abd4581ac87541`，354088字节；三档SHA分别为`11e87d81190917adf326cc669f1f8731c0efe20edfa5c62c1b91b2b530083d14`、`633ff3387585369ea3952adc13be07669150fc4014ef10779b156e72e2b536f7`、`cce433c4e78f88fce76b0f8c4df5927c2f9d40330de6c016fffd56d1c8591e0b`，均已独立重算相符。

三档实际P均5497，civilian/ruler/specialist/worker四组人数始终2397/200/1500/1400；所有国内岗位的六个工作量/容量字段与分配三档无差异。0402和0502的`last_month_growth_data`总量、species48及四类别的`growth`均明确为0，月初人数也固定。两档增长来源细项没有序列化，故ASSEMBLY/ORGANIC/DECLINE逐来源数值保留UNKNOWN；原版规则、真实永久停组装carrier和机械物种定义提供有限来源依据，不把缺字段当作保存的0，也不宣称内部队列普遍为空。

两项capital modifier各唯一、永久且倍率正确，实际稳定度100；U7/R0/T7/B.35/n1/J100守卫全通过。warm→common的全部已观察经济context无差异；input→warm仅carrier_flags由3变1，此后不变。warm.current、common.current和common.last_month的完整原生预算类别两两一致；机械师合金维护4.05→0.54只在旧预算暖机历史中保留，不沿用旧预算作新共同源oracle。无active特殊项目，四个国家modifier均永久；未额外读取科研partial，因此不预测未来两月必定无科研完工。

严格P/W合并报告的两项FAIL仅来自立即input：缓存5491/38437对实际5497/38479。warm和新common本身的P/W严格检查已PASS。结论为 **PASS_LIMITED_PRECONDITION**：真实0502成熟共同源可以继续采集0502/0602/0702七支；完整新矩阵仍NOT RUN，每支仍须通过既定core/setup/就业/context/期间及算术门禁。原自然增长七支INVALID、旧严格缓存FAIL和其它未覆盖资源/外国阴性边界全部保留。

静态来源链保存在该报告：上述原生控制来源计划SHA=`e18654698122eb087868573938b4e78d5b6a8510eb9ed51cdff8c162d2bc4c15`，审计器读前后均为冻结`2bee9c8460e07a228d8d0f577aa8245792e2ecc936497c975e6bd422be0173a1`，native parser为`e3308841093cccb0ae7e463067acc5127c6acc69844e632e3b7a5241ac37d984`；每份完整Document读取后均已释放。未修改生产、夹具、冻结G1包、审计规则或原生档。

## 停组装后F00的必要窗口先检

新`ecng_F00_input/warm/measured.sav`实际日期0502/0602/0702，SHA依次为`0e2cfde191ce884af825347be423697692b4c5c63357d48c80fcc741ef281554`、`546988e783f757dc160c4f1e39dcdc276500224438b556278595499a229ae39c`、`b3f5880c758b9eee787558f6806d1bdb89c209fb75df2b2c9795e7cf288bd988`。与真实共同S一同顺序读取，读取前后原生文件SHA/大小及ZIP CRC稳定，审计器保持冻结2bee版本。报告`run113522Z/independent-ecng-F00-window-precheck.json`（SHA=`80cfdb2d10759148a125b7ced8d7decf17c769c065daa050def0f94ed92b469a`，268502字节）已封口。

单支必要窗口守卫及strict P/W均PASS：实际P5497、四组人数、全部国内岗位六字段/分配三档固定，setup身份/日期/全就业与S相符，warm→measured已观察经济context零差异，原生carrier控制及100稳定度正确。measured被测分类社会学8.184、凝聚力1.705、CG维护1.98；不把F00重复填入缺失的其它六支，完整新矩阵仍NOT RUN。

两项额外原生观察独立保留：input相对S的carrier_flags由1变3，warm/measured恢复1；这属于输入共同暖机观察，原工具要求的setup只核日期/身份/就业，input经济context仍须在真实七支齐全后跨支核对，未修改原门禁。measured的current/last_month中leader_officials凝聚力成本为10/8，完整预算差异留在报告；被测分类和country_base一致，不据此宣称所有非岗位成本均已通过。其它分支仍需各自实际检查，前置单支PASS不能替代完整经济验收。

## 停组装后完整七支原生结果

同一冻结116文件包的七支真实input/warm/measured全部完成，日期依次为2210.05.02/06.02/07.02，仍使用正常决议成熟后的实际共同S0502。manifest SHA=`302f57d36bbb4b7ffdbb47ff2ccb9e1491712f12fce34dab3f8a7a9b6abc5da3`；冻结2bee审计器顺序读取共同源及21档，每次释放完整gamestate，不并发驻留22个对象。工具读前后SHA完全相同，CLI退出0，没有修改脚本、审计门禁、epsilon或任何存档。

[完整新矩阵报告](evidence/feedback-redesign/remaining-2026-10-15/controlled-economy-run113522/additive-no-growth-native-audit.json) SHA=`c55fa0ff97453227153a2fb7bd9cba1ed572b8778769b16d16cebba47c926e42`，1521873字节；[精确数值摘要](evidence/feedback-redesign/remaining-2026-10-15/controlled-economy-run113522/additive-no-growth-native-numeric-summary.json) SHA=`a9877808c68e3a2e4c180afc8e47da77c5263045b783e3633ff0a3d7192367ef`，56196字节。报告先生成在run113522Z，约定仓库归档目录由balance在完整run停机后统一按原字节归档；报告已冻结，不为归档改变内容。

本次登记的有限经济、setup与strict P/W均 **PASS**，有限守卫与严格缓存诊断均为空。全部21档实际P5497不变，各组人数、被测岗位及其它岗位满足跨月/同日跨支规则；维护员100+bonus10、biologist60+bonus6和实际容量/分配固定，稳定度100及已观察环境、期间检查通过。原生U在四格中为7，在正面/负面/隐藏三支为8；R始终0、n始终1、T等于实际U，架构modifier唯一且multiplier=T；OFF反向控制倍率及A40输入也通过实际检查。

|分支|实际U|原生凝聚力|归一凝聚力|原生社会学|归一社会学|类别CG维护|
|---|---:|---:|---:|---:|---:|---:|
|F00|7|1.705|1.55|8.184|4.65|1.98|
|F10|7|2.145|1.95|10.296|5.85|1.98|
|F01|7|2.090|1.90|10.032|5.70|1.98|
|F11|7|2.530|2.30|12.144|6.90|1.98|
|FP|8|2.585|2.35|12.408|7.05|1.98|
|FN|8|2.585|2.35|12.408|7.05|1.98|
|FH|8|2.585|2.35|12.408|7.05|1.98|

凝聚力按真实维护员有效工作量1.1归一，社会学按维护员和biologist合计1.76归一。由真实A40差分得到Q0=Q1=1（凝聚力）和3（社会学），A0/A40下架构差值都为`.35Q`，交互项0；正面、负面、隐藏dummy各增加`.05Q`，相应两资源各7项算术均PASS。类别CG维护归一全部1.125，非零country_base各资源不变。没有预设unity必须是.44，社会学没有误用仅维护员分母。

结论只覆盖已登记模板/岗位来源与这组U7/U8、R0、n1、J100的有限加算响应，支持TS05/06的本样本验收；不表示独立乘算完成，也不替代高R、迁移、任意资源、其它模板组合、外国经济、非主谱系国内岗位、空间站/地块/建筑收入或性能用例。所有新支measured仍有leader_officials的current/last凝聚力成本10/8，原样保存在摘要并交独立补充预算审计，不把有限country_base阴性对照扩写为全部非岗位成本通过。端点守卫不证明期间每个tick无不可见变化；未序列化的逐来源增长细项仍未知。首次自然增长版的完整七支INVALID、32项P/W FAIL以及更早自然试跑的INVALID均按原字节保留。

### 最终只读来源归档方案

随本轮真实报告归档冻结审计器、native parser、36项工具测试源码和7项稳定夹具测试源码的原字节快照，以及已有43项开发测试回执；建立逐文件来源路径/字节数/SHA清单，复制前后校验原文件未变。不重新运行游戏或改验收工具，不把开发测试计为原生样本，不复制另一个完整116包；冻结夹具及G1来源继续使用既有静态证据。此清单与原、新两矩阵及前置报告一并由balance纳入同一run归档，保留所有历史状态。

本轮只读来源清单已生成并封口：[最终逐文件清单](evidence/feedback-redesign/remaining-2026-10-15/controlled-economy-run113522/additive-final-readonly-evidence-manifest.json)，SHA=`e6aa3b0d26711bacb312dc2b16f2e5a21fdb9cbce935b39c838f5b3e1da6b042`。内含10份原生只读报告/来源计划的完整身份，以及5份原字节源码/开发回执快照；审计器2bee、parser e330、36项测试e0bd和7项夹具测试`672112b9be2d6b6accc0bbd0bc87db9be39ea3ec8338900e855b6ea3b89245e4`均复制前后不变。已有43项测试回执仍为`0df7be9f4976205efd05cbd71d58584e5a3b9029811d2a73de9e081de6c1201f`，没有为新原生结果改写或重造测试日志。重命名源码仅作身份快照，实际执行入口仍是仓库原路径。
