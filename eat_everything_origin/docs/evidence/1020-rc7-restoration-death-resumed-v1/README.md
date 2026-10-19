# RC7 真实受伤恢复与母舰死亡

简体中文、单生产Mod，run `20261019T204055Z`。before高档引用独立ordinary-control
封包，不再复制。Mother125/ship809，C20500、L2050、R410/P0、六tier均非零。

Aug7仅执行原正伤害命令后先原生保存hurt：舰体和装甲各真实减少100000，
Mother身份、三项max、账本和六层数不变。hurt护盾当前字段被省略，原样保留
present=false；最初直接索引造成的KeyError发生在FF前，未重复伤害，未伪造0。
仅FF1到Aug8，实际舰体+18094.76、装甲+29849.576，无修复输入或订单，身份、
max、账本和六层数不变，原growth通过。不据此拟合闭源恢复率或声称数值护盾差。

Aug8真实destroy后调用原完整initialize/startup/sync，FF24跨Sep1月脉冲另存Sep2；
真正从主菜单载入这份已毁档，再完整初始化、FF1另存Sep3。两档全局实际舰船
和国家所属列表均无替代Mother，原125/809不在所属表，绑定不指向新活舰。
国家/core存活、grant flags齐全；C/L/R/P和六tier历史保持，snapshot_state=1。
没有调用要求活Mother的growth reader去读取死亡after。

235原件共12,697,606字节，四份SAV和49对GPU/OCR全部通过稳定字节、ZIP及
audit/receipt绑定检查。原strict、字段缺失及失败事实保留。仅支持daily_regeneration
与destroyed_mother_not_respawned两项，最终完整日志及整组验收仍PENDING。
