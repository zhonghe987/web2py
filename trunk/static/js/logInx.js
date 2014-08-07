function getPaginationInfo(page, postUrl){
    //alert('get pagination info');
    $.ajax({type: "post",
        url: postUrl,
        data: {'page':page,
                    'startDate':$("#tblLog").attr("startDate"),
                    'endDate':$("#tblLog").attr("endDate")
                   },
        dataType: "json",
        success: function(data){//成功时执行函数
            //alert( "回调成功！"+data);
            tbl = jQuery("#tblLog"); 
            tbl.children().remove();
            var tr,td;
            for(var i=0, j=data.startId; i<data.data.length; i++,j++){
                tr = $('<tr align="center"></tr>');
                td = $("<td></td>");
                td.append(j);
                tr.append(td);
                td = $("<td></td>");
                td.append(data.data[i].createDate);
                tr.append(td);
                td = $("<td></td>");
                td.append(data.data[i].ip);
                tr.append(td);
                td = $("<td></td>");
                td.append(data.data[i].count);
                tr.append(td);
                tbl.append(tr);
             }
        }
    });
}