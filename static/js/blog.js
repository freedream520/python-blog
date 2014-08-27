/**
 * Created by xiong on 4/12/14.
 */

var sub=function(str,n){
  var r=/[^\x00-\xff]/g;
  if(str.replace(r,"mm").length<=n){return str;}
  var m=Math.floor(n/2);
  for(var i=m;i<str.length;i++){
      if(str.substr(0,i).replace(r,"mm").length>=n){
          return str.substr(0,i)+"...";
      }
  }
  return str;
}


$(function () {
    $(window).scroll(function (evt) {
        evt = evt || window.event;
        var isTrue = true;
        if (evt.wheelDelta) {//如果是IE/Opera/Chrome浏览器
            if(evt.wheelDelta > 0){
                isTrue = false;
            }
            if(evt.wheelDelta < 0){
                isTrue = true;
            }
        } else if (evt.detail) {//如果是Firefox浏览器
            if(evt.detail > 0){
                isTrue = false;
            }
            if(evt.detail < 0){
                isTrue = true;
            }
        }
        var curPage = $("#next").attr("href");
        var totalPage = $("#next").attr("data-number");
        if(curPage <= totalPage && isTrue) {
            if ($(this).scrollTop() + 10 > document.body.scrollHeight-document.body.clientHeight) {
                var next = "/scroll_load/?page="+curPage;
                $("#next").attr("href", parseInt(curPage)+1);
                ajaxGet(next, function (content) {
                    //onSuccess
                    //alert(content.articles);
                    var contents = jQuery.parseJSON(content.articles);
                    $.each(contents, function (index, value) {
                        $('#article').append('<article class="news-item">'
                            + '<h4 class="title">'
                            + '<a target="_" href="/blog/'
                            + value.fields.slug
                            + '">'
                            + value.fields.title
                            + '</a> </h4>'
                            +'<div class="meta">'
                            + Date(value.fields.date_publish).slice(3, 15)
                            + '</div></article><hr/>'
                        );
                    });
                });
            }
        }
        else {

        }
    });




    /**
     * Get the random article function
     */
    function get_random_article(){
        ajaxGet('/random-list/', function(content){
            //alert(content.list);
            random_articles = jQuery.parseJSON(content.articles);
            $('#random-list li').remove();
            $.each(random_articles, function(index, value){
                $('#random-list').append('<li class="random-article"><a target="_" href="/blog/'
                + value.fields.slug
                +'" title="'
                + value.fields.title
                + '">'
                + sub(value.fields.title, 10)
                +'</a></li>');
            })
        });
    }

    get_random_article();

    setInterval(get_random_article, 300000);

    if($('#relate-list').length > 0){
        var href = '/relate-list/' + $('#article-title').text();
        ajaxGet(href, function(content){
            //alert(content.list);
            random_articles = jQuery.parseJSON(content.articles);
            $('#random-list li').remove();
            $.each(random_articles, function(index, value){
                $('#relate-list').append('<li class="random-article"><a target="_" href="/blog/'
                + value.fields.slug
                +'" title="'
                + value.fields.title
                + '">'
                + sub(value.fields.title, 10)
                +'</a></li>');
            })
        });
    }

    /**
     * fixed the sidebar nav
     * and Go top
     */
    $(window).scroll(function () {
        var winH = $(this).scrollTop();
        if ( winH> 100) {
            $("#go_top").fadeIn(1000);
        }
        else {
            $("#go_top").fadeOut(500);
        }
    });

    $("#go_top").click(function () {
        $(document.body).animate({scrollTop: 0}, 1000);
        return false;
    });
});
