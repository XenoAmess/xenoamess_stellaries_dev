# RC7成长矩阵独立逐对观察

## 目标、范围与固定前件

主线程运行唯一UI采集器，本代理只读完成且稳定的原生refresh/final样本对。运行 `20261019T164112Z`，prefix `r7mx`，Mother fleet125/ship809，锚点 `r7ganchor.native-save.json` 对应2201.01.01，主线程报告原ZIP SHA `aec53eeed736d23abb856b7a1c1696657ce55517124097f1ad6c69921f1d8385`。锚点是RC6干净C0导入RC7后原生加载保存，不能冒充RC7新游戏全年或startup_stability。新prefix的preflight因 `r7ganchor` 占用r7g名称而拒绝旧prefix不涉及输入，本轮只接受r7mx。

固定RC7 tree `61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`、59文件、简体中文、同一已绑定EXE。使用当前checker SHA `a8d70f1015b6f1f4026ae811c38653997fd41a55bbca9b9b8fba391fb4070bf5` 及v1–v5原字节模型链（v5 SHA `b761caa8b5e31cd2981588cc307e9d1da8840b69a4d3ab403454cd3a197c6f28`）。完整包与v5 source-only核对不代替实际运行证据。

## 预声明预测与验收边界

- 九节点C为0/9/10/19/20/49/50/200/10000，L=floor(C/10)、B=floor(C/50)；本矩阵各节点单次需求小于或等于200，应R=B/P0，R=sum六N，country镜像精确，六tier永久且不下降。
- C0 final先取得当前同夹具的实际十modifier和最大H/A/S截距；不直接移用RC6值。此后固定三防增量为 `1500L+3000Nh`、`1287L+2574Na`、`2091.375L+4182.75Ns`。
- 十modifier只用已固定v1/v2/v5源系数分离L/N：H/A/S mult为`.05L+.1N`，damage为`.05L+.05Nd`，tracking为`3Nt`，固定H/A regen为`.1L+.2Nr`，三个flat add保持。
- 三防HP量继续abs=max(.01,8*ULP32(expected))/rel0；十modifier固定abs.01/rel0；计数、tiers、身份、真实装备精确。不得根据未来结果调系数或余量。
- 原生trigger导出在refresh日取得，核其对应refresh实际maxH/maxA；final原生最大三防及存储的十modifier与该节点预测比较。C10000预期同日196次补差一次完成，refresh/final六N均不再变，但仍由原生样本验证。
- 跨月government使用当前checker的窄身份比较：仅直层finite scalar council_agenda_progress单列时间观察，其他所有政府字段/unknown保持严格；完整raw与观察值保留。same-day repeat/reload不在本矩阵观察范围，不放宽其精确规则。

## 读取与归档流程

1. 仅监看预声明 `r7mx-nNN-cC-{refresh,final}` 的SAV/audit/observation六文件元数据，全部存在并连续稳定后打开；不读progress receipt、UI、OCR、动作或运行日志。
2. 每对原ZIP仅解析一次，核CRC、日期、SHA、audit/observation交叉绑定、唯一country0归属、实际新设计及六AUX真核心。来源六文件SHA与元数据写入新不可变报告。
3. C0完成后固化本轮实际截距、设计载荷、government raw及普通舰对照；以后只读自己的已封存报告作比较。普通舰负控只覆盖实际同国非Mother ID集合和最大三防，缺失字段保持缺失；不宣称未导出的普通D/T/regen已验证。
4. 只新建 `rc7-growth-pair-nNN-cC-observation-v1.json`，状态为OBSERVATION_ONLY或FAIL_OBSERVATION；每项列实际值/预期/差值/所用余量。不把单对无失败写为完整矩阵、预算、重载或发布通过。
5. 发现任何真实不匹配立即告主线程，不改checker/collector/Mod/历史报告，不读取未来样本拟合。原RC6失败及默认while诊断保持原样。
6. 18个样本全部完成后另建不可变独立矩阵总结，只汇总本九份报告、覆盖与失败，不代替主线程正式report及repeat/reload/20500 monthly补充；startup_stability仍明确缺失。

## C0实际截距

[rc7-growth-pair-n00-c0-observation-v1.json](evidence/1019-analysis/rc7-growth-pair-n00-c0-observation-v1.json)，SHA256 `9488ec81e834bd591e151d2d1391baaa5eb9f65514f92f191bb7b7d51a91b49d`：170项逐对检查均匹配，状态仍OBSERVATION_ONLY。final为2201.03.01，原ZIP SHA `481724067359f10ecb899a56434dd829565c59bad061a6c618976de391abd10c`。

实际C/L/B/R/P与六tier均0；Mother125/809、实际design16777235，完整设计body SHA `be9562535dd559dbc4c74de4b8687d2075bbdd1b41b897e6b771ac98627129d9`，六真核心装备完整。新实际最大H/A/S截距为93960/44787.6/167310；十modifier依预声明顺序为 `-70000,2.132,0,.74,0,3,4.1,15,1.392,2.088`，两max trigger为93960/44787.6。它们是本RC7样本独立取得的截距，虽然数值与RC6一致，也未借用旧结果替代本次采样。11个普通舰ID和原生最大三防稳定，缺失shield字段保持null；government进度作为时间观察保留，其他政府结构匹配。

## 观察方法原字节留档与C9

本轮独立inline观察程序已另存 [rc7-growth-observer-method-v1.json](evidence/1019-analysis/rc7-growth-observer-method-v1.json)，SHA256 `547e18edb98dd76c8a7137ae099e88babb53098f606330ad69e56c9479089f80`；其中完整Python源UTF-8 SHA `13695c0a0f987f1cdfccc0ef01e156901f148f2c393e279f73d99a1c210d781e`。留档文件不是新UI工具，不触发执行；实际顺序监看器只逐index等待六文件、调用这段已固定分析，首个失败立即停止后续读取。生产、既有工具及live receipt均未更改。

[rc7-growth-pair-n01-c9-observation-v1.json](evidence/1019-analysis/rc7-growth-pair-n01-c9-observation-v1.json)，SHA256 `ec976ce059b74d17e8e9d7b477e9ffd652bcd669babb1b058223334aeb9f8c56`：2201.05.01 final，C9/L0/next1/B0/R0/P0、六tier0，三防与十modifier仍为本次实际C0值。170项检查均匹配，11普通舰负控保持，状态OBSERVATION_ONLY。

## C10首次基础升级

[rc7-growth-pair-n02-c10-observation-v1.json](evidence/1019-analysis/rc7-growth-pair-n02-c10-observation-v1.json)，SHA256 `dbc5248d77f17d6656b959df20e6d478f7bda115d6e0357d970f325d9d21f543`：2201.07.01 final，L1/R0/P0、六tier0。最大H/A/S为95460/46074.6/169401.375，即实际C0加1500/1287/2091.375；十modifier符合一级源增量，damage4.15、固定H/A恢复1.492/2.188、tracking15。174项检查均匹配，真实设计/六core及普通11舰负控保持，状态OBSERVATION_ONLY。

## C19同级边界

[rc7-growth-pair-n03-c19-observation-v1.json](evidence/1019-analysis/rc7-growth-pair-n03-c19-observation-v1.json)，SHA256 `bb5a35c8d5ea376ef11face5c9e2de5c8fbd0f8f4135a06ec06455ac53bedf49`：2201.09.01 final，L1/next1/R0/P0、六tier0，最大三防与十modifier精确保持C10的同一级状态。174项检查均匹配；设计、普通11舰负控和政府身份持续匹配，状态OBSERVATION_ONLY。

## C20第二级

[rc7-growth-pair-n04-c20-observation-v1.json](evidence/1019-analysis/rc7-growth-pair-n04-c20-observation-v1.json)，SHA256 `4eef96b767fbf089bbc7dc951e78c74a87e9f4894ac97ecd0c81b07783d621f1`：2201.11.01 final，L2/R0/P0、六tier0。最大H/A/S为96960/47361.6/171492.75，damage4.2、固定H/A恢复1.592/2.288，tracking保持15；成长modifier唯一、永久、倍率2，没有ship组件奖励modifier。174项检查均匹配，11普通舰负控稳定，状态OBSERVATION_ONLY。

## C49不提前发组件层数

[rc7-growth-pair-n05-c49-observation-v1.json](evidence/1019-analysis/rc7-growth-pair-n05-c49-observation-v1.json)，SHA256 `d9f82a4606050e65f41e88eaff9745cc7265caf9fea07cd6d91b103ddcf09a20`：2202.01.01 final，L4/next1/B0/R0/P0、六tier0。最大H/A/S为99960/49935.6/175675.5，damage4.3、固定H/A恢复1.792/2.488，tracking15；174项检查均匹配，未在首次每5级奖励之前发出层数。11普通舰最大三防及身份稳定，状态OBSERVATION_ONLY。

## C50首次随机升级：索敌核心

[rc7-growth-pair-n06-c50-observation-v1.json](evidence/1019-analysis/rc7-growth-pair-n06-c50-observation-v1.json)，SHA256 `ab89811ba671d4750d90227773a39ab4141746db8303468e7d420757642a2529`：2202.03.01 final，L5/B1/R1/P0，自然随机tracking tier1，其他五tier0。实际tracking导出18，分解为本次C0实际15加已装备索敌核心1层的3；没有人工设tier、没有普通奖励modifier。

最大H/A/S为101460/51222.6/177766.875，为5级基础贡献；damage4.35、固定H/A恢复1.892/2.588。174项检查均匹配，11普通舰最大三防和身份保持。这里只证明本节点实际索敌组件贡献，普通舰未导出的tracking不在负控结论中，完整六类覆盖仍待后续样本。

## C200：独立船体、火力、索敌贡献

[rc7-growth-pair-n07-c200-observation-v1.json](evidence/1019-analysis/rc7-growth-pair-n07-c200-observation-v1.json)，SHA256 `fec1e31d70a0d10e4b9f4a20df45ab4f4bc8ad71ee3574ad4572c553b31be955`：2202.05.01 final，L20/B4/R4/P0；实际hull1、damage1、tracking2，另外三tier0，合计4。最大H126960分解为93960实际截距、20级基础30000和船体核心3000；damage5.15分解为4.1实际截距、基础1和火力核心0.05；tracking21为15加索敌核心6。

最大A70527.6、S209137.5及固定H/A恢复3.392/4.088只有20级基础贡献。174项检查均匹配、设计体与六core不变、11普通舰最大三防/身份保持，状态OBSERVATION_ONLY。护盾、装甲、再生核心尚未在本轮出现正层数，不提前声称六频道覆盖。

## C10000完整六核心覆盖与原失效点复核

[rc7-growth-pair-n08-c10000-observation-v1.json](evidence/1019-analysis/rc7-growth-pair-n08-c10000-observation-v1.json)，SHA256 `21ea4cb4826f4c8d369b2ecaa38e92386adef9e99f284aa97cdf88b015dd7be9`：2202.06.01 refresh及2202.07.01 final均为L1000/B200/R200/P0，六tier实际为shield28/armor37/hull44/damage25/tracking27/regen39，合计200，两个时点计数与各tier相同。这是两份原生样本的直接账本结果，区别于RC6诊断中仅反推的较早104缓存。

最大H1725960分解为93960实际截距、1000级基础1500000、船体核心132000；最大A1427025.6为44787.6+1287000+95238；最大S2375802为167310+2091375+117117。实际十导出依次 `-70000,56.532,0,54.44,0,55.8,55.35,96,109.192,109.888`。火力55.35为4.1+50+1.25，索敌96为15+81，固定H/A恢复109.192/109.888为各自实际截距+100+7.8；三防mult也分别符合基础50与各核心0.1×tier。七项曾在RC6失败的存储导出在本新RC7对均匹配，原失败报告不重写。

本对174项检查无不匹配，六core均有真实自然随机正tier，11普通舰最大三防/身份保持。此结果支持明确count200后原collector的预声明30+30天顺序可用，不需要新增等待、重导出或改公式；它没有直接提供首次同日setter后的R200存档，也不能替代20500单次200预算的专门原生验证。

## 已完成九对独立总结

[rc7-growth-matrix-independent-summary-v1.json](evidence/1019-analysis/rc7-growth-matrix-independent-summary-v1.json)，SHA256 `5a4c28e85dcf10ab79f3d1feac7817f4da66b09262c1c438e71927f2c056aae1`，汇总九份不可变观察、18个互异原生SAV SHA、五模型SHA、本轮独立C0截距和完整政府时间观察。共1558项观察检查，0项不匹配；六核心自然正tier覆盖齐，C10000 refresh/final原生三防也完全相同。只从自己的九份既有报告汇总，没有再次解析SAV或读取补充阶段。

总结状态保持OBSERVATION_ONLY，明确不包含同日重复/重载、20500单次400/10及monthly410/0、RC7三政体真实新开局全年、报告UI、实际回血或面板DPS、完整gamestate相等。主线程仍需正式report及对应补充证据才能对那些范围下结论；RC6旧FAIL全部原样保留。当前checker、collector、生产包与源模型没有因观察结果再改变，亦未进行Git操作。
