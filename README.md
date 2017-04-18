# taoman
基于网络查询的快速子域名收集工具

    主要是为了快速收集 https://src.edu-info.edu.cn 平台的学校子域名写的一个小工具.

data 目录:  

    根据网络查询收集的平台上学校的 10 万左右域名,过滤出的域名元数据与简单统计的数据.
    可用 pydictor 的 -tool counter 功能,结合自己需求,筛选data目录内元数据的高频域名单词, 作为针对教育行业子域名爆破的爆破字典.


```
edusrc_SLD_name_raw_list			常用二级域名单词元数据
edusrc_SLD_top_1000				1000个最常用的二级域名单词
edusrc_SLD_top_3000				3000个最常用的二级域名单词
edusrc_SLD_unique_name			去重后的所有二级域名单词

edusrc_MLD_name_raw_list			常用多级域名单词元数据
edusrc_MLD_top_300				300个最常用的多级域名单词
edusrc_MLD_top_600				600个最常用的多级域名单词
```