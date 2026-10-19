# 1019：移动Starbase真实动态组件链路调查

## 目标与范围（调查前）

优先研究原生Starbase的module／building／equipped_component到实际ship design／runtime component的物化链路，以及固定事件Mother是否能在保留身份、船坞队列和设计主体的条件下增加或升级真实组件。只读查阅本机精确4.5.2原版脚本、引擎生成的effects／scopes文档，以及公开Mod的原始技术代码；不修改Mod、不操作UI、不编辑SAV。

本页不重复通用动态组件API或生物舰成长路线；重点核查模块／建筑API、standalone重建、固定事件设计与可升级属性之间的边界。现有探针证明standalone可保存，不代表组件已物化或生效；后续结论必须明确静态事实、推断和仍需原生实测的部分。

## 验收与交付

- 记录本机原始文件路径、相关定义和SHA256；公开来源只采用作者仓库／原始Mod代码或官方技术资料，保留可核对链接。
- 给出每条链路的可用原生effect、scope、潜在门槛和最小可测探针，不把静态字段存在当作实机成功。
- 明确fixed event Mother、普通原生juggernaut及普通starbase之间可比较的变量，记录自动设计／required components／standalone／模块建筑／运行时weapon的数据层。
- 仅在原生SAV与面板证实真实组件物化／属性生效后，才能推荐接入每5级奖励；无法证明时保留限制，不以普通modifier冒充组件。

## 调查记录

调查日期2026-10-19；只读研究，未执行本页探针，未修改Mod或游戏文件。准确游戏EXE SHA256仍为 `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。

当前最值得补测的是**建筑equipped_component**。它在原版中有真实三件装甲／护盾的重复装备定义，与此前只写入standalone的光环探针不同。固定事件Mother是否经过此物化链尚未知；不能根据standalone失败提前否定建筑链，也不能根据原版方舟定义就宣告Mother成功。

### 1. 原生链路与边界

| 层 | 本机原始事实 | 对Mother的含义 |
| --- | --- | --- |
| Starbase module | `common/starbase_modules/00_example.txt:7`：module安装时把section加入station design；换成不同section会重建整艘design。`:12`的component_set沿owner已研究科技选择组件阶级；triggered form最后符合的一项生效 | 有真实动态重建入口，但风险是整艘Mother固定设计被自动设计替换，不能只看新模块出现 |
| Starbase building | 同文件`:24`：equipped_component及triggered_equipped_component可重复，每项贡献实际装备；building直接给station装备组件 | 不必先加普通ship section，优先级高于module探针 |
| 原版实用定义 | `common/starbase_buildings/00_arkship_component_buildings.txt:4` 的arkship_armor含三次LARGE_ARMOR_1；`:148`附近arkship_shield含三次LARGE_SHIELD_1。两者均允许重复建筑；potential检查owner科技和is_arkship_starbase | 可先force安装现成建筑，但effect是否绕过potential／零槽限制待实测；失败需分辨是门槛还是物化链 |
| 原版调用 | `common/scripted_effects/nomads_effects.txt:351`及`:3443`起，实际调用set_starbase_building把装甲／护盾装入1～8号槽 | 是原版运行脚本中的真实使用，不只是说明注释；调用目标本来是方舟，不证明juggernaut也可用 |
| 槽容量 | engine modifiers.log:304/307列出starbase_building_capacity_add及starbase_module_capacity_add，Category为Starbases。普通starport的ship_size.modifier含2模块／1建筑；方舟也在ship_size.modifier中给容量 | 修改器可以给槽，但不能把字段名当作console effect直接执行 |
| Mother底盘 | `ship_sizes/18_juggernauts.txt`为可设计juggernaut、shipclass_starbase、只有core section_slot、十船坞。`starbase_levels/01_juggernauts.txt`没有module_slots或building_slots，ship_size也没有两项容量 | 当前Mother没有现成建筑槽。module额外section尤其容易碰到船体槽／实体定位器不匹配 |
| 原生重建 | effects.log:3838的rebuild_owned_starbase_designs只承诺重选country的“non-designable starbases”自动配置 | **推断**：juggernaut底盘本身可设计，固定事件Mother可能被排除；既有rebuild失败不能证明普通station或建筑链都失效 |

`starbase_type=arkship`只是技术解锁文字分类，`00_example.txt`明确要求真正限制在potential里写scope条件。因此不能仅靠把新建筑starbase_type改为starbase，就认为已经移除了is_arkship_starbase门槛。

### 2. 精确原生effects与scope

生成文档来自 `C:\Users\1\AppData\Local\xenoamess_stellaries_dev\runs\20261019T081638Z\logs\script_documentation`：

| 接口 | 支持scope／限制 |
| --- | --- |
| set_starbase_building = { slot = 1 building = arkship_armor } | starbase；slot从1开始。没有文档保证超容量slot能自动扩容或绕过potential |
| remove_starbase_building = { slot = 1 building = arkship_armor } | starbase；可以只移除这一槽、这一建筑 |
| set_starbase_module = { slot = 1 module = shipyard } | starbase；更换section可能重建整个ship design，故不优先在Mother测试 |
| add_modifier = { modifier = KEY days = -1 } | 支持starbase；KEY须事先定义，不能内联starbase_building_capacity_add字典冒充KEY |
| set_starbase_size = SIZE | 支持starbase，但改变底盘／level，可能重建、改变移动性和船坞，不作为保持Mother主体的加槽办法 |
| starbase scope link | scopes.log:266支持从fleet／ship进入starbase；可直接由eep_mothership舰队目标进入 |
| design scope link | scopes.log:62只支持从ship进入design |

本轮检索原版common与生成effects：没有找到add_starbase_building_slot之类直接effect，也没有找到可现成add_modifier到Mother、恰好只加1建筑槽的原版static_modifier。原版实际槽数来自各ship_size.modifier。结论是**修改器字段存在且scope明确**，但“不改任何Mod定义即可保证加1槽”尚没有可核准方案。

### 3. 最小探针A：不改Mod的零容量setter边界

只在独立原生功能分支，保存before；所有country起点显式包在root，避免控制台选中Mother导致Current=fleet的错误scope。此类调用scope错误是探针错误，不能记作Mod运行时错误。

```text
effect root = { event_target:eep_mothership@this = { starbase = { set_starbase_building = { slot = 1 building = arkship_armor } } } }
```

随后原生保存，不先叠加rebuild或更换design；检查是否有slot错误、是否真实出现建筑，记录Mother和control舰船三防及完整设计。若setter拒绝零容量slot，停止这一分支并保留失败日志，不重复强插更大槽号。

优先armor而非shield：LARGE_ARMOR_1原版power=0、ship_armor_add=900（变量文件:253），避免把新增盾供能不足误判成组件接口无效。当前pmm00国家实际只研究armor_1、shields_1，Mother基础装甲乘数为1.74；如果三件确实应用且其它条件未变，预期装甲上限额外 `3×900×1.74=4698`，即44787.6→49485.6。此数是待验证预期，不是已观察结果；若引擎自动解析更高tier或其它修正变动，需以实际design／组件解析记录重新核对。

原生移除命令（先移建筑，再移容量修正）：

```text
effect root = { event_target:eep_mothership@this = { starbase = { remove_starbase_building = { slot = 1 building = arkship_armor } } } }
```

### 4. 最小探针B：下一隔离fixture的+1槽

以下仅是未来夹具设计，本次**没有创建这些Mod定义**。需要先给独立夹具定义一项已命名静态修正，再通过现有原生effect应用；生产eep_mothership基础修正不改，普通juggernaut全局定义不改。

```text
eep_probe_one_building_slot = { starbase_building_capacity_add = 1 }
```

运行原生命令，先只加槽并保存，确认slot增加本身没有改变三防／设计／队列：

```text
effect root = { event_target:eep_mothership@this = { starbase = { add_modifier = { modifier = eep_probe_one_building_slot days = -1 } } } }
```

再运行探针A的set_starbase_building命令。若有槽且建筑存在仍无装甲变化，第三个区分性夹具应定义Mother专用、无is_arkship_starbase门槛、仅equipped_component=LARGE_ARMOR_1的建筑，再安装到同一槽；不能把原版建筑的potential拒绝与整个building物化链失效混为一谈。

通过后一件、移除、再安装、两槽同类、同日重载逐步验证；capacity=2时用两个不同字面slot，先不要假设slot参数可接受变量。生成文档写slot=<int>，本轮已查到的原版实际调用均为固定数字；动态slot变量／script value和无限增长的性能边界仍需另测。

### 5. 设计升级与runtime数据层

**已确认接口边界**：`set_auto_upgrade_components=yes`支持design scope；原版 `grand_archive_effects.txt:9` 实际先create_ship_design，再在last_created_design设置自动升级，最后add_ship_design给country。它是沿已有组件的upgrades_to／科技链升级，并没有任意增加槽位或超越最高定义tier的承诺。Mother目前是is_event_design=yes、创建时upgradable=no、fleet.can_upgrade=no，三项不是同一层。

该开关本身不证明已存在舰船会即时完成物理换装；必须另查实际ship design引用／组件体和运行时属性，不能将设计flag变化当作已换装成功。

`set_fleet_settings`的生成文档明确：未写出的settings会恢复默认。因此单独 `can_upgrade=yes` 会意外改变其它舰队限制；若未来对照测试，必须完整重述现有settings并保留before/after，不能据舰队按钮变化宣告已修改ship.upgradable或设计的event属性。未发现原生set_ship_upgradable或set_event_design_flag effect。

本轮真实SAV显示三个独立层：①ship_design的growth_stages／section组件及required列表；②starbase的modules／buildings／standalone_components和自己的design引用；③ship实例的section.weapon、坐标和三防缓存。既有光环探针只改变②standalone而①及③不变。building即使没有改①，也可能经其它station装备缓存改变③，所以验收既不能只看design不变就否定，也不能只看②列表增长就认定成功；需对应组件实际属性、武器实例或面板效果。未发现把任意component直接写入普通ship实例数据层的原生effect；不编辑SAV研究此层。

**推断／风险**：给固定事件design启用自动升级或启用fleet升级，可能触及所有引用同一个design对象的舰船；应先克隆独立design并核对引用范围。该路径即便成功也只能升级已定义tier，不能解释满级组件继续无限成长。此项留给其它组件研究，不在本页重复实现。

### 6. 公开作者源码交叉验证

查阅Gigastructures作者仓库，固定commit `436812fb3acd9dc7d6cb5e666268a3a1d8135aa7`。其自定义移动Starbase模块把模块、独立section、组件set连成实际代码链，证明作者在使用模块生成真实部件的路径；不能据此外推fixed event juggernaut支持相同链路。[模块定义](https://github.com/Pouchkinn-s-Gigastructures/Gigastructures/blob/436812fb3acd9dc7d6cb5e666268a3a1d8135aa7/common/starbase_modules/giga_arkship_modules.txt#L80)、[组件set](https://github.com/Pouchkinn-s-Gigastructures/Gigastructures/blob/436812fb3acd9dc7d6cb5e666268a3a1d8135aa7/common/component_sets/giga_arkship_component_sets.txt)、[真实section槽](https://github.com/Pouchkinn-s-Gigastructures/Gigastructures/blob/436812fb3acd9dc7d6cb5e666268a3a1d8135aa7/common/section_templates/giga_arkship_spinal_mounts.txt)。

该作者已读的giga_arkship_buildings与giga_starbase_buildings两份文件没有本次所需equipped_component例子，所以建筑路径的直接根据仍是本机原版方舟building与nomads_effects调用，没有用第三方综述或镜像替代原始技术来源。

| 公开原始文件（同一固定commit） | SHA256 |
| --- | --- |
| common/starbase_modules/giga_arkship_modules.txt | d2e7c3ee0ef8fa4394732b55aa99e0ff03576ac2d15d39cbe06d7b45c5c2c161 |
| common/component_sets/giga_arkship_component_sets.txt | 2784b2a4d3bc315b7532d1ad5823ca25769a3adc79f909444ec641c6c02381cb |
| common/section_templates/giga_arkship_spinal_mounts.txt | de5bca17ab9d0d68332ec1bd3af384afa13cf7dc7baeb05f23902125c628f864 |

### 7. 本机原始证据哈希

游戏文件根目录 `C:\SteamLibrary\steamapps\common\Stellaris\`；engine文件根目录为上文精确run的script_documentation。

| 原始文件 | SHA256 |
| --- | --- |
| common/starbase_modules/00_example.txt | c290af5f9f2d785803cb3ad843573e3fc31822f937382d8730948cdc7ad3282e |
| common/starbase_buildings/00_arkship_component_buildings.txt | aabfd1e024572c1783c452d3a1cb29a9707850aa0ad898c3446ef03e4d1e83c5 |
| common/scripted_effects/nomads_effects.txt | b42b9f72f341e1e1a6bb624cf5d438677893c1e47bc0f4040844f15ac5e7ba96 |
| common/ship_sizes/18_juggernauts.txt | 3402b13978de2bbcc36c6d4eedab9e4a9ac7f5160183fa2b908029f10842f11f |
| common/ship_sizes/00_starbases.txt | bf3719e954596118f046f49f4b672b0e1f88d11c192bd179170a651d12c1f1ce |
| common/starbase_levels/01_juggernauts.txt | 13aa6b5590fcd479dc87fef2eabea3d691cab0f17affde2b1e512f0f9fe0883d |
| common/component_templates/00_utilities.txt | cd8a9a20f856d6abb6fdb98636cfb5dcda471f25d4ed757d46a668f95d0fa254 |
| common/scripted_variables/02_scripted_variables_component_cost.txt | d2b035df63e70f0ae970f03c06c70ee6b6f52ef372e049b6c69a50517d183d07 |
| engine/effects.log | d8ae346be74784474015d9a1cff474302ab98c59065c46d25c842553c3af6f44 |
| engine/scopes.log | 26e06ad465f02482f8efe344b3456dfd6aca0102c31e3bb1ef2d7796ee15186f |
| engine/modifiers.log | 37d3ddd98669c96b9598bf654d07f3ee8e296b1d126d20e14cb1d30077c7a3f2 |

### 8. 探针验收与当前结论

每步保留真实before／after／reload SAV、receipt、audit、操作action、日志与简中面板；核对Mother身份／位置／原设计44组件／跃迁／十船坞／已付款队列保留，普通ship1～5不受影响。新增装甲出现后，还要移除建筑确认相同属性增量回退，再做同类第二槽与重载，才足以确认真实组件链路和叠加。

目前建筑／模块链路**尚未实测**。已有standalone／BULWARK／rebuild探针未见收益，仍不足以关闭building直接装备路线。建议先做零容量setter边界，再在必要的隔离fixture中加1槽并移除原版potential门槛；module整设计重建和启用普通升级因风险更高排在后面。本页没有宣布动态真实组件不可行，也没有用随机普通modifier替代用户要求。
