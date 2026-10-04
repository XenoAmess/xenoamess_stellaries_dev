# 反馈改版开发与程序性验证

日期：2026-10-04。用户已授权实施此前设计，限定只做开发与基本程序性验证，禁止启动游戏、抢占屏幕；要求提高并发。本记录先于代码修改建立，后续持续记录实施事实与验证证据。

## 目标与范围

以现有 0.1.3 为基线，实现初始局势月速 1、每次维护增加 0.25、每 100 实际维护员劳动力减速 0.25、最低月速 0.2；研究所基础社会学 3 与凝聚力 1；负面阶段惩罚减半；白绮社会学改正向且免自身凝聚力维护。保持起源预算 -6/+3、研究项目费用与复活成长合同。

奖励改为同层最多三选一，免费 reroll、同票据最多一次、三次实体选择冷却（含使用当轮确认）；候选、冷却和票据持久保存，结算幂等。两层有限池耗尽后每次奖励 R+1，旧四类迭代停止新增，旧效果保留，迁移重复部分仅一次。

所有正式物种特质按国内主体谱系真实人口加权计数，正负均计入，每层 5%，无限成长；机制名固定为「基于低内聚高耦合的旧时代集成服务架构」。优先实现能从本机引擎文档和源码确定的独立乘算渠道；静态证据不能证明运行时经济和 UI 已正确，不把加算或维护一并增加的渠道冒充目标。

合同来源：[整体设计](../../docs/shishan-code-origin-feedback-redesign-2026-10-04.md)、[特质机制](../../docs/shishan-code-origin-trait-synergy-design-2026-10-04.md)、[测试方案](feedback-redesign-test-plan-2026-10-04.md)、[详细用例](feedback-redesign-test-cases-2026-10-04.md)。本轮仅执行静态/程序性子项，实机、UI/OCR、自然局和存档运行回归保持 NOT RUN。

## 实施安排与文件边界

并行开发基础数值/领袖、特质统计/经济通道、程序性验证；奖励生成器、事件、成功凭证和最终集成由主任务负责。共享文件的修改顺序明确，避免并行覆盖；不提交用户未完成的 `console_history.txt`。候选版本使用 0.2.0-rc.1，仅修改本 Mod 的 VERSION、描述符和 changelog，不进行 Workshop 上传或发布标签。

所有正式语言补齐新增文本；运行时仍仅简体中文。完整名称采用本地化引用，长文本验收保留实际界面测试边界。生成产物与生成器同步修改，不能仅手改生成内容。

## 本轮验证与收口

先读取本机 `C:\workspace\open_kaishek` 使用说明并执行包级验收，工具缺陷按仓库规则先修复工具后继续。程序性验证覆盖数值边界、原始键/计数/迁移算术、候选唯一性和层优先、reroll 时序、结算凭证、资源与维护作用域、本地化键/编码/引用及完整名称。新增测试用于检查独立合同和负例，不仅复制生产实现。

记录实际工具版本、命令、退出码和 JSON 报告；保证测试命令无启动游戏、截图、输入、Steam 操作等副作用。必要测试失败后修复并重跑相关范围；未验证的引擎行为、UI 宽度或独立乘算可行性如实报告。最后更新设计的实施状态、整理证据，提交仅本任务文件并推送。

## 实施事实与结果

### 集成审查后的恢复边界

离线审查发现：成功凭证存在但事件尚未消费时，月度修复原来只阻止项目重开，会留下无法推进的凭证；维护成功后清理先完成，也会被当前重构状态拒绝。改为先恢复清理/维护/优化/复发凭证，再恢复缺失项目。维护和优化按真实成功凭证结算，不因当前状态变化丢失；存在未领取奖励时延后消费下一份凭证。优化仅在仍处于重构态时抽取复发。清理/复发已完成而残留对应凭证时，标记异常并清除，不重复执行状态转换。

另补国家持久化的唯一奖励窗口锁：授奖、重抽和决议统一经过同一开窗 effect；领取、稍后和重抽释放锁。正常入口无法为同一票据创建多个窗口，避免旧窗口消费下一张票据。月脉冲不清除窗口锁；游戏是否恢复存档中的弹窗仍属未执行的实机用例，不能用离线旗标检查宣称 UI 恢复通过。

复查补充：窗口打开后候选资格可能变化。确认或重抽的守卫拒绝时，游戏仍可能关闭事件窗口，因此两个入口先释放当前窗口锁，再判断是否可以消费。拒绝操作保留待领票据、候选和冷却，不计成功选择；首都决议可重新打开并刷新失效候选。增加守卫拒绝后的解锁/重开程序用例，避免资格变化导致永久无法领取。

### 经济通道的明确回退

本机原版脚本及引擎生成文档能确认岗位资源表的 `produces.mult`，但接入全国所有岗位需要覆盖原版/第三方岗位，且不能静态证明其包含 `_add` 基值。未找到可证实的全国岗位最终独立倍率；按岗位毛收入补发资源则会改变收入来源和 UI。本轮用户把独立乘算表述为「试试看最好能做成」，故当前 0.2.0-rc.1 明确采用原生 `planet_jobs_produces_mult` 的每特质 5% 加算候选，真正提供岗位收益且不修改维护。不执行大面积岗位覆盖或资源补发。

这是已说明的设计回退，不能登记原乘算用例通过。当前应用的增幅为 `B=0.05T`，与既有同类岗位修正加算；`M=1+B` 仅作为原独立目标的统计值，不在 UI 冒充实际全量产出比值。全文名称和玩家说明明确写「岗位产出加算」。独立乘算、实机实际比值及全资源来源回归仍未完成，后续需单独确定渠道和验收。本轮程序校验据当前加算合同检查范围与数值，保留原独立目标而不篡改其 PASS 条件。

原 0.1.3 包级 `open_kaishek` 基线检查通过（19 脚本全部解析、13 DDS、173 本地化键）；证据：`evidence/feedback-redesign/development-2026-10-04/baseline-open-kaishek.json`。当前候选代码已完成开发与程序性集成，最终结果在下方登记。没有启动游戏或屏幕操作。

### 当前候选的具体行为

- 初始月速 1、次数增速 0.25、全国实际维护员劳动力合计后每百减速 0.25、下限 0.2；岗位社会学 3、凝聚力 1。III/IV/V 的原有资源、武器、航速和岗位维护惩罚减半；项目、建筑费用及 -6/+3 预算保留。
- 白绮社会学改为 +5%+2.5%n、取消旧负面上限；工程学和付费复活成长流程保留。领袖自身 `leaders_unity_upkeep_mult=-1`，其它领袖不减免。此为自身 -100% 维护修正，存在其它正倍率时最终严格零维护仍未证明；不以其代替原豁免目标的通过结果。
- 候选取国内主谱系真实人口模板；先机械原版层、再兼容层，同层最多三个不同实体选项。免费重抽优先替换原组，N=4/5/6 分别最多替换 1/2/3 个；无替代项时禁用。每票最多一次，冷却 3，使用当轮确认计入，确认后 2→1→0，第四轮可用；耗尽后的自动层不推进冷却。
- 全部正式特质键均计数，包括正负、隐藏、偏好、身份和第三方；本实现没有新增物种簿记特质，例外集合为空。国内实际主谱系人口加权 U，历史/新重复层 R，T=U+R，当前原生岗位加算 B=0.05T。无覆盖人口时撤销修正、保留 R；失去起源时撤销本机制修正。
- 两层有限池耗尽后每次有效项目增加 R 一层，玩法无硬上限。旧四类 1% 迭代保留效果和原计数、停止新增，只迁移各自首层以外部分一次（7/5/11/4→23）。负数/非整数旧值记录异常，不静默取整；非整数正重复量可保留原精度。
- 新特质及清理/复发通过克隆模板迁移本国精确匹配的人口/领袖；共享旧模板保留，外国不在迁移范围。程序检查验证结构和抽象克隆夹具，原生迭代、飞升身份和实际迁移待实机验证。
- 首都新增查看架构与重开奖励决议；全名用于国家修正、详情与结果标题，起源说明引用完整机制名称和说明。十语言补齐，中文名完整保留 18 汉字/54 UTF-8 字节；字段截断、换行与遮挡未实测。

主事件、特殊项目回调和生成器同步修订；三份生成脚本及十语言奖励/兼容别名均由 `tools/shishan_code/generate_rewards.py` 生成。生成器不向正式 Mod 注入测试事件、预置计数或诊断经济补给。旧实机报告仅作历史证据，未把其 PASS 转记到新候选。

### 程序验证的边界

首道工具为 `C:\workspace\open_kaishek\tools\accept_stellaris_mod.py`，工具提交 `522ac2d93bd6c534a6a242a227057de40a8977c1`，依照其仓库说明执行；本轮工具无需修复、未修改工具仓库。游戏文件只读，EXE SHA-256 为 `6fe06709f265e726722dc23f617c5fc4e5557629e2d43fe312016aba547c83e4`。

离线合同检查器直接解释实际产物的有限 AST 子集，预期来自设计。候选抽取测试的资格事实为固定夹具，并另测真实资格 guard；模板克隆、局势变更、白绮刷新等引擎行为使用明确的抽象/opaque hook。未知语法报错，不把 hook 运行当作引擎执行。详见 [程序工具记录](feedback-redesign-programmatic-2026-10-04.md)。

本机 Stellaris 生成文档 `C:\Users\Administrator\Documents\Paradox Interactive\Stellaris\logs\script_documentation\effects.log` 再次核对：`add_modifier`（480—488）支持 `multiplier=<float>/<variable>` 与 country；`modify_species`（854—869）克隆新模板、支持 `change_scoped_species=no` 与结果 effect；`every_trait_of_species`（6092—6095）明确支持 pop_group，故可以在实际人口组计数。作用域和动态 modifier 参数按 Stellaris 文档使用，未将 CK3 特有格式推定为兼容。国内模板链、裸 `[Root.变量]` 本地化及领袖自身维护的证据另见架构/数值实施记录。这些是 Stellaris 方言的静态事实，不构成原生执行结果。

`evidence/feedback-redesign/development-2026-10-04/` 中 baseline 为旧包；candidate 和 programmatic-initial 为开发中快照，不能用于最终身份判断。最终证据只使用 `final-open-kaishek.json` 与 `programmatic-final.json`。完整 Mod 验收、TS-06 独立乘算、实机经济来源、长名 UI、存档读回和自然体验均未完成；九种非中文翻译运行时不在范围内。本任务完成开发及用户允许的程序验证，不宣告改版完整验收或正式发布。

### 最终执行证据

提交前发现 Windows 默认写入 CRLF，而 Git 按 LF 收录，导致同一语义的候选文件字节指纹不能跨检出复现。生成器固定 `newline="\n"`，候选文本统一 LF 后再次检查生成的 23 个文件逐字节一致，并更新最终包指纹和验证证据。此项只改变文本换行，不调整玩法、编码/BOM或本地化内容。

全部命令退出码 0。候选 `VERSION` 与 descriptor 均为 `0.2.0-rc.1`；正式 Mod 共 90 文件，LF 归一后检查器记录的 tree SHA-256 为 `230b87c89debfcf202ee47e7efc51cf5418e01ba8cb64734d935367097dfa696`。提交前逐文件核对验证目录与 Git 暂存区 blob 一致，包括原有 asset-manifest.json 的换行归一。

| 检查 | 结果与实际覆盖 | 证据 |
| --- | --- | --- |
| open_kaishek 包级入口 | PASS；25/25 P 脚本解析、13 DDS、268 本地化键、10 语言；syntax/package 范围，不是引擎完整语义。 | [最终包级 JSON](evidence/feedback-redesign/development-2026-10-04/final-open-kaishek.json) |
| 离线合同检查器 | 5 组 PASS；22 月速边界、12 费用样例、22 阶段资源键；U=9、部分覆盖至10.2、历史R=23仅迁一次、相邻10000/10001层差0.05；56个候选样例、3→2→1→0冷却、窗口锁及2个拒绝后重开、13个成功凭证恢复场景。 | [最终合同 JSON](evidence/feedback-redesign/development-2026-10-04/programmatic-final.json) |
| 程序回归及故障负例 | 32/32 PASS；错误月速/系数/取整、重复候选、错误冷却、历史双计、共享模板直接修改、维护污染、漏恢复/漏锁/拒绝后漏解锁、名称截断与本地化缺键等能被拒绝。 | [命令与原始输出](evidence/feedback-redesign/development-2026-10-04/verification-commands.json) |
| 既有奖励合同 audit | PASS；20 原版正面机械项及新产物候选/冷却合同，保持可调用旧入口。 | 同上 |
| 本地化 | 50 个 UTF-8 BOM 文件，每语言268键、2070别名引用、154脚本引用；原版引用已对本机游戏检查。全名18字/54字节静态完整；九种非中文翻译“静态校验通过”，运行时不在范围内。 | 最终合同 JSON |
| 生成与基本源码检查 | 23 个生成产物再次生成逐字节相同；4个Python源码compile通过；12份文档UTF-8及相对链接检查通过；git diff --check通过。 | 本记录及命令输出 |

实际主要复现命令从本仓库根执行：

```powershell
python C:\workspace\open_kaishek\tools\accept_stellaris_mod.py --mod C:\workspace\xenoamess_stellaries_dev\shishan_code_origin\mod --game 'C:\Program Files (x86)\Steam\steamapps\common\Stellaris' --version-file C:\workspace\xenoamess_stellaries_dev\shishan_code_origin\VERSION --report C:\workspace\xenoamess_stellaries_dev\shishan_code_origin\docs\evidence\feedback-redesign\development-2026-10-04\final-open-kaishek.json
python -X utf8 shishan_code_origin/tools/validate_feedback_redesign.py --mod shishan_code_origin/mod --game 'C:\Program Files (x86)\Steam\steamapps\common\Stellaris' --report shishan_code_origin/docs/evidence/feedback-redesign/development-2026-10-04/programmatic-final.json
python -X utf8 -m unittest discover -s tests -p test_shishan_feedback_redesign.py -v
python -X utf8 tools/shishan_code/audit_reward_contract.py --game 'C:\Program Files (x86)\Steam\steamapps\common\Stellaris'
```

开发结果和所允许的程序性验证已完成。没有启动 Stellaris、Steam、桌面窗口、截图/OCR或输入自动化；没有变更游戏安装/加载目录，没有 Workshop 发布。用户的 `console_history.txt` 保留原状，不进入提交。
