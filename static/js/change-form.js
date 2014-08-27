/**
 * Created by Smile on 6/11/2014.
 */
$(function () {
    $("#grp-header").css({"position": "relative"});
    $("#grp-content").css({"padding-bottom": "60px"});
    $(".category").css({"display": "inline-block", "width": "40%", "clear": "none"});
    $(".date_publish").css({"display": "inline-block", "width": "50%", "clear": "none"});
    $("#id_content_markdown").css({"width": $("#id_content_markdown_wmd_button_bar").width() * 0.499});
    $("#id_content_markdown_wmd_preview").css({"width": $("#id_content_markdown_wmd_button_bar").width() * 0.5});

    $(window).resize(function () {
        $("#id_content_markdown").css({"width": $("#id_content_markdown_wmd_button_bar").width() * 0.499});
        $("#id_content_markdown_wmd_preview").css({"width": $("#id_content_markdown_wmd_button_bar").width() * 0.5});

        //alert($("#id_content_markdown").attr("width") + $("#id_content_markdown_wmd_preview").attr("width"));
    });

});