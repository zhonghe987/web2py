function getRule(data){
    //alert(ele);
    var g,d,s;
    g = data["LC"];
    s = "";
    for(var i=0; i<g.length; i++){
        s += '\t'+'规则组'+(i+1)+'\n';
        for(var o in g[i]){
            s += '\t\t'+ele[o]+' : '+g[i][o]+'\n';
        }
    }
    d = data["FQ"];
    if(d){
        s += '\n\t频次: 大于，等于 '+d+' 次';
    }
    return s;
}

function show(obj){
    var tr = $($(obj).parents("tr")[0]);
    var td = $(tr.children()[1]);
    //alert(td.html());
    $("#showLabel").text("标签："+td.text()); 
    $("#showModal").css("display", "block");
    $("#showDesc").text(tr.attr("desc"));
    var j = JSON.parse(tr.attr("json"));
    $("#showRule").text(getRule(j));
}

function showRule(){
    var tr,td,r, tds, pre, d;
    tr = $("#tblTag").children();
    for(var i=0; i<tr.length; i++){
        td = $($($(tr[i]).children()[4]).find("label")[0]);
        //alert(td.text()););
        if(td.text()=="active"){
            td.text("激活")
        }else{
            td.text("未激活");
        }
        td = $($(tr[i]).children()[2]);
        d = JSON.parse(td.text());
        td.text(d.FQ);
    }
}

function createRow(i, j, row){
    var tr,td, a, d,p, l;
    tr = $('<tr align="center"></tr>');
    tr.attr('desc', row.tagDesc);
    tr.attr('json', row.json);
    td = $("<td></td>");
    td.append(j);
    tr.append(td);
    td = $("<td></td>");
    td.append(row.name);
    tr.append(td);
    td = $("<td></td>");
    d = JSON.parse(row.json);
    td.append(d.FQ);
    tr.append(td);
    td = $("<td></td>");
    td.append(row.createDate);
    tr.append(td);
    td = $('<td align="left"></td>');
    td.attr("id", row.id);
    td.attr("initStatus", row.status);
    td.attr("finStatus", row.status);
    d = $('<div class="radio"></div>');
    p = $('<input class="icheck" type="checkbox">');
    l = $('<label></label>');
   if(row.status == "active"){
       p.attr("checked","");
       l.text("激活");
    }else{
        l.text("未激活");
    }
    d.append(p);
    d.append(l);
    td.append(d);
    tr.append(td);
    td = $("<td></td>");
    a = $('<a>查看</a>'); 
    a.attr("href","#");
    a.click(function(){
        show(this);
    });
    td.append(a);
    td.append('&nbsp;');
    a = $('<a>编辑</a>'); 
    a.attr("href", urlEdit+'?id='+row.id);
    td.append(a);
    td.append('&nbsp;');
    a = $('<a href="#" data-toggle="modal" data-target="#dlgDel">删除</a>');
    a.click(function(){
        change(row.id,row.name,j-1, i)
    });
    td.append(a);
    tr.append(td);
    return tr;                
}

function getPaginationInfo(page, postUrl){
    //alert('get pagination info');
    $.ajax({type: "post",
        url: postUrl,
        data: {'page':page,
                    'channel':jQuery("#tblContent").attr("channel"),
                    'area':jQuery("#tblContent").attr("area")
                   },
        dataType: "json",
        success: function(data){//成功时执行函数
            tbl = jQuery("#tblTag"); 
            tbl.children().remove();
            jQuery("#tblContent").attr("ids",data.con);
            var tr, c;
            for(var i=0, j=data.startId; i<data.data.length; i++,j++){
                tr = createRow(i, j, data.data[i]);
                tbl.append(tr);
             }
             $("input.icheck").iCheck({checkboxClass: 'icheckbox_flat-grey'});
             $("#tblTag ins").unbind('click');
             $("#tblTag ins").click(function(){selectIns(this)});
             c = $("#checkAll").next();
             c.parent().removeClass("checked");
             c.prev().attr("status", "");
             c.unbind('click');
             c.click(function(){selectIns(c)});
        }
    });
}

function selectIns(obj){
    var o = $(obj);
     //alert(o.parent().html());
    var t, s, ins, m, v, td;
    var p =o.prev()
    if(p.attr("id")){
        if(p.attr("status")=="checked"){
            t = "未激活";
            s  = "not active";
            p.parent().removeClass("checked");
            p.attr("status", "");
        }else{
            t = "激活";
            s = "active";
            p.parent().addClass("checked");
            p.attr("status", "checked");
        } 
        ins = $("#tblTag ins");
        for(var i=0; i<ins.length; i++){
             m = $(ins[i]);
             if (s == "active"){
                 m.parent().addClass("checked");
             }else{
                 m.parent().removeClass("checked");
             }
             m.parent().next().text(t);
             $(m.parents("td")[0]).attr("finStatus", s);
         }
   }else{   
      td = $(o.parents("td")[0]);   
      if(td.attr("finStatus") == "active"){
          o.parent().next().text("未激活");
          td.attr("finStatus", "not active");
          o.parent().removeClass("checked");
      }else{
          o.parent().next().text("激活");
          td.attr("finStatus", "active");
          o.parent().addClass("checked");
      } 
   }
}

function statusUpdate(postUrl){
    //alert("update");   
    var tr = $("#tblTag>tr");
    var d = [];
    var td, s, e;
    for(var i=0; i<tr.length; i++){
         td = $($(tr[i]).children()[4]);
         s = td.attr("finStatus");
         if( td.attr("initStatus") != s){
             td.attr("initStatus", s);
             d.push([td.attr('id'),s]);
         }
     }
     //alert(d.length);
    if(d.length>0){
        $.ajax({
            type: "post",
            url: postUrl,
            data: {"data":JSON.stringify(d)},
            dataType: "text",
            success:function(msg){
                 //jQuery('#cancel').click();
             }
        }); 
    }
}

function delTag(id, num, row){
    //alert(id+' - '+num);
    tbl = $("#tblTag");
    $.ajax({
            type: "post",
            url: urlTagDel,
            data: {"id":id,
                          "num":num,
                          "pageCount": tbl.attr("pageCount"),
                          "tagName": tbl.attr("tagName"), 
                          "status":tbl.attr("status")
                        },
            dataType: "json",
            success:function(msg){
                 //alert(JSON.stringify(msg));
                 var tr = $(tbl.children()[row]);               
                 var trLst = tr.nextAll();
                 var a, c;
                 for(var i=0; i<trLst.length; i++){
                     a  = $($(trLst[i]).children()[0]);
                     a.text(parseInt(a.text()) - 1)
                 }
                 tr.remove();
                 if(msg.count>0 && msg.data != ""){
                     for(var i=0, j=msg.num; i<msg.data.length; i++,j++){
                         tr = createRow(i, j, msg.data[i]);
                         tbl.append(tr);
                     }
                     $("#tblTag ins").unbind('click');
                     $("#tblTag ins").click(function(){selectIns(this)});
                     c = $("#checkAll").next();
                     c.parent().removeClass("checked");
                     c.unbind('click');
                     c.click(function(){selectIns(c.prev())});
                 }
                 tbl.attr("pageCount", msg.pageCount);
                 $(".dataTables_info").text("共 "+msg.count+" 条信息");
                 $("#tagPaginate").children().remove();
                 $("#tagPaginate").pagination(msg.pageCount, 1, options);
                 var li = $("#tagPaginate li");
                  $(li[0]).removeClass("active");
                  for(var i=0; i<li.length; i++){
                      a = $($(li[i]).children()[0]);
                      if (a.text() == msg.page){
                           a.parent().addClass("active");
                          break;
                      }
                  }
             }
        }); 
}

function tagDown(postUrl, taskProgressUrl){
    //alert('tag down');
    var bCancel = false;
    jQuery("#downModalLabel").text("正在处理命令"); 
    jQuery("#downProgress").text("5%");   
    jQuery("#downProgress").attr("style", "width: 5%");
    jQuery("#cancelDown").click(function(){bCancel = true;});
    $.ajax({
        type: "post",
        url: postUrl,
        data: {},
        dataType: "json",
        success: function(data){
             //alert(data.taskId);
             jQuery("#downModalLabel").text("正在生成文件:"+data.filename);              
             if (bCancel){
                 return true
             }

             var t = setInterval(function(){
                 $.ajax({
                     type: "post",
                     url: taskProgressUrl, //"{{=URL('getTaskProgress')}}",
                     data: {"taskId":data.taskId},
                     dataType: "json",
                     success:function(msg){
                         //alert(msg.status);
                         jQuery("#downProgress").text(msg.progress);   
                         jQuery("#downProgress").attr("style", "width: "+msg.progress);
                         if(msg.status=="COMPLETED")
                         {
                             clearInterval(t);
                             setTimeout(function(){
                                 jQuery("#cancelDown").click(); 
                             },2000);
                             location="downFile?filename="+data.filename;
                         }
                     }
                 }); },2000); 

              jQuery("#cancelDown").click(function(){
                  clearInterval(t)
              });
        }
    });
}

function showEleDateStatus(){
    var tr,td, lbl;
    tr = $("#tblEleDate").children();
    for(var i=0; i<tr.length; i++){
        td = $($(tr[i]).children()[3]);
        lbl = $(td.find("label")[0]);
        if(lbl.text()=="selected"){
            lbl.text("激活")
        }else{
            lbl.text("未激活");
        }
    }
}

function selectDateIns(obj){
    var o = $(obj);
     //alert(o.parent().html());
    var t, s, ins, m, v, td;
    var p =o.prev()
    if(p.attr("id")){
        if(p.attr("status")=="checked"){
            t = "未激活";
            s  = "";
            p.parent().removeClass("checked");
            p.attr("status", "");
        }else{
            t = "激活";
            s = "selected";
            p.parent().addClass("checked");
            p.attr("status", "checked");
        } 
        ins = $("#tblEleDate ins");
        for(var i=0; i<ins.length; i++){
             m = $(ins[i]);
             if (s == "selected"){
                 m.parent().addClass("checked");
             }else{
                 m.parent().removeClass("checked");
             }
             m.parent().next().text(t);
             $(m.parents("td")[0]).attr("finStatus", s);
         }
   }else{   
      td = $(o.parents("td")[0]);   
      if(td.attr("finStatus") == "selected"){
          o.parent().next().text("未激活");
          td.attr("finStatus", "");
          o.parent().removeClass("checked");
      }else{
          o.parent().next().text("激活");
          td.attr("finStatus", "selected");
          o.parent().addClass("checked");
      } 
   }
   
   m = $("#eleDateSave");
   m.attr("disabled", "true");
   tr = $("#tblEleDate").children();
   for(var i=0; i<tr.length; i++){
       td = $($(tr[i]).children()[3]);
       if(td.attr('initStatus') != td.attr('finStatus')){
           m.removeAttr("disabled");
           break;
       }
   }
}

function save(postUrl){
   $("#eleDateSave").attr("disabled", "true");
   var tr = $("#tblEleDate").children();
   var d = [];
   for(var i=0; i<tr.length; i++){
       td = $($(tr[i]).children()[3]);
       if(td.attr('initStatus') != td.attr('finStatus')){
           d.push([td.attr('id'),td.attr('finStatus')]);
           td.attr('initStatus',td.attr('finStatus'));
       }
   }

    $.ajax({
        type: "post",
        url: postUrl,
        data: {'data':JSON.stringify(d)},
        dataType: "text",
        success: function(data){ //alert(data);
        }  
    });
}

function change(ids, album, num, row){
    $('button#sure').attr('values',ids);
    $('button#sure').attr('num',num); 
    $('button#sure').attr('row', row);
    var d = $("#dlgDel p").parent();
     d.children().remove();
     d.append('<p>确定删除&nbsp;&nbsp;<span style="color:red;">'+album+'</span>&nbsp;&nbsp;记录？</p>');
}
