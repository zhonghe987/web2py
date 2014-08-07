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
            tbl = jQuery("#tblContent"); 
            tbl.children().remove();
            jQuery("#tblContent").attr('ids',data.con);
            var tr,td;
            for(var i=0, j=data.startId; i<data.data.length; i++,j++){
                  tr = $('<tr align="center"></tr>');
                td = $("<td></td>");
                td.append(j);
                tr.append(td);
                td = $("<td></td>");
                td.append(data.data[i].album);
                tr.append(td);
                td = $("<td></td>");
                td.append(data.data[i].channel);
                tr.append(td);
                td = $("<td></td>");
                td.append(data.data[i].area);
                tr.append(td);
                td = $('<td></td>');
                a=$('<a>编辑</a>');
                a.attr('href','conEdit'+'?ids='+data.data[i].c_id);
                td.append(a);
                td.append('&nbsp;&nbsp;');
                a=$('<a>删除</a>');
                a.attr('href','#');
                a.attr('data-toggle','modal');
                a.attr('data-target','#dlgDel');
                a.attr('onclick','change('+data.data[i].c_id+','+"'"+(data.data[i].album)+"'"+')');
                td.append(a);
                tr.append(td);
                tbl.append(tr);
             }
        }
    });
}

function downContent(obj){
    //alert('down content')
    var bCancel = false;
    jQuery("#downModalLabel").text("正在处理命令"); 
    jQuery("#downProgress").text("5%");   
    jQuery("#downProgress").attr("style", "width: 5%");
    jQuery("#cancelDown").click(function(){bCancel = true;});
    $.ajax({
        type: "post",
        url: urlContentDown,
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
                     url:urlGetTaskProgress,
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

function clearTimer(timer){
    //alert("timer.length: "+timer.length);
    for(var i=0; i<timer.length; i++){
         clearInterval(timer[i]);
    }
    timer.length = 0;
}

function change(ids,album){
    $('button#sure').attr('values',ids);
    var d = $("#dlgDel p").parent();
     d.children().remove();
     d.append('<p>确定删除&nbsp;&nbsp;<span style="color:red;">'+album+'</span>&nbsp;&nbsp;记录？</p>');
}
