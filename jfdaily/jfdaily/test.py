
import re

from bs4 import BeautifulSoup
string ='''
<div class="chengshi">
      <div class="chengshi_img">
      	<a href="/news/detail?id=81054" target="_blank" title="【观见】“清北浙交复”？眼花缭乱的大学排名背后，有一条可怕的“信息食物链”">
      		<img src="http://images.shobserver.com/news/240_150/2018/2/27/343bf7fc-8dd2-495f-a4b6-0a9ef7eb9586.jpg" />
      	</a>
      </div>
      <div class="chengshi_wz">
        <div class="chengshi_wz_h"><a href="/news/detail?id=81054" target="_blank" title="【观见】“清北浙交复”？眼花缭乱的大学排名背后，有一条可怕的“信息食物链”">【观见】“清北浙交复”？眼花缭乱的大学排名背后，有一条可怕的“信息食物链”</a></div>
        <div class="chengshi_wz_m">排名过多过滥，甚至曾惊动过领导层，呼吁高校理性看待，更在乎自身的底蕴和质量，而不是被五花八门的排名牵着鼻子走。但排名机构的生意，为何依然风生水起？</div>
        <div class="chengshi_wz_f">作者：周云龙   2018-02-27 17:46:05</div>
        <div class="chengshi_wz_f1">
            <div class="tu"><img src="/images/red_01.png" /><span style="position:relative;bottom:6px; left:3px;">(10)</span></div>
            <div class="dj"><img src="/images/red_02.png" /><span style="position:relative;bottom:6px; left:3px;">(1)</span></div>
            <div class="clear"></div>
        </div>        
      </div>
      <div class="clear"></div>
    </div>
    <div class="chengshi">
      <div class="chengshi_img">
      	<a href="/news/detail?id=78550" target="_blank" title="【观见】机关干部解密：为什么有些退居二线的“老领导”，能够堂而皇之“带薪养老”？">
      		<img src="http://images.shobserver.com/news/240_150/2018/1/30/dd66ad94-fdf9-419b-8ea3-e6c94af661ef.jpg" />
      	</a>
      </div>
      <div class="chengshi_wz">
        <div class="chengshi_wz_h"><a href="/news/detail?id=78550" target="_blank" title="【观见】机关干部解密：为什么有些退居二线的“老领导”，能够堂而皇之“带薪养老”？">【观见】机关干部解密：为什么有些退居二线的“老领导”，能够堂而皇之“带薪养老”？</a></div>
        <div class="chengshi_wz_m">新领导对老领导，本来就认定“不添乱就是帮忙”。为什么有这样的心态？还是因为在基层，“退二线”干部所任的“主任科员”“调研员”等职务太稀罕了。</div>
        <div class="chengshi_wz_f">作者：廖德凯   2018-01-30 11:52:02</div>
        <div class="chengshi_wz_f1">
            <div class="tu"><img src="/images/red_01.png" /><span style="position:relative;bottom:6px; left:3px;">(8)</span></div>
            <div class="dj"><img src="/images/red_02.png" /><span style="position:relative;bottom:6px; left:3px;">(4)</span></div>
            <div class="clear"></div>
        </div>        
      </div>
      <div class="clear"></div>
    </div>
</div>
'''