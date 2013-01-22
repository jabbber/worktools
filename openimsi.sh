#!/bin/bash
cat <<HEAD
大家好！<br><p class="MsoNormal" align="left" style="line-height:12.75pt;text-indent:24pt">附件是昨天的openimis报表的汇总，其中有以下问题需要个位系统管理员关注
一下，其中有些数据可能与openimis未同步，还是请管理员确认一下，以免出错。</p>
HEAD
echo "1)日常检查异常统计，请各位管理员关注自己的系统。<br/>"
${0%/*}/readxlsx.py $1/开放平台开放平台日常检查异常统计表*.xlsx 1

echo "2)开放平台报警系统管理员后续处理跟踪。<br/>"
${0%/*}/readxlsx.py $1/开放平台开放平台报警系统管理员后续处理跟踪表*.xlsx all

echo "3)"
${0%/*}/readxlsx.py $1/开放平台开放平台操作系统定义作业变化情况统计表*.xlsx 0

cat <<FOOT
<div><font color="#000000">Best Regards,</font></div>
<div> </div>
<div><font color="#000000"><span>周文君<br>Jabber Zhou</span></font><br>  </div>
</div>
<div><font color="#000000">深圳市傲冠软件股份有限公司             <font color="#c0c0c0">        服务中心</font></font><font><font face="Verdana"><font color="blue" face="宋体"><span style="font-size:10pt;color:blue"><br>
</span></font></font></font><font color="#000000"><span>Shenzhen Skybility Software Co.,Ltd.</span></font><font><font face="Verdana"><font color="blue" face="宋体"><span style="font-size:10pt;color:blue"></span></font></font></font><br>
</div>
<div><font color="#000000">--------------------------------------------------------------</font></div>
<div><font color="#000000">Address:深圳市南山区科技中二路深圳软件园二期14栋501-502   </font></div>

<div>

<div><font color="#000000">Tel:0755-88308830
Fax:0755-88308955  Mobile:<a value="+13602652035">18665380021</a><br>Email:<a href="mailto:zwj@skybility.com" target="_blank"> zwj@skybility.com</a>
 MSN：<a href="mailto:mayjabber@gmail.com" target="_blank">mayjabber@gmail.com</a></font></div></div></div>
FOOT
