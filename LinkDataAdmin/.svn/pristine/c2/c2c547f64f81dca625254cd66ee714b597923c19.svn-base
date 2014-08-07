;(function($, window, document){
    var Pagination = function(ele, pageCount, opt){
        this.$element = ele;
        this.$ul = jQuery('<ul></ul>');
        this.pageCount = pageCount;
        this.defaults = {
            'ulClass': 'pagination',
            'liClass': '',
            'inputClass':'form-control form-input',
            'fieldText':'go',
            'fieldWidth':76,
            'itemCount': 12,
            'fnCondition': null,
            'callback':null,
            'numWidth':8,
            'itemWidth':26,
         };
         this.options = $.extend({}, this.defaults, opt);
         return this
    };

    Pagination.prototype = {
        init: function(startPage){
            var pageCount = this.pageCount;
            var $ul = this.$ul;
            var options = this.options;
            var maxWidth = this.$element.width();
            var bNext = false;
            var endPage = startPage + options.itemCount - 1;

            if(pageCount > endPage){
                bNext = true;
                endPage -= 4;
                $pageField = jQuery('<INPUT>');
                $pageField.addClass(this.options.inputClass);
                $pageField.css('float', 'right');
                $pageField.css('width','70px');
                $pageField.css('margin-left','4px');
                $pageField.attr('placeholder',this.options.fieldText);
                this.$element.append($pageField);
                $pageField.click(function(e){
                    e.stopPropagation();
                });

                $pageField.keyup(function(e){
                    e.stopPropagation();
                    if(e.keyCode==13){
                        var target = $(e.target);
                        var c = Number(target.val());
                        if ( c<=0){
                            c = 1
                        }else if (c > pageCount){
                            c = pageCount;
                        }

                        $ul.find('li.active').removeClass('active');
                        var bReset = true;
                        var $li;
                         lis = $ul.children();
                        for(var i=0; i<lis.length;i++){
                            $li = $(lis[i]);
                            if($li.text() == c){
                                if($li.next().text() != '...' && $li.prev().text() != '...'){
                                    $(lis[i]).addClass('active');
                                    bReset = false;
                                }
                                break;
                           }
                        }
                        if(bReset){
                            data = calcStartPage(c, pageCount, maxWidth, options);
                            reset($ul, pageCount, data.startPage, data.endPage, bNext, options);
                            lis = $ul.children();
                            for(var i=0; i<lis.length;i++){
                                $li = $(lis[i]);
                                if($li.text() == c){
                                     $li.addClass('active');
                                    break;
                                }
                            }
                        }
                       if(options.callback){
                            options.callback(c, options.callParam);
                       }
                     }
                 });
            }else{
                endPage = pageCount;
            }
             
            this.$ul.addClass(this.options.ulClass);
            this.$element.append(this.$ul);
            reset($ul, pageCount, startPage, endPage, bNext, options);
            if(bNext){
                $ul.children().eq(0).addClass('disabled');
                $ul.children().eq(1).addClass('active');
            }else{
                $ul.children().eq(0).addClass('active');
            }

            this.$element.click(function(e){
                var opt;
                var $curPage;
                var $clickPage;
                var $target;
                var clickValue;
                var curValue;
                var bReset;
                var lis;
                
                $target = $(e.target);
                if($target.parent().hasClass('disabled')){
                    return;
                }
               
                opt = $target.text();
                $curPage = $(this).find('li.active');
                curValue = $curPage.text();

                if(opt == '<'){
                    $clickPage = $curPage.prev();
                }else if(opt=='>'){
                    $clickPage = $curPage.next();
                }else{
                    $clickPage = $target.parent();
                }
                clickValue = $clickPage.text();
                //alert(clickValue);
                if($clickPage.prev().text() == '...'){
                    data = calcStartPage(clickValue, pageCount, maxWidth, options); 
                   //alert(data.startPage+' -- '+data.endPage);
                    reset($ul, pageCount, data.startPage, data.endPage, bNext, options);
                    lis = $ul.children();
                    for(var i=lis.length-1; i>=0;i--){
                        if($(lis[i]).text() == clickValue){
                            $clickPage = $(lis[i]);
                            break;
                        }
                    }
                }else if ($clickPage.next().text()=='...'){
                    data = calcEndPage(clickValue, pageCount, maxWidth, options);
                    reset($ul, pageCount, data.startPage, data.endPage, bNext, options);
                    lis = $ul.children();
                    for(var i=0; i<lis.length;i++){
                        if($(lis[i]).text() == clickValue){
                            $clickPage = $(lis[i]);
                            break;
                        }
                    }
                }

                $curPage.removeClass('active');   
                $clickPage.addClass('active'); 
                //alert($clickPage.html());
                $prv = $(this).find('li.previous');
                if ($clickPage.text() == '1'){
                    $prv.addClass('disabled');
                }
                if($curPage.text() == '1'){
                    $prv.removeClass('disabled');
                }

                $nxt = $(this).find('li.next');
                //alert($clickPage.text()+' - '+pageCount);
                if($clickPage.text() == pageCount){
                    $nxt.addClass('disabled');
                }
               if($curPage.text() == pageCount){
                    $nxt.removeClass('disabled');
               }

                if(options.callback){
                    options.callback(clickValue, options.callParam);
                }

            });
        }
        
    };

    $.fn.pagination = function(pageCount, startPage, options){
        var p = new Pagination(this, pageCount, options);
        return p.init(startPage);
    };


    function reset($ul, pageCount, startPage, endPage, bNext, options){
        var $first;
         if(endPage - startPage <= 1){
              return ;
         }

         $ul.children().remove();

        if (bNext){
            $li = jQuery('<li></li>');
            $li.addClass(options.liClass);
            $li.addClass('previous');
            $a = jQuery('<a></a>');
            $a.text('<');
            $li.append($a);
            $ul.append($li);
            $first = $li

            if(endPage == pageCount || startPage > 1){
                $li = jQuery('<li></li>');
                $li.addClass(options.liClass);
                $a = jQuery('<a></a>');
                $a.text(1);
                $li.append($a);
                $ul.append($li);

                $li = jQuery('<li></li>');
                $li.addClass(options.liClass);
                $li.addClass('disabled');
                $a = jQuery('<a></a>');
                $a.text('...');
                $li.append($a);
                $ul.append($li);
                $first = $li
            }

            if(startPage == 1 || endPage < pageCount){
                $li = jQuery('<li></li>');
                $li.addClass(options.liClass);
                $li.addClass('disabled');
                $a = jQuery('<a></a>');
                $a.text('...');
                $li.append($a);
                $ul.append($li);

                $li = jQuery('<li></li>');
                $li.addClass(options.liClass);
                $a = jQuery('<a></a>');
                $a.text(pageCount);
                $li.append($a);
                $ul.append($li);
            }

            $li = jQuery('<li></li>');
            $li.addClass(options.liClass);
            $li.addClass('next');
            $a = jQuery('<a></a>');
            $a.text('>');
            $li.append($a);
            $ul.append($li);
        }

        if($first){
            for(var i=startPage, $sFirst=$first; i<=endPage; i++){
                $li = jQuery('<li></li>');
                $li.addClass(options.liClass);
                $a = jQuery('<a></a>');
                $a.text(i);
                $li.append($a);
                $li.insertAfter($first);
                $first = $li
            }
        }else{
            for(var i=startPage; i<=endPage; i++){
                $li = jQuery('<li></li>');
                $li.addClass(options.liClass);
                $a = jQuery('<a></a>');
                $a.text(i);
                $li.append($a);
                $ul.append($li);
            }
        }
    }

    function calcStartPage(clickValue, pageCount, maxWidth, options){
        var itemWidth;
        var w;
        var startPage = clickValue;
        var i = 0;
        var itemCount;
        if(clickValue==pageCount){
            itemWidth = 4 * (options.numWidth+options.itemWidth);
            itemCount = 4;
        }else{
            itemWidth = 5*(options.numWidth+options.itemWidth) + pageCount.toString().length*options.numWidth+options.itemWidth;
            startPage++;
            itemCount = 6;
        }
        maxWidth -= itemWidth + options.fieldWidth;
        w = startPage.toString().length * options.numWidth + options.itemWidth;
        while(1){      
              w += startPage.toString().length * options.numWidth + options.itemWidth;
             if(w >= maxWidth){
                break;
             }
             startPage--;
             if(startPage == 1){
                 i = options.itemCount-5;
                 break;
             }
             
             i++;
             if( i+itemCount == options.itemCount){
                 break;
             }
         }
         if(startPage - 1 == 1){
             startPage = 1;
             i = options.itemCount-5;
         }
         return {startPage:startPage, endPage:startPage+i};
    }

    function calcEndPage(clickValue, pageCount, maxWidth, options){
        var itemWidth;
        var w;
        var startPage = clickValue;
        var i = 0;
        var itemCount;
        var width = maxWidth;

        if(clickValue==1){
            itemWidth = 3 * (options.numWidth+options.itemWidth)+pageCount.toString().length*options.numWidth+options.itemWidth;
            itemCount = 4;
        }else{
            itemWidth = 5*(options.numWidth+options.itemWidth) + pageCount.toString().length*options.numWidth+options.itemWidth;
            startPage--;
            itemCount = 6;
        }
       width -= itemWidth + options.fieldWidth;
        w = startPage.toString().length * options.numWidth + options.itemWidth;
        while(1){             
             w += startPage.toString().length * options.numWidth + options.itemWidth;
             if(w >= width){
                 break;
             }
             startPage++;
             if(startPage == pageCount){
                 break;
             }
             
             i++;
             if( i+itemCount == options.itemCount){
                  startPage--;
                  i--;
                 break;
             }
         }

         if(startPage + 1 == pageCount){
             startPage++;
         }

         if(startPage == pageCount){
                 width = maxWidth - 4 * (options.numWidth+options.itemWidth)-options.fieldWidth;
                 w = startPage.toString().length * options.numWidth + options.itemWidth;
                 i = parseInt(width / w)-1;
         }
         return {startPage:startPage-i, endPage:startPage};
    }
})(jQuery, window, document);