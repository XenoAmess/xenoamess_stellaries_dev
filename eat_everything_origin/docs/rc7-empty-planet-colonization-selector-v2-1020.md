# Stellaris4.5.2空物理planet的殖民谓词与独立v2夹具

root实际纯日志A已证明ROOT→core2→solar_system(origin5)、every_system_planet共10对象及无条件random均有效。B实际03:39:35显示9个未殖民对象均通过is_colony=no、NOT(is_colony=yes)、NOT(is_under_colonization=yes)；而is_under_colonization=no只在已殖民core打印，9个空物理planet均不打印。当前C尚在执行，没有完整limit运行结果，不能仅凭B称创建修复或正常拆解已经通过。

该事实绑定当前Stellaris4.5.2／EXE SHA `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`，是空物理planet上这个具体trigger的行为；不能泛化所有布尔trigger、所有作用域、其他Paradox游戏或其他版本。生成scope文档仅登记允许作用域，无法证明对象缺失colony时`=no`与`NOT{=yes}`等价；此前只读候选报告只证明原生字段匹配，未获此engine谓词实测。A/B事实当前来自root交接摘录，原始probe闭合后再另行归档；旧失败包不改。

## 实施目标与范围（先于创建v2）

新建独立`testing/empty_planet_selector_v2_1020/`命令包，仅在既有命令的**未殖民候选选择器**中，将精确文本`is_under_colonization = no`替换为`NOT = { is_under_colonization = yes }`。保持原39与RC6 map原字节、原Mod、原工具、原SAVE不变，不加资源／科技／新验收要求。优先交normal owned_q2_setup v2；并准备guard绑定／七setup、home外uncolonized绑定／dispatch、Lithoid空球setup等同类实际执行命令。已殖民源上的readiness、neutral/ground等原有`=no`不在本修复范围，仍按原生状态验证。

每个v2命令保留原source path/SHA、原id、完整原command SHA、新command SHA和替换次数；只允许该单一片段变化，不能用v2文件替代旧失败证据。若命令包含混合已殖民与未殖民selector，必须逐scope分辨，不能全局字符串替换误改已殖民合同。旧未执行>1000字符大夹具不作为root执行建议，原split路线仍优先；v2新增命令亦须保持实际console长度边界。

新P夹具创建后先运行open_kaishek现成包级静态验收，PASS后才交root执行。静态通过只证明该工具当前声明的syntax/package边界，不证明scope运行或创建成功。C闭合后与A/B结合确认原limit根因；v2 actual run还须新alias、目标实体、恰50或既有指定pop、size／class／owner／无损耗、原账本未改变等原readiness，再接正常决议或guard路线。不会用B或静态PASS顶替这些实机条件。

## 生产调用只读审计

只读当前实际RC7 Mod路径及冻结同tree原文件，查相同trigger是否出现在未殖民候选选择中；报告命中及colony前提。即便发现需关注项，也只报告，不擅改RC7、版本或发布候选。

## C闭合与证据收件设计

root随后明确r7normalprobe-*全部闭合、worker EXIT0，并交接36份固定操作／原图OCR／摘录文件；C实际03:40:14为K0=9、R0=10、完整PASS及RANDOM_PASS均0。现在只读这些精确probe前缀，不读后续normal新stem。另建`evidence/1019-rc7-empty-selector-probe-v1`封存36原件、逐命令输入/Enter匹配、摘录逐marker与对象集合交集、v2单片段差异及实际Kaishek输入绑定。保留原摘录v1/v2；它们由root从活动原生日志主动摘取，仅为诊断摘录，不冒充最终停机完整日志。

v2命令已生成并实际Kaishek EXIT0、2/2 P解析PASS；normal为683字符（替换片段长度差11），完整包16条，每条只有一个片段替换，两个已有殖民首都选择器不改。初次生成脚本因预估字符差误写14的断言在写文件前退出，按实际片段长度11复核后生成；原源码与生产Mod不受影响。全包只有旧colonizing_setup仍超过1000，保持不推荐执行；旧lithoid_q2_setup虽修空球谓词，仍因无既有损耗不用于本轮，继续用r6_lithoid_loss_setup v2。

静态工具报告本身只给结果汇总，因此另在新证据包记录实际调用参数、输入P/descriptor/VERSION SHA、CLI及工具源SHA与输出report SHA，避免同结果汇总字节相同被误认为未区分两个输入包。旧purelog三probe静态报告与本v2静态报告恰因相同汇总内容SHA相同，输入由各自命令／source及调用绑定区分；这不是运行语义认证。

## 独立收件结果

已双读复制36份闭合原件，实际三条命令逐字匹配纯log包且均有物理Enter。v2摘录83行，原摘录v1逐行是其前缀，均原样保留。独立计数为：A ROOT／CORE_EXISTS／CORE／SYSTEM／RANDOM／END各1、EACH10；B C0=9、CN=9、UN=10、A0=10、S0=9、U0=1；C K0=9、R0=10、PASS=0、RANDOM_PASS=0。

U0唯一对象是EEP-Core，与C0九对象集合完全不相交。原完整limit交集为空；把U0换UN后，与非星、非人工、非core、非reserved相交得到8个对象。因此原选择器被空物理planet的`is_under_colonization=no`排空，scope link、对象数量和其余各谓词不是本次根因。该结论不延伸为所有布尔写法的共性规则；不需要更改CK3方言文档。

已只读实际repository_mod与运行中copied_mod，每份59个文件全部匹配固定RC7 manifest。两处生产命中仅`common/scripted_triggers/eep_triggers.txt:54`的eep_source_valid及`eep_planet_killer.txt:13`的eep_colossus_target_valid，二者均显式先要求is_colony=yes。因此本次空候选缺陷不要求更改RC7生产文件；没有热改运行目录。

16个v2包括normal1、guard count绑定及七setup共8、colonizing旧整串及reserve/start split共3、旧与当前Lithoid setup共2、uncolonized bind/dispatch共2。两个原colonized enemy/neutral首都选择器保持原字节。`execute_in_current_route`只标可用性，不要求添加原路线未用的batch_split_bind；root仍可沿已有state_guard_bind及split路线。uncolonized不但绑定需v2，其dispatch前的空球readiness也要用对应v2，才能实际发出无效目标callback，避免未dispatch而误判拒绝。

normal静态单命令[normal-command-v2.json](../testing/empty_planet_selector_v2_1020/normal-command-v2.json) SHA `2e8835c8c5262e525b0e1578993ef0bef39b9a19d296e714a4dd9938d2a26057`；完整[commands-v2.json](../testing/empty_planet_selector_v2_1020/commands-v2.json) SHA `7b90bc9d247b119f4ac66aac6771236b3cea64402defd95324bd5ffe2c38a99d`。原source逆替换逐字相等，Kaishek静态实际输入P／元数据／工具／CLI／report绑定在独立分析中，未将相同结果汇总SHA当输入相同。

- [probe index](evidence/1019-rc7-empty-selector-probe-v1/index.json)：`e9531c43507c2a4674e73ce4f2c82ebcdb971ae09297b705d32810a1497fa49a`
- [probe verify](evidence/1019-rc7-empty-selector-probe-v1/verify.json)：`07c011d264b3278476a7e2afef9518c41463c928d04ac2bfe67d8e2485e3a61c`，13/13，限定PASS_BYTES_ENGINE_CAUSE_AND_V2_STATIC_ONLY。
- [分析及实际静态调用绑定](evidence/1019-rc7-empty-selector-probe-v1/authored/analysis-v1.json)：`08550160a5d1ab20fa87119b88f2073aa1066d29d46588bc9a31350617790329`。

封口共38payload／1,420,099字节、7组图/OCR、19项canonical引用；整个probe包42文件。可stage本文、probe包全42文件、独立v2测试目录全5文件、v2 Kaishek报告1文件，共49文件。后续v2实际setup动作、normalready2与normal运行由另包接收；本文与本包仅证明原缺陷及v2静态准备，未读取这些后续活动新stem。
