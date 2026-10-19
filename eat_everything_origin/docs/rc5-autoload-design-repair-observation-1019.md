# RC5 自动读档修复：独立只读核验

本轮只读检查 `20261019T143452Z` 的真实原生 SAV、审计、保存回执和冻结源码，不操作游戏、不修改 Mod、存档、检查器或原有损伤门槛。以真实 public 0.3.1 部分受伤原件 `p031before` 为完整前置状态，分别比较首次无控制台加载 `r5pautoload` 与实际再次加载后的 `r5preload1`。所有 JSON 使用新文件名，不覆盖 RC4 或原 `1e-6` FAIL。

验收分别记录实际 ship implementation、关联 mobile-starbase implementation、引用设计完整组件、六个 AUX 核心、ship flag 和实际 design flag 的原始存储位置；不得将 ship flag 或根 flags 当成设计局部标记。身份、坐标、人口、岗位、世界布局、库存、全部队列和已付款项与旧原件比较；严格比较器保留全部差异。三防绝对值、最大值和比例误差单独列出，沿用此前 absolute tolerance `0.000001`、relative tolerance `0`，不因新样本改变原政策。

## 已观察事实

`r5pautoload` SHA256 `85681feaee14600ab13d8d8a08bb3ca8b2e4ce8181c3ead5bd69da15b264de38`，日期 `2200.01.01`，冻结生产树 `1cc8b77c28f3d59b0d840982c7f039a209cb66f3e26d9c3280ad2dfa0f9dbd52`。实际 Mother ship1008/fleet128 的 implementation1592 引用新 `_1019` 设计，真实50个槽位、6个 required components，AUX6..11 包含全部六个真实核心。关联 starbase15 的 implementation1591 仍引用旧设计。该首次加载仅修设计，country 全变量与旧原件相同，fleet 新变量仍不存在，不能称已完成成长同步。

全 gamestate 的 `eep_mothership_layout_1019` 仅出现一次，位于根 `flags`，紧邻原生灰蛊等全局事件标记，值为62808000；引用设计1592 的完整原始块内没有这个字符串。实际 ship flag `eep_mothership_design_1019` 同时存在。这些原始事实不足以证明设计局部标记成功或所有设计共享某种内部标记机制，必须保留范围。

首次加载三防为 H92960/93960、A44567.245/44787.6、S69177.6657/167310；相对真实旧原件，装甲比例误差约 `-7.926301029748117e-6`，护盾约 `-4.232120464575662e-6`，原 `1e-6` 两项 FAIL 继续成立。身份、位置、全部队列及队列项、库存、人口、岗位、世界布局和 country 全变量均与原件一致；严格比较保留36项差异。

第二次加载的正式报告须绑定其独立原生回执与 SHA，报告实际设计是否仍有50槽/六核心，并保留根 flag 和旧 mobile-starbase 指针。若设计回旧，整体自动读档持久性结论为 FAIL，不以首次安装成功替代第二次加载结果。

实际 `r5preload1` SHA256 `72ad1539bebefedb109da01486dace37db211d9cd01819795b985bc33772384e` 仍为Jan1。ship1008 和 starbase15 均引用旧设计1608，实际引用设计没有六核心；护甲/护盾最大值回到24429.6/61776。当前三防 H92960/93960、A24309.16207/24429.6、S25542.52272/61776。ship 历史迁移标记和根 flags 中的新字符串仍在，但没有阻止实际设计回旧。country/fleet 全变量、身份、位置、空队列及全部队列项、人口、岗位、布局和库存继续与真实旧原件一致。

独立报告 [rc5-public031-autoload-reload-report-v1.json](evidence/1019-analysis/rc5-public031-autoload-reload-report-v1.json)，SHA256 `8386be1b6a5a49c5ef93b5df751e7b0bb0e0f1e5325caebfe9af4992b14320b1`，结论 FAIL，40项限定事实中31项为真。完整原始 ship/base/design/root flags、冻结 helper/event/on_actions 文本和来源 SHA 均入报告；旧原件→首次加载严格36项、旧原件→再次加载28项、首次→再次加载32项差异全保留。失败项明确包括第二次加载的新设计/50槽与六核心、设计原始块未见 marker，以及两阶段装甲/护盾比例超原门槛；不将这些不同问题合并归因为已证明的引擎内部机制。
