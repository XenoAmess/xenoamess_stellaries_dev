# RC7 普通舰完整负对照与高档新导出

简体中文、单生产Mod，run `20261019T204055Z`。真实载入原同银河C0及C20500
输入，分别原生另存r9growthlow/high，不调C或组件层数。

11艘普通舰0～5、804～808的实际所属、fleet、原生设计正文SHA和配置shape
相同，110个原生getter逐项一致且完整有限；三项最大耐久投影也一致。
包含民船和星基，不将其统称战斗舰。Mother125/ship809不在该负对照名单。

高档Mother十getter与三项native max由原C0-final来源公式事前预测，继续原
0.01及HP8ULP工程政策，全部通过；四个额外regen getter实际完整导出为0。
旧eep_probe_max_*缓存保持原样，不当作本次新导出或原生max。

167份原件共8,157,515字节，两份SAV和36对GPU/OCR及原件双SHA、稳定stat、
audit/receipt绑定均通过。source保存实际加载包装和预测工具原字节。
只支持ordinary negative control，不包含进行中的受伤、恢复、死亡或最终日志。
整组与component_rewards仍PENDING，原矩阵、来源模型和数值政策不改。
