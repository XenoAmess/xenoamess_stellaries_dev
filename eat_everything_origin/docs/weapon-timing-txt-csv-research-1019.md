# 1019 武器时间：原生TXT字段与CSV加载范围调查

## 目标与证据边界

RC3专属武器CSV写入与原版相同的90日windup／30日cooldown，但主线程原生受控下令从3月7日至10日已经完成且收益一次，疑似任意命名CSV未被游戏加载。暂停新成长live；本子任务仅只读调查原版4.5.2文档、官方原始说明与主流Mod作者仓库，记录现代TXT时间字段的准确结构和原始用例，以及CSV文件名加载证据。

不改Mod、工具、既有报告或桌面。优先寻找仅修改专属组件TXT的方案，避免覆盖整份原版 `weapon_components.csv` 引发兼容冲突。文档字段存在、作者源码存在、解析通过与本轮真实时间生效属于不同证据层，不能互相冒充；单位、planet_killer适用与任意CSV加载规则没有原始证据时保留未知。

## 原始来源与结果

调查日期为2026-10-19。本机原版4.5.2的 `stellaris.exe` SHA256为 `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。

| 来源 | 定位与摘要 | SHA256 |
| --- | --- | --- |
| 本机 `common/component_templates/000_documentation.txt` | 138—144行区分CSV常见数值与TXT，并列出 `windup`、`total_fire_time`；152—153行明确TXT伤害可用min/max块或标量，省略默认1 | `f9c0edfee06c59422609c04030e890afeb824055deeee18507315d8acb875286` |
| 本机 `common/component_templates/weapon_components.csv` | 194行起原版planet_killer，384行MAW，时间均为min_windup90、max_windup0、cooldown30；MAW功耗0 | `a0d4b199ea51e59a600beab99046fad3c8a11a49ae39c8ace0aed73ebf6ff330` |
| 本机 `common/component_templates/mutation_weapon_components.csv` | 第二个原生专名CSV | `759fe5e7d82927b91c75838b37726bd1fd79d63f0be24bba428403734b032b72` |
| 本机 `common/component_templates/99_README_WEAPON_COMPONENTS_STAT_DOCS.txt` | 要求由ODS导出分号分隔、无文本分隔符的CSV；没有任意CSV文件名扫描承诺 | `ca8057cf1e41058b943422b2d47be709b584e57dc7fea2d2dbc3a28dd5ed4855` |
| Gigastructures作者仓库 `descriptor.mod` | Mod3.40.4 DEV，`supported_version="v4.5.*"`；这是作者声明的兼容范围，不是本项目实测结论 | `e46858326183fd74837b8bf043aeb4abbb4d69a54798304c92c902ef6b88eded` |
| Gigastructures `aeternum_components.txt` | 466—483行真实 `PLANET_KILLER_AETERNUM_SHROUD`，size/type均planet_killer，479—480行直接TXT时间 | `d2274c452717e1fb5b089e10480881d36804ebe64f0f26350ac780999b0d9256` |
| Gigastructures `blokkat_components.txt` | 830—847行GENERATOR时间20/20与20；850—870行HARVESTER时间5/5与20，均真实planet_killer | `068fb04724ab0e255dffe2aade3258a68fa27f8a04cf75c6d187c8538b190c1d` |
| Gigastructures `ehof_t2_components.txt` | 962—981行 `COMPOUND_HM_RESHAPER`，planet_killer，978—979行时间1/1与80.00 | `1585c4fe8bf602bf38c527aa67ab39ccac7da4c3fc96cb5e26d59257de32bed1` |
| CWTools作者schema `components_consolidated.cwt` | 516行windup为min/max浮点块，518行total_fire_time为浮点。属于校验器作者的语法合同，不能替代引擎实测 | `3e6e108a8953a159ea61d38f66909c785acf4ad5cc9de9b07ee6bba64545a7ba` |

Gigastructures原作者源码固定到commit `436812fb3acd9dc7d6cb5e666268a3a1d8135aa7`，链接如下，避免滚动main改变调查对象：[descriptor](https://github.com/Pouchkinn-s-Gigastructures/Gigastructures/blob/436812fb3acd9dc7d6cb5e666268a3a1d8135aa7/descriptor.mod#L1)、[Aeternum planet killer](https://github.com/Pouchkinn-s-Gigastructures/Gigastructures/blob/436812fb3acd9dc7d6cb5e666268a3a1d8135aa7/common/component_templates/aeternum_components.txt#L466)、[Blokkat planet killers](https://github.com/Pouchkinn-s-Gigastructures/Gigastructures/blob/436812fb3acd9dc7d6cb5e666268a3a1d8135aa7/common/component_templates/blokkat_components.txt#L830)、[Compound planet killer](https://github.com/Pouchkinn-s-Gigastructures/Gigastructures/blob/436812fb3acd9dc7d6cb5e666268a3a1d8135aa7/common/component_templates/ehof_t2_components.txt#L962)。短原文为：

```text
windup = { min = 30 max = 30 }
total_fire_time = 30
```

通过GitHub recursive tree（`truncated=false`）枚举该commit的 `common/component_templates/`，读取22个TXT／CSV候选文件；其中没有任何CSV。四个上述planet_killer都在其TXT定义中写时间，没有写damage或power。该事实支持“现代作者实际使用内联时间、无需另设CSV”的候选路线，不能证明本项目90/0数值已被引擎载入。其他普通武器也广泛使用相同结构，但结论不依赖把普通武器规则推广给planet_killer。

CWTools独立固定commit `99147efe8072b331005b50536762dcc0b8573224`：[schema原始文件](https://github.com/cwtools/cwtools-stellaris-config/blob/99147efe8072b331005b50536762dcc0b8573224/config/common/components_consolidated.cwt#L516)。它补充确认字段形状为 `windup={min=float max=float}` 与 `total_fire_time=float`，没有把windup标量90当成已证语法。

## CSV文件名证据的有限结论

独立读取本机EXE字节，发现两个完整NUL结尾路径字面量：

- 十进制偏移37569608：`common/component_templates/weapon_components.csv`。
- 十进制偏移37569848：`common/component_templates/mutation_weapon_components.csv`。

这与原版README、原版实际文件名相符。仅凭二进制字面量无法证明没有其他扫描路径，不能写成对整个引擎的穷尽逆向结论。本轮也没有找到官方明确保证任意CSV命名可用的原始说明。结合主线程报告的RC3实际3月7日下令、3月10日已完成，专属任意命名 `eep_weapon_components.csv` 不应再作为90/30成功载入的证据。没有错误日志同样不构成载入证明。

直接覆盖原生专名整份CSV虽可能进入已知读取路径，但会与其他同名覆盖Mod争夺同一个全量表；本次不建议采用。第二个mutation专名也属于原生全量表，不能作为无兼容代价的自定义命名空间。

## 互联网检索范围与排除项

完成了不同路径查询：`site.github.com Stellaris "planet_killer" "windup" "total_fire_time"`、`site.github.com "Stellaris" "windup = {" "total_fire_time"`、`site.forum.paradoxplaza.com "weapon_components.csv" modding`、`site.forum.paradoxplaza.com Stellaris "weapon_components.csv" "windup"`、`site.forum.paradoxplaza.com Stellaris modding "total_fire_time"`、`site.stellaris.paradoxwikis.com "weapon_components.csv"`。随后直接读取作者仓库树及完整源文件，而非依赖搜索摘要。

官方域 [Ship modding](https://stellaris.paradoxwikis.com/Ship_modding) 在本次浏览器访问返回Internal Error。搜索返回的Fandom镜像、Steam普通玩家答复、Reddit和转载资料只作为查找线索，不用于本次现代引擎结论。尤其普通武器tick换日、planet_killer日计时与CSV覆盖优先级没有在可访问官方原始页面得到核实，本报告不借镜像为其背书。未发现可访问的官方开发者贴直接回答任意CSV文件名规则。

## 最小修复候选与验收要求

最初由原生CSV推导的候选为 `windup={min=90 max=0}`；但作者planet_killer内联实例使用30／30，CSV的max0哨兵在TXT中没有直接实证。因此主线程最终选择RC4的 `windup={min=90 max=90}`、`total_fire_time=30`、`power=0`，明确固定上下界，避免原版全表覆盖。形状有同类原始源码依据，90／30实际日数仍须本机原生订单证明，不能只因schema接受数字就判定已生效。

若要求保留旧专属CSV的零伤害合同，还应显式 `damage={min=0 max=0}`（或原生文档允许的标量0）：省略字段的文档默认值为1，不能把“原作者planet_killer省略damage”误写成其默认0。该武器的planet_destruction回调是否独立于普通damage，仍由本项目原生实际结果约束。

候选需先通过修复后的open_kaishek载入来源合同，随后冻结新快照、简中原生重新启动并重新下令。以原生队列起始日、充能进度、发射阶段、实际完成日与单次收益、原始SAV SHA及组件真实设计字段组成证据；不要使用RC3旧任务状态或只看静态TXT替代。至少保存起始、充能中、充能后／发射中、完成四个阶段，并保留无提前收益证据。若固定90／90内联仍不生效，继续调查字段载入与原生单位，不修改最终时长预期迎合结果。本子任务未进行该运行时试验，未修改任何生产Mod或工具。
