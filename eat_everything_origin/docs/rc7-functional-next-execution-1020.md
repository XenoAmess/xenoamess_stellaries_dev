# RC7功能下一轮：主线程短执行链

## 目标、范围、验收

本页于2026-10-20先行记录后续操作目标、范围及验收：三类开局全年经济封存后，按**新Machine年末C0重复初始化→Mother参照／真实跃迁→敌星PK／普通拆解／护栏→独立Lithoid首月／自有PK→旧档迁移／跨进程重启**推进。只复用已有命令和原生保存／读取工具，不改Mod、测试工具、SAV或发布门槛。本页作者只离线读现有文档、源码和封存证据；未操作桌面、Steam、活动日志或Git。以下运行步骤全部PENDING，不继承RC6通过结果。

唯一候选为`0.4.0-rc.7`、59文件树`61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`。每个实际保存都绑定其自己的RC7 manifest／run／PID、简体中文及单生产Mod；原生输入链、GPU图、原始SAV／receipt／audit、独立分析和停止后完整日志共同验收。只通过离线数学检查不能代替实际充能、发射、取消、跃迁或进程重启。

## 先直接复用的调用

从综合仓库根`D:/workspace/xenoamess_stellaries_dev`执行；下文相对文件属于子项目`eat_everything_origin`。这不是新安装工具，`Send-R7Effect`只是主线程会话中的薄调用，逐步执行，不整段无人检查地循环。命令取原JSON原字节作为单个参数，不用eval或shell字符串拼接：

```powershell
$R7Old = Get-Content -LiteralPath 'eat_everything_origin/testing/colossus_1019_postfire_plan.json' -Raw -Encoding UTF8 | ConvertFrom-Json
$R7Map = Get-Content -LiteralPath 'eat_everything_origin/testing/colossus_1019_rc6_execution_map.json' -Raw -Encoding UTF8 | ConvertFrom-Json
$R7Rows = @($R7Old.commands) + @($R7Map.commands)
function Send-R7Effect([string]$R7Id, [string]$R7Stage) {
    $R7Found = @($R7Rows | Where-Object { $_.id -ceq $R7Id })
    if ($R7Found.Count -ne 1) { throw 'Missing or duplicate command id' }
    & python -B eat_everything_origin/tools/runtime_1019.py console-open ([string]$R7Found[0].command) $R7Stage
    if ($LASTEXITCODE -ne 0) { throw 'Physical console input failed' }
}
```

`r6_*`只是现有片段ID和标记名，不能据此把它们的旧tree／run／runtime_result带入RC7。两命令资产SHA分别为`76adabaf82dc2c10894222bdb425ee1b994307233e1bccb2c251bdf2f07325c8`、`c9b81e616bc3bc2b79c240f8889fe668d296e5035c80b4cbcb7a9ba18f935650`，本轮未改动。

```powershell
python -B eat_everything_origin/tools/runtime_1019.py frame r7-unique-frame
python -B eat_everything_origin/tools/runtime_1019.py console 'help' r7-unique-close-console
python -B eat_everything_origin/tools/runtime_1019.py native-save r7-unique-save '<实际HUD日期>'
python -B eat_everything_origin/tools/runtime_1019.py native-load '<实际save名>' r7-unique-load
python -B eat_everything_origin/tools/runtime_1019.py console 'fast_forward 1' r7-unique-day
```

`console-open`保留已观察console；保存／加载前先用现有`console 'help'`关闭console并正常关debug overlay。`runtime_single_homeworld.monthly-autosaves`旧日期表固定2200年，2201年后的功能分支不要复用该日历表。每个stage／output用未存在的新名；已失败的尝试另留原件。

## 实际Load后如何拿ID，不猜旧银河

每次真实Load后立即原生另存锚点。先从这个**新receipt**读`archived`，不要把加载输入文件当作新输出。下面是主线程一次性只读核对示例；`<本轮receipt绝对路径>`必须替换，脚本不写文件、不操作UI：

```powershell
@'
import hashlib, json, sys
from pathlib import Path
sys.path.insert(0, 'eat_everything_origin/tools')
import check_1019 as c
receipt = json.loads(Path(r'<本轮receipt绝对路径>').read_text(encoding='utf-8-sig'))
sav = Path(receipt['archived'])
assert hashlib.sha256(sav.read_bytes()).hexdigest() == receipt['sha256']
audit = json.loads(sav.with_suffix('.audit.json').read_text(encoding='utf-8-sig'))
assert audit['save_sha256'] == receipt['sha256'] and audit['date'] == receipt['date']
manifest = json.loads((sav.parent / 'manifest.json').read_text(encoding='utf-8-sig'))
tree = '61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0'
assert manifest['repository_mod_tree_sha256'] == manifest['copied_mod_tree_sha256'] == tree
assert manifest['static_gate']['version'] == '0.4.0-rc.7'
targets = audit['event_targets']
def target(name, kind):
    matches = [r for r in targets if r['name'] == name and r['type'] == kind]
    assert len(matches) == 1, (name, matches)
    return matches[0]['id']
core = target('eep_core0', 'planet')
fleet_id = str(target('eep_mothership0', 'fleet'))
worlds = sorted({r['id'] for r in targets if r['type'] == 'planet'})
obs = c.n.observe(sav, worlds)
mother = c.mother_records(obs)
assert len(mother) == 1 and fleet_id in mother
ships = mother[fleet_id]['ships']
assert len(ships) == 1
print(json.dumps({'date': obs['date'], 'run': manifest['run_id'],
  'targets': targets, 'core': core, 'fleet': fleet_id,
  'ship_and_design': {k: v['design_id'] for k,v in ships.items()},
  'ledger': obs['country']['variables'],
  'order': c.a.block(mother[fleet_id]['raw'], 'current_order'),
  'worlds': {k:{'native':v['native'], 'flags':v['flags'],
    'variables':v['variables'], 'pop':v['actual_pop_sum'],
    'deposits':v['deposits']} for k,v in obs['worlds_1019'].items()}},
  ensure_ascii=True, indent=2))
'@ | python -B -
```

`eep_colossus_probe_target`、`eep_reg_owned_source`、`eep_guard_*`等目标只有相应绑定命令**执行并保存之后**才从`event_targets`取物理ID。plan里的旧planet17、fleet159、ship997、system196一律不带入。国家资本标量是colony ID，不能当物理planet ID；使用目标的`type=planet`和`worlds_1019.<ID>.native`。

如只需外方国家原始信息，现有`audit_save.audit(sav, (0, actual_victim_id))`可纯内存读取；全原生war／army／colonization／ground对象不在轻量audit中时，用`zipfile.ZipFile(sav).read('gamestate')`和已有`audit_save.fields/block/scalars`只读解析。先记录实际ID，再向现有observe传`--world <source> --world <core>`；不能用后来after的差值倒推before人口或目标前提。

已有封存`r7ganchor`是2201.01.01、core4／fleet125／ship809，只有显式Load这个指定锚点才可作为预期核对；新Machine年末必须重新读。本轮优先从**新Machine全年后C0**直接接Mother功能，必要时可明确Load旧RC7 C0锚点作配置分支，但它不替代新开局／经济验收。

## 1. C0 Mother／Relic／跃迁：不串入经济

按[RC7短步骤](rc7-relic-jump-short-execution-1020.md)执行原样Relic创建串、FF6、两张同日详情；然后新邻居绑定串、`survey`、真实UI跃迁、wind1及真实到达／冷却。两串使用`event_target:eep_mothership0`当前绑定，不需要数字ID。参考舰创建后实际归属、fleet／ship／design从其`eep_relic_reference_1019`提取。

主线程最新优化明确：Machine LAST完整yearUI保存后，**原地继续**同日执行`r6_repeat_initialize`两次并保存`r7initrepeat`，以完整initialize／startup／sync覆盖四项重复初始化；随后直接Relic／真实jump，不额外Load旧imported `r7ganchor`。原短步骤保留历史不改，fresh Machine的实际日期／ID在本页重新绑定。布局helper不是完整初始化替代。

本轮输入精简到本次fresh Machine yearUI→`r7initrepeat`→`r7relic6`／`r7jumpready`→`r7jumpwind1`→`r7jumparrived`。已有有效同日SAV可兼任ready，不为角色名重复保存。只有新入口实际无法继续时才把指定`r7ganchor`作为明确备用Load来源，不套其125／809／4数字。

主线程已有worker对象可直接复用：`import runtime_1019 as w; b=w.base; h=b.h; b.h.load_run()`；`w.command_open(command, stage)`、`b.console(...)`、`b.r.native_save(name,date,(0,))`、`b.r.native_load(name,stage)`、`h.capture(stage)`、`h.click_point(client_x,client_y,stage)`都是现有接口。UI全部只由主线程执行。当前工具已将click坐标解释为client，不再自行加旧desktop偏移。

| 实际控件／动作 | 旧成功client位置，仅供新GPU定位 | 本轮必须确认 |
| --- | --- | --- |
| Mother舰船行详情放大镜 | `(360,709)` | 详情实际舰名和50组件槽／6required，不能把舰队全景当详情 |
| 详情关闭／舰队面板关闭 | `(739,162)`／`(387,340)` | 真关闭后再选另一舰 |
| 单舰舰名／舰体hover | 约`(130,708)` | “舰船维护费／维护费”明确归属本实舰；若未显示保留事实 |
| 详情“打开设计器” | 约`(400,603)` | 固定Mother设计本身；无效／普通设计不能冒充 |
| “启动跃迁”按钮 | `(145,339)` | 新hover确为jump，然后点实际绿色有效目标 |
| 搜索 | ASCII `EEP_JUMP_TARGET` | 从本次目标名字和存档对应唯一邻居，不用旧196 |

`check_1019 mother`验证实际Mother设计／三防底线／10yard，并不证明UI stats／jump／维护。它的`same_save_relic_fleets`只筛fleet名`NAME_Relic`；原控制夹具的fleet名为`EEP_Native_Relic_1019`，该列表空不能直接认定参照不存在，应按真实全局目标与舰船设计检查。供电用已完成源推导报告并明确来源，实际维护另采本轮tooltip；不重做不存在getter的调查。

## 2. Machine有效敌星：一条取消＋一次完整发射

Mother／jump采完后**直接沿这份fresh Machine功能分支继续**，不额外Load旧imported锚点。Relic会真实增加维护／海容，jump有真实冷却：两者明确记录在功能基线，不能把这条分支重新计入干净经济，也不能当战斗性能正例。它们不改变EEP吞噬账本，PK前必须仍核C0/G0和无压力C写入。敌目标定位从当前真实Mother位置使用既有作用域命令；清场只按下述限定需要执行。

逐步`Send-R7Effect <id> <新stage>`：

1. `r6_enemy_bind`→保存新绑定／读实际victim country和source physical planet、q、pop、全部可用前提。
2. `r6_enemy_declare`→核真实war participants／goal→`r6_enemy_place`。定位只是公开夹具，不计真实跃迁。若固定敌基地实际困战，才使用`r6_enemy_fixed_starbase_clear`，等原生combat清理并保存新base；不清目标殖民地或国家。
3. `r7pkbase`存实际war／完整有效源／活母舰／C0G0／无陆军参与。`r6_crisis_calibrate`→`r7pkcalafter`，分别读worlds/empires一份奖励，**真实Load `r7pkbase`并保存已恢复状态**，不保留探针收益。
4. 选实际Mother，右键本次实际源；菜单行是**“拆解星球”＋目标名称**。点该行，原生保存queued；订单必须`destroy_planet_order.planet=<实际source>`。推进到首个真实windup0或1／90，存charge。真实hover／点Stop→同日cancel→真正Load cancel并保存cancelreload。
5. 重新真实右键同一源下令，存requeued。按实际原生子订单推进，见下表；每段FF天数由当前读取计数计算，不能一口气从点击日FF120。

| 节点 | 必须从原生order读取 | 下段只推进 |
| --- | --- | --- |
| queued | `destroy_planet_order.planet`，可先有move子订单 | 到真正进入windup，不把移动日当充能日 |
| charge／cancel | `planet_killer_weapon_windup_order.windup`、`windup_time=90`；Stop后空订单 | 取消后重下令重新计时 |
| windup_last | 实际windup89／90 | 1日并另存fire_start |
| fire_start | `planet_killer_weapon_fire_order.fire=0`或1、`fire_time=30` | 到实际29／30，不硬套29天 |
| prefire | fire29／30，源仍活、owner／q／core前提有效 | 1日自然完成 |
| immediate／stable | 源真破碎／无owner／实际人口清空，订单清除，正确EEP收益 | 允许country销毁缓存稳定；按实际目标清理取stable |

旧Stop成功client`(69,339)`，先新hover确认“停止全部命令”，按键提示H并不等于本轮已输入H。旧两次右键为`(465,507)`／`(421,540)`，菜单行中心`(520,538)`／`(538,414)`，说明菜单随镜头变化，**不复用这些地图数字**。由新GPU目视实际目标／菜单或唯一匹配目标名行取box。现`h.click_text`为子串最高分，遇同词描述不应盲用；先检查新capture的`rows`和对应box。新下令SAV中的physical ID才是命中依据。

结算后待原生灭国清理稳定，`duplicate_destroyed_enemy_twice`→同日`r7pkduplicate`；实际Load该档，再`duplicate_destroyed_enemy_after_reload`→`r7pkdupereload`。这两个callback仅允许已毁带receipt源，不能用在有效活源冒充发射。原生ROOT为目标planet／FROM为Mother fleet，不能换FROM为planet。对nomads原生日志如再出现按新实际上下文评估，旧手动CRACKER回调不是本轮真实原生发射对照。

本轮checker的expected_q取**prefire实际size−真实d_lithoid_devastation数**；expected_return敌星为0；worlds/empires各用本银河scratch独立校准。若最后殖民地的原星主在immediate尚留缓存，保留该事实，待stable再核灭国与奖励，不能称第一次无empires已通过／也不能把后续自然清理算重复奖励。

## 3. 同分支普通q2／seed50

稳定敌星后运行`owned_q2_setup`、`owned_q2_inspect`→存`r7normalready`，实际`eep_reg_owned_source`必须size2／pc_machine／恰50主体人口，EEP账本尚未因夹具改变。然后**真正星球决议**“吞噬：献于唯一王座”，不是`eep_begin`代点。

同暂停日存`r7normalstart`：source50→100、core−50、总数守恒、seed_existing100／seed_need0、q2／months5／Situation progress0。按实际FF30逐月保存，读真实target Situation和progress；接近门槛时仅推进到完成前一日`r7normalprecomplete`，再1日自然完成`r7normalimmediate`／稳定`r7normalstable`，不预填“150天”。前后源返回R取**precomplete合格founder groups**，不能抄`eep_last_return`来当期望；跨月其它人口变化需要独立原生依据，不能残差拟合。

收益使用本轮之前账本：C_after=C_before+2，G_after=G_before+2，D=2+floor(C_after/4)，made_after=floor(G_after/6)×100；不能硬套旧C19→21／made300。运行`normal_destroyed_source_repeat`、实际same-day reload，确认无新收益。`r7normalready`保持源活，是后续核心迁移的真实恢复点。

## 4. guard集中做，避免重新发射

真实Load `r7pkbase`，恢复有效敌星和未reserved的home。按下列已有ID，不运行长度>1000的旧大串`batch_inspect/ground_setup/colonizing_setup`：

```text
state_guard_bind
r6_uncolonized_bind
r6_neutral_bind
batch_setup_active
batch_setup_devouring
batch_setup_credit
batch_setup_destroy
batch_setup_secondary_core
batch_setup_artificial
batch_setup_qzero
```

先只读SAV确认home至少7个未reserved可选对象；不满足先停止构造，不把部分目标认作七项。九源物理ID须不同：七批目标＋home外自然未殖民星＋真实中立殖民星。qzero须size2和两个真实损耗deposit；不是改eep_q。保存`r7guardready`→仅FF1、存`r7guardidle`→实际Load ready→`batch_dispatch`／`r6_uncolonized_dispatch`／`r6_neutral_dispatch`→FF1、存`r7guardfired`。每个目标只以**idle同日→fired同日**运行no-settlement并核原生前提仍在，ready→次日不能代替。补当前bound core拒绝`current_bound_core_reject`；同分支`foreign_secondary_core_transfer`→实际外国所有但带eep_core→`foreign_secondary_core_reject`，bound core始终可用。

另一次真实Load `r7pkbase`：`state_guard_bind`→`colonizing_reserve_split`→`colonizing_start_split`→`ground_bind_split`→`ground_armies_split`→`colonizing_inspect`／`ground_inspect`。实际保存readiness，FF1 idle时两个状态仍真才Load ready、分别`colonizing_dispatch`／`ground_dispatch`、FF1 fired。创建军队本身不等于真实地战；需真实双方／攻击方本国／防守方原星主和持续combat，若已结束则夹具失败。该独立护栏的军队不混入前面的无陆军有效shot。

核心重绑定与失主：Load `r7normalready`→`migration_bind_physical_refs`→真实决议“迁移王座至此”→`migration_inspect`→存新core状态→`migrated_bound_core_reject`；再`core_owner_loss_bind_receiver/apply/inspect/dispatch`，保持旧core仍有本国人口、新core被外方拥有且仍为EEP绑定。分别留idle／fired同日对照证明**完成时core owner重校验**，不能只看source护栏。所有旧／新物理core ID从新存档目标取。

母舰损毁留在功能收尾，真实Load已完成高成长档`r7evreport`（C20500/R410、六种tier全非零）后保存before，再`r6_destroy_mother`；随后`r6_destroy_sync`完整initialize／startup／sync、真实月脉冲、已毁档Load后再次同步。要核所有舰队／舰船无新Mother，三个grant flags和国家／core仍有效；6种tier历史镜像允许存在，不能当活装备。这同时验证已有六种随机强化不会因死亡“重发”，不另造高阶夹具。

## 5. Lithoid：首月先封存，再一个自有PK

独立EEP05原生新局Jan1／首月完成startup＋首月非负的既定范围，先封存经济；之后读取本run全局Mother／core。本页不增加第四个全年经济。功能用**`r6_lithoid_loss_setup`／`r6_lithoid_loss_inspect`**，不要旧`lithoid_q2_setup`（后者size2无既有损耗）。

本轮源应为pc_hive／物理size3／恰1真实d_lithoid_devastation／300主体人口，有效q2。保存ready、scratch危机奖励校准后真实Load恢复、`owned_pk_position`仅预先放舰，然后真正自有星右键“拆解星球”90／30；角色与enemy相同，但无须再取消同一组已覆盖的功能。

before C0/G0/D2/made0，after C2/G0/D2/made0/L0、容量差0、G制造0；owned founder返回R取prefire真实可返回group，不能硬写300。原生随机矿／合金／pop分列：若抽到pop，用对应新原生奖励通知GPU／OCR证明每次100，否则native-pop为0；不由core人口残差推奖励类别。source旧损耗只扣一次，以before物理3−deposit1和after持久eep_q2联合核对。

## 6. 接收和后续重启只用现有工具

固定现有原checker SHA `681836d2da9c6b28ee9bfd583c87e5ced96f06543901e71d3dc35fa226f3afdc`，inspector SHA `1ec3ad71f877be5704959134b76e59be077b756a906f7297f278613ee8bfbf92`。现有receiver SHA `d4daa66a575fa8c0ce5bba9796b6c6d4eef0b0573184ec9b6c4e5102fd033ca5`：

```powershell
python -B eat_everything_origin/tools/receive_functional_1019.py template --output '<新intake模板.json>'
python -B eat_everything_origin/tools/receive_functional_1019.py receive --intake '<填入实际角色的intake.json>' --cache-dir '<专用空cache目录>' --output '<新接收报告.json>'
python -B eat_everything_origin/tools/check_1019.py --output '<新报告.json>' mother '<实际native.sav>'
python -B eat_everything_origin/tools/check_1019.py --output '<新报告.json>' settlement '<实际settlement-case.json>'
python -B eat_everything_origin/tools/check_1019.py --output '<新报告.json>' no-settlement '<实际same-day-case.json>'
```

模板必须现在新建：`interface_sources.publisher_interface`当前为`06c60c0a9bd406580314999ae6649365bb5c1fa6c7152c0b0a7fb5a420e06918`，旧模板未必同SHA。每role填写`kind=native_ui_save`及实际save／receipt／audit各path+SHA；自动存档用`native_autosave`及真实advance-start／mtime证明，不冒充UI保存。原始SAV与manifest需在原artifact同目录；封存副本不改receipt指向，把归档映射另记。

`world_ids`用本intake所有实际source／core union，`roles`按工具`enemy_pk/normal/guard/native_state_guard/core/death/lithoid_pk`语义名字绑定，跨run显式`additional_run_ids`及角色manifest。任务`mother/growth/compare/no-settlement/settlement`只调原检查，不解释UI／war／army；receiver结果`OBSERVATION_ONLY`不是18组整体通过。

settlement-case必须有schema、path、source_world／core_world、expected_q、native、expected_return、expected_other_core_pop_delta和独立worlds／empires奖励校准引用。当前原settlement checker明确beneficiary/core owner0；若实际受益国不是0应先报告前置不符，不静默改checker。九guard同日各源分别建no-settlement task；不覆盖跨月人口／库存原始严格差异。

最后沿[最终索引清单](rc7-final-index-closeout-20261020.md)做原public／paid受伤fixture的新RC7 Load／Save／Reload，保留原strict FAIL和v2预算；真进程退出后新PID／同候选tree启动，先Load已存在`r7gbudget1`保留C20500/R400/P10再自然月补10，另Load已测PK／normal稳定非零账本验证没有重复奖励。一次新进程可做这两个既有输入，不为每案另启进程。停止方式和forced实际值如实记录，manifest存在不能当“正常退出”或“已重启”证明。

本页仅交付执行路线。当前没有在此页创建任何RC7功能PASS、final-result、正式版本或Steam发布；后续主线程将实际结果及失败边界回写到相应证据文档。
