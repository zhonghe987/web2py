function initGroup(){
    var p = $('<div class="panel panel-solid-default border-02"></div>');
    var t = $('<div class="panel-heading"><div class="pull-right"><i class="fa fa-times" data-toggle="tooltip" data-placement="bottom" title="删除组"></i></div><h4 class="panel-title">规则组</h4></div>');
    var x = $(t.find('i')[0]);
    var d = $('<div class="panel-body"></div>');
    var sel = $("#selDimContent").clone();
    sel.attr("id","");
    sel.removeClass("hide");
    d.append(sel);
    d.append('<table class="table table-bordered"></table>');
    p.append(t);
    p.append(d);
    jQuery("#dimContent").append(p);
    x.click(function(){
        //alert(jQuery("#dimContent").children("div").length);
        if(jQuery("#dimContent").children("div").length > 1){
            p.remove();
        }
    });
   x.tooltip();
   return sel;
}

function showLcDlg(obj, mode){    
    var check, btnCheckCnl, sel, s, f, dlg, tbl, i, tr, td, t, o, p;
    if(mode == 'new'){
        sel = $(obj);
        s = $(sel.children("select option:selected")[0]);
        f = s.val()
        dlg = $("#LC");
        dlg.css("display", "block");
        $(dlg.find("#titleLbl")[0]).text("新增: "+s.text());
        $(dlg.find("label")[0]).text(s.text()+": ");
        $(dlg.find("textarea")[0]).val("");
        $(dlg.find("#info")[0]).text("建议进行检查");
        $(dlg.find("button")).unbind('click');
        btnCheckCnl = $(dlg.find("#btnChkCnl")[0]);
        $(dlg.find("#btnCnl")[0]).click(function(){
            dlg.css("display", "none");
            sel.val("");
            btnCheckCnl.click();
        });

        $(dlg.find("#btnSub")[0]).click(function(){
            dlg.css("display", "none");            
            tbl = sel.next();
            i = dlg.find("textarea");
            createLC(tbl, s, $(i[0]).val());
            s.remove();
            if(sel.children().length==1){
                sel.addClass("hide");
            }
            btnCheckCnl.click();
        });
        check = s.attr("check");
    }else{
        tr = $(obj).parent().parent();
        td = tr.children();
        dlg = $("#LC");
        dlg.css("display", "block");
        $(dlg.find("#titleLbl")[0]).text("新增: "+$(td[0]).text());
        $(dlg.find("label")[0]).text($(td[0]).text()+": ");
        $(dlg.find("textarea")[0]).val($(td[1]).text());
        $(dlg.find("#info")[0]).text("建议进行检查");
        $(dlg.find("button")).unbind('click');
        btnCheckCnl = $(dlg.find("#btnChkCnl")[0]);
        $(dlg.find("#btnCnl")[0]).click(function(){
            dlg.css("display", "none");
            btnCheckCnl.click();
        });

        $(dlg.find("#btnSub")[0]).click(function(){
            dlg.css("display", "none");            
            i = dlg.find("textarea");
            $(td[1]).text($(i[0]).val());
            btnCheckCnl.click();
        });
        check = tr.attr("check");
    }

    $(dlg.find("#btnChk")[0]).click(function(){
        t = $(dlg.find("textarea")[0]).val();
        o = $(this);
        if(t){
            $(dlg.find("#info")[0]).text("");
            $(dlg.find("textarea")[0]).attr("disabled", "disabled");
            o.addClass("disabled");
            p = $(dlg.find("#checkProgress")[0]);
            p.attr("style", "width: 10%");
            p.parent().removeClass("hide");
            btnCheckCnl.removeClass("hide");

            $.ajax({
                type: "post",
                url: urlContentCheck,
                data: {"check":check,
                            "data":t
                           },
                dataType: "text",
                success:function(msg){
                	//alert(msg);
                	var d;
                	if(msg != ""){
                		d =  "内容库不包括 (<span style='color:red'>"+msg+"</span>)"
                	}else{
                		d = "<span style='color:green'>通过</span>"
                	}
                	$(dlg.find("#info")[0]).append("检查结果: "+d);
                    btnCheckCnl.addClass("hide");
                	$(dlg.find("textarea")[0]).removeAttr("disabled");
                    o.removeClass("disabled");
                    
                	/*
                    //alert(msg);
                    var t = setInterval(function(){
                        $.ajax({
                            type: "post",
                            url: urlGetChechInfo,
                            data: {"taskId":msg},
                            dataType: "json",
                            success:function(msg){
                                //alert(msg.data);
                                p.text("正在检查中......");   
                                p.attr("style", "width: "+msg.progress);
                                if(msg.status=="COMPLETED"){
                                    clearInterval(t);
                                    p.parent().addClass("hide");
                                    btnCheckCnl.addClass("hide");
                                    var d;
                                    if(msg.data!='""'){
                                        d = "内容库不包括( "+unescape(msg.data.replace(/\\(u[0-9a-fA-F]{4})/gm, '%$1')+" )");
                                    }else{
                                        d = "通过"
                                    }
                                    $(dlg.find("#info")[0]).text("检查结果: "+d);
                                    $(dlg.find("textarea")[0]).removeAttr("disabled");
                                    o.removeClass("disabled");
                                }
                            }
                        }); },2000); 
                    */
                    btnCheckCnl.click(function(){
                        clearInterval(t);
                        p.parent().addClass("hide");
                        btnCheckCnl.addClass("hide");
                        o.removeClass("disabled");
                        $(dlg.find("textarea")[0]).removeAttr("disabled");
                    });
                }
            }); 
        }else{
            $(dlg.find("#info")[0]).text("没有内容");
        }
    });
}

function createLC(tbl, sel, value){
    var tr, td, a;
    tr = jQuery('<tr align="center"></tr>');
    tr.attr('symbol', sel.val());
    tr.attr('check', sel.attr('check'));
    td = jQuery('<td width="25"></td>');
    //td.attr("check", sel.attr("check"));
    td.append(sel.text());
    tr.append(td);
    td = jQuery('<td width="50"></td>');
    td.append(value);
    tr.append(td);    
    td = jQuery('<td width="25"></td>');
    a = jQuery('<a href="#" onclick="showLcDlg(this,\'edit\')">编辑</a>');
    td.append(a);
    td.append('&nbsp;&nbsp;');
    a = jQuery('<a href="#" onclick="delLcEle(this)">删除</a>');
    td.append(a);
    tr.append(td);
    tbl.append(tr);
}

function delLcEle(obj){
    tr = ($(obj).parents("tr"));    
    sel = $(tr.parents("div")[0]).children("select");
    if(sel.children().length == 1){
        sel.removeClass("hide");
    }
    opt = $('<option></option>');
    opt.val(tr.attr("symbol"));
    opt.attr("check", tr.attr("check"));
    opt.text($(tr.children("td")[0]).text());
    sel.append(opt);
    tr.remove();
}

function createTagRule(){
    var t, r, d, g, c, o;
    var dt = null;
    var lc = null;
    var lst = [];
    var tag = {};

    tag["TAG"] = $("#tagName").val();
    g = $("#dimContent").children();
    for(var i=0; i<g.length; i++){
         t = $($(g[i]).find("table")[0]);
         r = t.find("tr");
         if(r.length){
             c = {};
             for(var j=0; j<r.length; j++){
                 o = $(r[j]);
                 d = $(o.children()[1]);
                 c[o.attr("check")] = d.text();
             }
              lst.push(c);
         }
        
     }
     if(lst.length>0){
         tag["LC"] = lst;
         //alert(JSON.stringify(lc));
     }else{
         return 201;
     }
     
     tag["FQ"] = parseInt($("#actFeq").val());

   //alert(JSON.stringify(tag));
   return tag;
}

function save(checkUrl, postUrl, urlIndex, id){
    var t = $("#tagName").val();
     
   if(!t){
        return 101;
   }

    var r=-1;
    $.ajax({
        async:false,
        type: "post",
        url: checkUrl,
        data: {"name":t, 'id':id},
        dataType: "text",
        success:function(msg){
             r = parseInt(msg);
        }
    });

    if(r>0){
        return r;
    }


    tag = createTagRule();
    if(tag==201){
        return 201
    }

    $.ajax({
        type: "post",
        url: postUrl,
        data: {"name":$("#tagName").val(),
                     "desc":$("#desc").val(),
                     "status":$($("input.icheck").parent(".checked")[0]).parent().attr("status"),
                     "rules": JSON.stringify(tag),
                     "id":id
                   },
         dataType: "text",
         success:function(msg){
             window.location = urlIndex;
         }
    }); 
    return 0;
}

function checkFeq(obj){
    o = $(obj);
    v = o.val();
    if(v==""  || v < '1' ||  isNaN(v)){
        o.val(1);
    }else{
        o.val(parseInt(v));
    }
}