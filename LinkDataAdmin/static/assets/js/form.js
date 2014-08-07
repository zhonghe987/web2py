jQuery(document).ready(function(){
            jQuery('#no_table_dataSname').attr('class','form-control form-input');
            jQuery('#no_table_dataSname').attr('type','text');
            jQuery('#no_table_cookiedom').attr('class','form-control form-input');
            jQuery('#no_table_cookiedom').attr('type','text')
            jQuery('#no_table_source').attr('class','form-control input-sm form-input');
             jQuery("#no_table_source option:first ").remove();
             //jQuery('#sub').attr('type','button');
             jQuery("#sub").attr('class','btn btn-default');
             jQuery("#no_table_name").attr('class','form-control');
             jQuery("#no_table_name").attr('type','text');
             jQuery("#no_table_domain").attr('type','text');
             jQuery("#no_table_domain").attr('class','form-control');
             jQuery("#no_table_keyname1").attr('class','form-control');
             jQuery("#no_table_keyname1").attr('type','text');
             jQuery("#no_table_keyname2").attr('class','form-control');
             jQuery("#no_table_keyname2").attr('type','text');
             jQuery("#no_table_keyname3").attr('class','form-control');
             jQuery("#no_table_keyname3").attr('type','text');
             jQuery("#no_table_keyname1_value").attr('class','form-control');
             jQuery("#no_table_keyname1_value").attr('type','text');
             jQuery("#no_table_keyname2_value").attr('class','form-control');
             jQuery("#no_table_keyname2_value").attr('type','text');
             jQuery("#no_table_keyname3_value").attr('class','form-control');
             jQuery("#no_table_keyname3_value").attr('type','text');
			 
			 
             jQuery("#subs").attr('class','btn btn-primary');
             jQuery('#no_table_firsttime').attr('class','form-control form-input');
	  	     jQuery('#no_table_firsttime').attr('type','text');
	  	     jQuery('#no_table_lasttime').attr('class','form-control form-input');
	  	     jQuery('#no_table_lasttime').attr('type','text');
	  	     jQuery('#subt').attr('class','btn btn-primary');
	  	     jQuery('#subt').attr('data-toggle','modal');
	  	     jQuery('#subt').attr('data-target','#basicModal');
	  	     /*jQuery('#subt').click(function(){
	  	     	  
	  		      var showa ="数据源保存后只能删除，不能编辑，是否要继续保存？"; 
	  		      var hn=jQuery('#no_table_name').val();
	  		      if(hn){alert(showa);}
	  		      jQuery("#subt").attr("onclick","location='{{=URL('index')}}'");
	  	      });*/
	  	     
             
        });