# RC6逐对成长只读观察（2026-10-20）

## 事前目标与边界

主线程已启动唯一UI worker61271，运行 `20261019T150008Z`、prefix `r6g`，Machine母舰fleet125/ship809；入口为实际 `r6mcyearui`，自动存档目录由主线程确认是 `save games/eep03_-1033273808`。本任务仅在每一对refresh/final的原生SAV、audit与growth-observation共六文件齐全且元数据稳定后，独立只读分析该对一次；不解析正在改写的progress receipt，不读取日志、HUD或操作UI。

只新增本说明与不可覆盖的逐对观察JSON。不得改生产、采集器、检查器、既有模型/证据或Git，不预填未来结果、不宣称全量PASS。C0 final实际十modifier与三个native最大值作为后续截距；未齐以前只等待文件。

## 固定来源、公式与容差

源模型v4 SHA `6eb5ef0ef58fb353edd6e3f31b932ddc4bbf6b8b42b3bb6eaf2881fe51bd4c7f`，候选tree `cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a`。沿现有 `check_growth_1019.py` 的source验证、counts/prediction与数值比较原语，复核其实际结果；不建立第二套容差。

- C节点固定0/9/10/19/20/49/50/200/10000；L=floor(C/10)，B=floor(C/50)，正常本矩阵R=B、P0，R=sum六tier、六tier为非负整数、country镜像相同。
- H/A/S最大值相对实际C0分别增加 `1500L+3000N_hull`、`1287L+2574N_armor`、`2091.375L+4182.75N_shield`。
- 十modifier按原模型分离L与N；三个flat add不变，H/A/S multiplier为`.05L+.1N`，damage为`.05L+.05N_damage`，tracking为`3N_tracking`，固定H/A regen为`.1L+.2N_regen`。
- 三防HP量使用原 `max(.01,8*ULP32(expected))`、rel0；十modifier固定abs.01、rel0；离散字段精确。此为工程余量，不宣称已证明引擎存储位宽。
- refresh只核当前计数/装备等，不用其中可能来自上一节点的旧导出判本节点属性。只有final的十modifier及maxH/A trigger参与当前预测；最大盾直接取原生字段，不使用不存在的max-shield trigger。

## 读取与独立观察设计

1. 只监看预声明文件名的存在、size、mtime。六文件至少两次元数据相同并距离最近写入有稳定间隔后，才打开内容。若文件仍缺或变化，只等待，不反复解析。
2. 对该对原生ZIP核CRC、根日期与SHA，核audit/observation的SHA/date/身份，并把这六份文件SHA与元数据写入新报告。报告读原ZIP获得实际设计、计数、变量、修正与普通船；audit/observation仅作为交叉绑定，不替代原生值。
3. 原生Mother必须仍为125/809、country0唯一归属，实际六核心AUX6–11各一，完整载荷稳定。对照已有source checker的counts检查，不从shipflag或实体section代替实际implementation设计。
4. C0 final形成实际截距，保存完整原生十导出、三max与普通舰ID/最大三防。后续逐pair按该截距、预声明L/N系数预测，记录expected/observed/raw_delta/applied_tolerance/ULP。不得用未来tier结果拟合。
5. 普通舰负对照沿checker边界：同国非Mother ID集合、native最大H/A/S；每个频道要求至少一项真实正数。未导出的普通D/T/regen不能声明已实测。
6. 每对只生成一个新 `rc6-growth-pair-nNN-cC-observation-v1.json`，状态限定 `OBSERVATION_ONLY` 或明确 `FAIL_OBSERVATION`；附逐项checks，不把早期单对解释成整套通过。若不匹配立即通知主线程，提供原值/预期/差值/容差及原SAV SHA，不自动改测试。
7. 不读取未来阶段或progress receipt；已经完成的一对不反复重写。全矩阵及repeat/reload/budget补充齐备后由主线程运行正式check_growth report，单对观察仅作提前发现错误的独立证据。

## 首对实际观察：C0及完整government块差异

完成六文件稳定检查后，C0 pair仅分析一次。报告 [rc6-growth-pair-n00-c0-observation-v1.json](evidence/1019-analysis/rc6-growth-pair-n00-c0-observation-v1.json)，SHA256 `8073d947e1901ab28a21f0c9d49944656c7455864ef72c2b820114bd535a6021`，状态 `FAIL_OBSERVATION`，170检查中1项不匹配。

唯一差异是原检查器沿用的完整government.raw相等判据：2201.02.01 refresh的 `council_agenda_progress=6750.75`，2201.03.01 final为6808.5；国家政体、authority、civics、origin及议程名称相同。该自然跨月数值位于government块，因此原完整块比较失败。本任务没有删除该失败或修改检查器/容差；已即时交主线程处理。

实际C0 final ZIP SHA `11a04bd857199fcedb00e8334e0d6b04fc9b092dcf6abfc0c7c5493f3f4dd847`：Mother125/809、实际design1527新完整体；C/L/B/R/P及六tier均0。原生最大H/A/S为93960/44787.6/167310；十modifier截距依次为 `-70000,2.132,0,0.74,0,3,4.1,15,1.392,2.088`（顺序按预声明MODIFIERS）。伤害4.1是真实aggregate，只作为已声明的C0截距，不倒改源系数。六core实际槽位、无奖励modifier、普通舰三防对照及其余本对检查匹配；不据此写整矩阵PASS。

## C9观察

[rc6-growth-pair-n01-c9-observation-v1.json](evidence/1019-analysis/rc6-growth-pair-n01-c9-observation-v1.json)，SHA256 `66f0e65be8e9ac8adcfc314155180f7f31e480f4fb05f5e58671ebfcb86ec3e2`。C9/L0/next1/B0/R0/P0、六tier0；十导出和三防与C0相同，11个普通舰ID及最大三防稳定。170检查中两项完整government块比较失败：refresh议程进度6866.25、final6924，对照C0final6808.5；报告保留完整raw差异与 `FAIL_OBSERVATION`，未静默过滤。

继续使用C0已经记录的真实截距作数值观察，不把其整体FAIL伪装通过。唯一已知失败属于完整government块判据；观察脚本允许该已保留失败不阻断后续属性分析，原比较仍逐项执行且失败仍记录，不改变源公式、数值容限或正式checker。已向主线程与release维护者报告该问题，任何正式工具修正需另行授权与记录，旧观察JSON不重写。

## C10及工具修复协调

[rc6-growth-pair-n02-c10-observation-v1.json](evidence/1019-analysis/rc6-growth-pair-n02-c10-observation-v1.json)，SHA256 `ff38776c75f8f4b7d31dec747c3330b2ab72f1baa4afd77be2a3b4c22aebdd43`。L1、R0/P0、六tier0。实际最大H/A/S为95460/46074.6/169401.375，相对C0正好增加1500/1287/2091.375；damage4.15增加0.05、固定H/A恢复1.492/2.188各增加0.1，其他导出符合源分离预测。11个普通舰身份与最大三防不变。174检查中仅完整government块的两项跨月比较失败，状态仍 `FAIL_OBSERVATION`。

主线程确认跨月完整government比较存在判据缺陷，已另派工具代理先docs、保存a66原工具字节后最小修复：仅直层finite scalar `council_agenda_progress` 单列时间观察，其余所有字段/unknown仍精确；同日repeat/reload保持原raw精确。数值/HP/四模型/collector均不变。本观察继续使用原工具及原判据留存结果，不自行改checker，也不把原FAIL改成PASS。修正后如需补充解释，另写新版本supplement，不覆盖原JSON。

工具代理已提供a66原字节快照：[check_growth_1019.py](evidence/1020-growth-government-identity/old-tool/check_growth_1019.py)。后续观察从该不可变快照导入原counts/prediction/数值比较原语，不读取正在修改的正式checker；运行时只将模块ROOT绑定回项目路径，不改快照字节。源码与源模型核对只读59文件和四模型JSON，不读运行日志或UI。

## C19观察

[rc6-growth-pair-n03-c19-observation-v1.json](evidence/1019-analysis/rc6-growth-pair-n03-c19-observation-v1.json)，SHA256 `a5e9e05debbd9ac3a7955d0bc4eb86d07af4f66e24c7ddd0e39005079b20547b`。L1/next1/R0/P0、六tier0；最大三防及十导出与C10完全相同，11个普通舰身份/三防稳定。174检查中原rawgovernment跨月比较两项失败，原 `FAIL_OBSERVATION` 保留；尚未观察未来节点。

## C20观察

[rc6-growth-pair-n04-c20-observation-v1.json](evidence/1019-analysis/rc6-growth-pair-n04-c20-observation-v1.json)，SHA256 `10dd5cac09989ad47ee1b3db422a1944136794432e5f0bba0b0fd50bafdb2d20`。L2/R0/P0、六tier0；实际最大H/A/S为96960/47361.6/171492.75、damage4.2、固定H/A恢复1.592/2.288，均符合C0加两级的事前系数。成长modifier唯一且永久、multiplier2，无ship奖励modifier；11个普通舰身份/三防稳定。174检查中仅原rawgovernment两项跨月比较失败，原 `FAIL_OBSERVATION` 保留。

## C49观察与判据修复补充

[rc6-growth-pair-n05-c49-observation-v1.json](evidence/1019-analysis/rc6-growth-pair-n05-c49-observation-v1.json)，SHA256 `3d09c38933d92d680526355aded24943e0b8b9f4e0bb940be22380dd11fc1f59`。L4/next1/B0/R0/P0、六tier0，尚未提前发出组件层数。实际最大H/A/S为99960/49935.6/175675.5，damage4.3、固定H/A恢复1.792/2.488；源预测与普通11舰对照匹配。174检查中原rawgovernment两项失败继续保留。

工具代理另行交付修正checker SHA `0c31f76491c39aff56fb054088d2a8fa4b592eb7f0ad186c5f1ec0c6625832bd` 与41项离线测试结果，及 [fixed-native-pairs-supplement-v1.json](evidence/1020-growth-government-identity/fixed-native-pairs-supplement-v1.json)，SHA256 `9a4e721f22a32a7785df6dab64cb39bf9c323412e771b2c89989c7b4e2cd947f`。该supplement仅使用C0/C9原FAIL里完整raw字段，说明两对议程进度各+57.75、其余政府结构相同，不改原FAIL、不重读其采样SAV、不宣称全矩阵通过。

为避免标准Python import向冻结old-tool目录写缓存，后续观察在项目import之前设 `sys.dont_write_bytecode=True`；已生成的单个标准pyc由工具代理精确清理，原snapshot源字节与所有观察报告未改。

## C50首个自然随机组件升级

[rc6-growth-pair-n06-c50-observation-v1.json](evidence/1019-analysis/rc6-growth-pair-n06-c50-observation-v1.json)，SHA256 `ff1b82dc1299298724e0d34b95f7ce10d2dba6ccc7695a1f190cecc7860e6d29`；final ZIP SHA `fb310f19b4c133375f2b05ee08df9be2bd0786a5ddaccd1f1b159276550629bc`。

C50/L5/B1/R1/P0，实际自然随机选择damage tier1，其余五tier0；没有人工设tier。原生damage导出4.4，按预声明源系数分离为实际C0截距4.1、L5基础0.25、已装备火力核心tier1贡献0.05。最大H/A/S为101460/51222.6/177766.875，只含5级基础贡献；固定H/A恢复1.892/2.588，tracking15。实际六AUX组件设计体不变、只有base与倍率5的成长modifier，无ship奖励modifier；11个普通舰身份与最大三防保持。

本对174项检查只有旧rawgovernment跨月两项失败，原 `FAIL_OBSERVATION` 保留。这里是首个真实自然组件升级的限定正证据，不是六类全部覆盖或完整成长/repeat/reload/budget通过；C200及C10000仍待各自文件齐全后读取。

## C200观察

[rc6-growth-pair-n07-c200-observation-v1.json](evidence/1019-analysis/rc6-growth-pair-n07-c200-observation-v1.json)，SHA256 `6331577631532bff6cb9e94aa050aa227a5612aeac2ed0b259e1636f83cc555d`；final ZIP SHA `805baa0d927c122fecb1f44034001922fde0b0a02fa4b5fa2337906a7d30dda3`。

L20/B4/R4/P0，实际自然armor2、damage2，其余四tier0。最大装甲75675.6分解为C0的44787.6、基础成长25740、实际装甲核心5148；damage5.2分解为4.1、基础1、核心0.1。最大H123960、S209137.5为纯20级基础贡献，固定H/A恢复3.392/4.088、tracking15。六core设计体、无外挂奖励及普通11舰三防/身份保持；174检查中仅旧rawgovernment两项失败，原 `FAIL_OBSERVATION` 保留。六频道全覆盖仍待C10000，不提前判定。

## C10000：真实导出失败与刷新时序边界

[rc6-growth-pair-n08-c10000-observation-v1.json](evidence/1019-analysis/rc6-growth-pair-n08-c10000-observation-v1.json)，SHA256 `177c8b96cb32152ce2fcc818eba417a9b75bf72bddb21a1ca68cf76bd086a37c`。这是属性导出的真实失败，区别于已独立修正的跨月government判据；原报告及全部18个原始样本保留，不更换公式、容差或模型以获得通过。

2202.06.01 refresh与2202.07.01 final均已记录C10000/L1000/B200/R200/P0，实际六tier为shield34/armor37/hull39/damage22/tracking41/regen27，合计200；两个时点六tier及计数相同，不能把refresh描述为实际记录R104。final最大H/A/S为1710960/1427025.6/2400898.5，符合事前源公式；但存储的十modifier导出中七项不符合相同实际tier：H/A/S multiplier实际54.532/52.54/54.4，对应预期56.032/54.44/56.4；damage54.75对55.2、tracking81对138、固定H/A恢复103.992/104.688对106.792/107.488。原固定abs.01容差下均失败。三个flat add、设计体和普通11舰最大三防仍匹配。

refresh实际最大H/A/S为1665960/1378119.6/2317243.5，final保存的maxH/maxA trigger导出也仍为1665960/1378119.6。使用原有C0截距、原有L1000基础项和原有组件系数进行诊断反推，refresh三max与final七个存储modifier导出一致指向较早核心层数H24/A18/S14/D13/T22/regen13，合计104。此104是从数值反推的缓存状态，并不是已经在原生SAV中观测到的账本R104；不得混写两种证据。

为调查这一差异，当前新增只读范围为：核本机生成的原生while契约、原版显式count实例、冻结RC6发放while及既有collector的操作顺序；将既有不可变观察JSON中的数值用不变源系数反推，生成新的诊断JSON，不重读原始SAV、不改旧JSON。该分析只定位可检验假设，状态为OBSERVATION_ONLY；同日repeat/reload及独立重新export由主线程操作，任何后续结果另存证据。

## while默认上限假设的原生来源与可证边界

本机 `20261019T130448Z/logs/script_documentation/effects.log` 第3343–3346行（SHA256 `064b281a6c3a97f4261dfd30c3f761d1373a8ed82390fdc0109be9a112f6f489`）说明while在limit不再满足或达到count时停止，展示 `count = [3|Variable]`，没有在这段文档明确写默认100。当前游戏原版 `common/scripted_effects/marauder_scripted_effects.txt` 第1175–1182行同时使用同层 `count = 100` 和 `limit`（SHA256 `5fa5714b4d491993589226db4399c72af48de3f7d763d37e4a7e758c87e74fec`）；`common/solar_system_initializers/federations_initializers.txt` 第1703–1708行使用 `count = 115`（SHA256 `16b8cf994c5b46b8e08a56f2741f93cffd0b2979702d9a1e53914ae9c5356bfd`）。这两份原生实例分别支持count与limit共存、显式count可以超过100，不能把100理解为不可提高的硬上限。

冻结RC6 `eep_sync_mothership_components` 第33–50行虽然设置工作预算200，并在limit检查预算，但while没有显式count。工具代理对同一游戏EXE独立只读发现“aborting after 100 repetitions”及“Set a higher max count”诊断字符串，具体原字节绑定由其独立报告保存；字符串存在本身尚不等于本轮调用路径已被反汇编或运行追踪证明。

因此，目前可检验解释为：C200时实际R4；C10000同日首次调用可能只发100而达到R104，首个30天途中组件缓存按这一状态刷新；到2202.06.01月度回调再补96达到R200，但当月1日立即export读到更早的组件聚合值；第二个30天后实际max已刷新，保存在变量中的旧export仍保留。已有refresh/final数值与该解释一致，但原collector在setC+sync后直接推进30天，再保存第一个原生autosave，原18样本没有该次调用后、月度回调前的同日R104账本。因此应通过主线程独立同日计数探针验证while默认次数，并在刷新后重新export判当前聚合；不能用反推结果冒充缺失的中间存档。

既有collector源码SHA256 `cab98ce18119f27838456dd6118001cc7fee5254b3150c5e5c8fcf5365f7e747`：第156–164行定义refresh前setC+sync、final前export；第284–303行每阶段随后执行独立 `fast_forward 30` 并采集原生autosave。这里没有插入同日setter后原生保存，不能从脚本顺序单独证明实际引擎首次发放数量。候选显式count200的语法有原生来源，但本任务不改生产包、不开始20500预算验收，也不把尚待复验的200预算写为通过。

本次新诊断已保存为 [rc6-growth-c10000-cache-while-diagnosis-v1.json](evidence/1019-analysis/rc6-growth-c10000-cache-while-diagnosis-v1.json)，SHA256 `9ebbf2c916dd456fd426729e6506fbde7c0e38dad23a18548d6857d46f437a28`。它只引用既有C0/C200/C10000不可变观察报告，完整列出七导出和三max反推、实际refresh/final账本R200以及缺失的R104中间证据；未重读任何SAV。工具代理的独立原生来源归档为 [1020-native-while-primary-evidence-v1.json](evidence/1020-native-while-primary-evidence-v1.json)，SHA256 `0058ad7333e0c5b594eb06117d856ef3130b064912295523cac4681ecc69112c`，绑定当前EXE诊断字符串的准确字节偏移、原生生成文档和冻结while。该归档使用另一运行生成的effects.log（SHA `985c95672f491f0458fcd34232743e2c2a1b9e1862743e2b156eea7e9ca5a773`）；上文独立核对的130448Z文档SHA仍单独保留，二者不能混作同一文件。
