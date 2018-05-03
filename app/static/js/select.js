/*
* 单位选择
* */
(function(window){
    var unit = {
        // 长度
        length: ["请选择","千米(km)","米(m)","分米(dm)","厘米(cm)","毫米(mm)","微米(um)","英寸(in)","英尺(ft)","码(yd)","英里(mi)","海里(nmi)","英寻(fm)","弗隆(fur)","里","丈","尺","寸","分","厘","毫"],
        // 面积
        area : ["请选择","平方千米(km²)","公顷(ha)","公亩(are)","平方米(㎡)","平方分米(dm²)","平方厘米(cm²)","平方毫米(mm²)","英亩(acre)","平方英里(sq.mi)","平方码(sq.yd)","平方英尺(sq.ft)","平方英寸(sq.in)","平方竿(sq.rd)","顷","亩","平方尺","平方寸"],
        // 体积
        volume: ["请选择","立方米(m³)","立方分米(dm³)","立方厘米(cm³)","立方毫米(mm³)","升(l)","分升(dl)","毫升(ml)","厘升(cl)","公石(hl)","立方英尺(cu ft)","立方英寸(cu in)","立方码(cu yd)","亩英尺","英制加仑(uk gal)","美制加仑(us gal)"],
        // 质量
        mass: ["请选择","千克(kg)","克(g)","毫克(mg)","吨(t)","公担(q)","磅(lb)","盎司(oz)","克拉(ct)","格令(gr)","长吨(lt)","短吨(st)","英担","美担","英石(st)","打兰(dr)","担","斤","两","钱"],
        // 温度
        temperature: ["请选择","摄氏度(℃)","华氏度(℉)","开氏度(K)","兰氏度(°R)","列氏度(°Re)"],
        // 压力
        pressure: ["请选择","帕斯卡(Pa)","千帕(kpa)","百帕(hpa)","标准大气压(atm)","毫米汞柱(mmHg)","英寸汞柱(in Hg)","巴(bar)","毫巴(mbar)","磅力/平方英尺(psf)","磅力/平方英寸(psi)","毫米水柱","公斤力/平方厘米(kgf/cm²)","公斤力/平方米(kgf/㎡)"],
        // 功率
        power: ["请选择","瓦(W)","千瓦(kW)","英制马力(hp)","米制马力(ps)","公斤·米/秒(kg·m/s)","千卡/秒(kcal/s)","英热单位/秒(Btu/s)","英尺·磅/秒(ft·lb/s)","焦耳/秒(J/s)","牛顿·米/秒(N·m/s)"],
        // 功/能/热
        work: ["请选择","焦耳(J)","公斤·米(kg·m)","米制马力·时(ps·h)","英制马力·时(hp·h)","千瓦·时(kW·h)","卡(cal)","千卡(kcal)","英热单位(btu)","英尺·磅(ft·lb)"],
        // 密度
        density: ["请选择","千克/立方厘米(kg/cm³)","千克/立方分米(kg/dm³)","千克/立方米(kg/m³)","克/立方厘米(g/cm³)","克/立方分米(g/dm³)","克/立方米(g/m³)"],
        // 力
        strength: ["请选择","牛(N)","千牛(kN)","千克力(kgf)","克力(gf)","公吨力(tf)","磅力(lbf)","千磅力(kip)"],
        // 时间
        time: ["请选择","年(yr)","周(week)","天(d)","时(h)","分(min)","秒(s)","毫秒(ms)"],
        // 速度
        speed: ["请选择","米/秒(m/s)","千米/秒(km/s)","千米/时(km/h)","光速(c)","马赫(mach)","英里/时(mile/h)","英寸/秒(in/s)"],
        // 字节
        bytes: ["请选择","比特(bit)","字节(b)","千字节(kb)","兆字节(mb)","千兆字节(gb)","太字节(tb)","拍字节(pb)","艾字节(eb)"],
        // 角度
        angle: ["请选择","角度制","圆周","直角","百分度(gon)","度(°)","分( ′)","秒(\")","弧度制","弧度(rad)","毫弧度(mrad)"],

        TYPE:[
            {mapping:null, name:"请选择"},
            {mapping:"length", name:"长度"},
            {mapping:"area", name:"面积"},
            {mapping:"mass", name:"质量"},
            {mapping:"temperature", name:"温度"},
            {mapping:"pressure", name:"压力"},
            {mapping:"work", name:"功/能/热"},
            {mapping:"density", name:"密度"},
            {mapping:"strength", name:"力"},
            {mapping:"time", name:"时间"},
            {mapping:"speed", name:"速度"},
            {mapping:"bytes", name:"字节"},
            {mapping:"angle", name:"角度"},
        ],

        choose: function(unit) {
            return this[unit];
        }
    }

    window.UNIT = unit;

})(window);